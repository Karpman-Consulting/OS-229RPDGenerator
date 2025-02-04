import csv
import json
from collections import defaultdict
from pathlib import Path
from typing import Tuple, List, Dict, Union, Any


def transfer_csv_to_rpd(json_dict_path: Path, csv_file_path: Path) -> Path:
    """
    Transfers data from a CSV file to a JSON dictionary and writes the result to an RPD file.

    Args:
        json_dict_path (Path): Path to the JSON file to be modified.
        csv_file_path (Path): Path to the CSV file containing data mappings.

    Returns:
        Path: Path to the output RPD file.
    """
    with json_dict_path.open(mode="r", encoding="utf-8") as file:
        json_dict = json.load(file)

    csv_map, building_segment_map = load_csv_to_dict(csv_file_path)
    add_building_segments(json_dict, building_segment_map)
    json_dict = transfer_data_recursive(json_dict, csv_map)

    output_path = csv_file_path.parent / f"{csv_file_path.stem}.rpd"
    with output_path.open(mode="w", encoding="utf-8") as file:
        json.dump(json_dict, file, indent=4)

    return output_path


def load_csv_to_dict(csv_file_path: Path) -> Tuple[Dict[str, Dict[str, Dict[str, str]]], Dict[str, Dict[str, List[Dict[str, str]]]]]:
    """
    Reads a CSV file and organizes the data into a nested dictionary for mapping.

    The CSV must contain "229 Data Group ID" and "Compliance Parameter" columns.

    Args:
        csv_file_path (Path): Path to the CSV file.

    Returns:
        Dict[str, Dict[str, Dict[str, str]]]: A nested dictionary where:
            - The first key is the "229 Data Group ID".
            - The second key is the "Compliance Parameter".
            - The value is the corresponding row dictionary from the CSV.
    """
    param_map: Dict[str, Dict[str, Dict[str, str]]] = defaultdict(dict)
    segment_map: Dict[str, Dict[str, list]] = defaultdict(lambda: defaultdict(list))

    with csv_file_path.open(mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            parent_id = row.get("229 Parent ID")
            parent_key = row.get("229 Parent Key")
            data_group_id = row.get("229 Data Group ID")
            param = row.get("Compliance Parameter")

            if data_group_id and param:
                param_map[data_group_id][param] = row

            if parent_key in ["zones", "heating_ventilating_air_conditioning_systems"]:
                segment_map[parent_id][parent_key].append(row)

    return param_map, segment_map


def transfer_data_recursive(json_dict: Dict[str, Any], csv_map: Dict[str, Dict[str, Dict[str, str]]]) -> Dict[str, Any]:
    """
    Recursively updates values in a JSON dictionary using a CSV mapping.

    If a matching entry exists in the CSV map, it updates the value in the JSON.
    If the corresponding CSV value is empty, the key is removed from the JSON.

    Args:
        json_dict (Dict[str, Any]): The JSON dictionary to update.
        csv_map (Dict[str, Dict[str, Dict[str, str]]]): The nested dictionary from the CSV file.

    Returns:
        Dict[str, Any]: The updated JSON dictionary.
    """
    current_object_id = json_dict.get("id", "n/a")

    for key, value in list(json_dict.items()):
        if current_object_id in csv_map and key in csv_map[current_object_id]:
            csv_row_data = csv_map[current_object_id][key]
            param_value = csv_row_data.get("Compliance Parameter Value")

            if param_value:
                # Update JSON with the value from CSV, formatted correctly
                json_dict[key] = format_value(param_value)
            else:
                # Remove key if the CSV value is empty
                del json_dict[key]

        # Recursively apply the update to nested dictionaries or lists
        if isinstance(value, dict):
            json_dict[key] = transfer_data_recursive(value, csv_map)
        elif isinstance(value, list):
            json_dict[key] = [
                transfer_data_recursive(item, csv_map) if isinstance(item, dict) else item
                for item in value
            ]

    return json_dict


def add_building_segments(json_dict: Dict[str, Any], csv_map: Dict[str, Dict[str, List[Dict[str, str]]]]) -> Dict[str, Any]:
    building_segments = (
        json_dict.get("ruleset_model_descriptions", [{}])[0]
        .get("buildings", [{}])[0]
        .get("building_segments", [])
    )
    # Create a map for fast lookup of segments by ID
    segment_map = {segment.get("id"): segment for segment in building_segments}

    # Collect all zones and HVAC systems from existing segments
    zone_map = {}
    hvac_map = {}

    for segment in building_segments:
        segment.setdefault("zones", [])
        segment.setdefault("heating_ventilating_air_conditioning_systems", [])

        # Store zones and HVACs in dictionaries by ID for easy retrieval
        for zone in segment["zones"]:
            zone_map[zone["id"]] = zone

        for hvac in segment["heating_ventilating_air_conditioning_systems"]:
            hvac_map[hvac["id"]] = hvac

        # Clear zones and HVACs
        segment["zones"] = []
        segment["heating_ventilating_air_conditioning_systems"] = []

    added_ids = set()
    for segment_id, mappings in csv_map.items():

        # Create a new BuildingSegment if the ID doesn't already exist
        if segment_id not in segment_map:
            segment_map[segment_id] = {
                "id": segment_id,
                "zones": [],
                "heating_ventilating_air_conditioning_systems": []
            }
            building_segments.append(segment_map[segment_id])

        segment = segment_map[segment_id]

        # Move zones
        if "zones" in mappings:
            for zone_csv_data in mappings["zones"]:
                zone_id = zone_csv_data.get("229 Data Group ID")
                if zone_id not in zone_map:
                    raise ValueError(f"Zone ID ({zone_id}) was referenced in the CSV file but could not be found in the model files.")
                if zone_id not in added_ids:
                    segment["zones"].append(zone_map[zone_id])
                    added_ids.add(zone_id)

        # Move HVAC systems
        if "heating_ventilating_air_conditioning_systems" in mappings:
            for hvac_csv_data in mappings["heating_ventilating_air_conditioning_systems"]:
                hvac_id = hvac_csv_data.get("229 Data Group ID")
                if hvac_id not in hvac_map:
                    raise ValueError(f"HVAC ID ({hvac_id}) was referenced in the CSV file but could not be found in the model files.")
                if hvac_id not in added_ids:
                    segment["heating_ventilating_air_conditioning_systems"].append(hvac_map[hvac_id])
                    added_ids.add(hvac_id)

    return json_dict


def format_value(value: str) -> Union[int, float, bool, str]:
    """
    Converts a string value into an appropriate JSON-compatible data type.

    - Converts numeric strings to int or float.
    - Converts "true"/"false" (case-insensitive) to boolean.
    - Returns other values as strings.

    Args:
        value (str): The value to format.

    Returns:
        Union[int, float, bool, str]: The formatted value.
    """
    value = value.strip()

    if value.isdigit():
        return int(value)
    elif value.replace(".", "", 1).isdigit():
        return float(value)
    elif value.lower() == "true":
        return True
    elif value.lower() == "false":
        return False
    return value
