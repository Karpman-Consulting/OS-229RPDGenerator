import csv
import json
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, Union


def transfer_csv_to_rpd(json_dict_path: Path, csv_file_path: Path) -> int:
    """
    Transfers data from a CSV file to a JSON dictionary and writes the result to an RPD file.

    Args:
        json_dict_path (Path): Path to the JSON file to be modified.
        csv_file_path (Path): Path to the CSV file containing data mappings.

    Returns:
        int: Returns 1 upon successful completion.
    """
    with json_dict_path.open(mode="r", encoding="utf-8") as file:
        json_dict = json.load(file)

    csv_map = load_csv_to_dict(csv_file_path)
    json_dict = transfer_data_recursive(json_dict, csv_map)

    output_path = json_dict_path.parent / "in.rpd"
    with output_path.open(mode="w", encoding="utf-8") as file:
        json.dump(json_dict, file, indent=4)

    return 1


def load_csv_to_dict(csv_file_path: Path) -> Dict[str, Dict[str, Dict[str, str]]]:
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
    json_map: Dict[str, Dict[str, Dict[str, str]]] = defaultdict(dict)

    with csv_file_path.open(mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            data_group_id = row.get("229 Data Group ID")
            param = row.get("Compliance Parameter")

            if data_group_id and param:
                json_map[data_group_id][param] = row

    return json_map


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
