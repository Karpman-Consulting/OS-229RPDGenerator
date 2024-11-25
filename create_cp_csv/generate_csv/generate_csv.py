import jsonpath
import os
import json
import csv

empty_cp_json_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),'ASHRAE901_OfficeSmall_STD2019_Denver.comp-param-empty.json')

with open(empty_cp_json_file_path, 'r') as file:
    rpd = json.load(file)

def add_parent_ids_and_path(obj, parent_ids=None, path=""):
    """
    Recursively adds a parent_id and simplified JSON path (keys only, no $ or indices)
    to each object with an 'id' field in the JSON.
    """
    if parent_ids is None:
        parent_ids = []

    if isinstance(obj, dict):
        # If the current object has an 'id', update its 'parent_ids' and 'json_path'
        if "id" in obj:
            # Join the parent ids into a path and assign it to the parent_id field
            obj["parent_id"] = ".".join(parent_ids)
            obj["json_path"] = path.strip(".")  # Remove leading/trailing dots

        # Update parent_ids for child objects
        if "id" in obj:
            new_parent_ids = parent_ids + [obj["id"]]
        else:
            new_parent_ids = parent_ids

        # Recursively process child elements
        for key, value in obj.items():
            child_path = f"{path}.{key}" if path else key
            add_parent_ids_and_path(value, new_parent_ids, child_path)

    elif isinstance(obj, list):
        for item in obj:
            add_parent_ids_and_path(item, parent_ids, path)

# Process the JSON to add parent IDs and simplified paths
add_parent_ids_and_path(rpd)

# Write JSON data to a file
with open("parent_data.json", "w") as json_file:
    json.dump(rpd, json_file, indent=4)  # `indent` for pretty formatting

"$.ruleset_model_descriptions[0].buildings[0].building_segments[0].zones[*]"
required_compliance_parameters = [
#   {
#     "ruleset_model_descriptions": "compliance_path",
#     "id_path":"id"
#   },
#   {
#     "ruleset_model_descriptions": "type",
#     "229_parent_id":"$.ruleset_model_descriptions[0].id",
#     "id_path":'$.ruleset_model_descriptions[0].id',
#     "comp_param_path":'$.ruleset_model_descriptions[0].type'
#   },
#   {
#     "229_parent_id":"$.ruleset_model_descriptions[0].id",
#     "building": "building_open_schedule",
#     "id_path":'$.ruleset_model_descriptions[0].id',
#     "comp_param_path":'$.ruleset_model_descriptions[0].building_open_schedule'
#   },
  {
    "compliance_parameter_category": "building_segment",
    "compliance_parameter": "is_all_new",
    "comp_param_path":'$.ruleset_model_descriptions[0].buildings[0].building_segments[0]'
  },
  {
    "compliance_parameter_category":"building_segment",
    "compliance_parameter":"lighting_building_area_type",
    "comp_param_path":'$.ruleset_model_descriptions[0].buildings[0].building_segments[0]'
  },
  {
    "compliance_parameter_category":"building_segment",
    "compliance_parameter":"area_type_vertical_fenestration",
    "comp_param_path":'$.ruleset_model_descriptions[0].buildings[0].building_segments[0]'
  },
  {
    "compliance_parameter_category":"building_segment",
    "compliance_parameter": "area_type_heating_ventilating_air_conditioning_system",
    "comp_param_path":'$.ruleset_model_descriptions[0].buildings[0].building_segments[0]'
  },
    ### Priotize using surfaces and subsurface 
    ### Need to keep track of the parent as im going through int his case it wont work
  {
    "compliance_parameter_category":"infiltration",
    "compliance_parameter": "measured_air_leakage_rate",
    "comp_param_path":'$.ruleset_model_descriptions[0].buildings[0].building_segments[0].zones[*].infiltration'
  },
  {
    "compliance_parameter_category":"terminal",
    "compliance_parameter": "is_supply_ducted",
    "comp_param_path":'$.ruleset_model_descriptions[0].buildings[0].building_segments[0].zones[*].terminals[*]'
  },
  {
    "compliance_parameter_category":"space",
    "compliance_parameter": "lighting_space_type",
    "comp_param_path":'$.ruleset_model_descriptions[0].buildings[0]'
  },
  {
    "compliance_parameter_category":"subsurface",
    "compliance_parameter": "subclassification",
    "comp_param_path":'$.ruleset_model_descriptions[0].buildings[0].building_segments[0].zones[*].surfaces[*].subsurfaces[*]'
  },
  {
    "compliance_parameter_category":"subsurface",
    "compliance_parameter": "has_manual_interior_shades",
    "comp_param_path":'$.ruleset_model_descriptions[0].buildings[0].building_segments[0].zones[*].surfaces[*].subsurfaces[*]'
  },
    {
    "compliance_parameter_category":"HeatingVentilatingAirConditioningSystem",
    "compliance_parameter": "status_type",
    "comp_param_path":'$.ruleset_model_descriptions[0].buildings[0].building_segments[0].heating_ventilating_air_conditioning_systems[*]'
  },
#   {
#     "Boiler": "draft_type"
#   },
#   {
#     "Chiller": "compressor_type"
#   },
#   {
#     "HeatRejection": "fan_type"
#   },
#   {
#     "heating_ventilating_air_conditioning_systems": "status_type"
#   },
#   {
#     "heating_ventilating_air_conditioning_systems.fan_system": "air_filter_merv_rating"
#   },
#   {
#     "zone": "aggregation_factor"
#   },
#   {
#     "zone.infiltration": "measured_air_leakage_rate"
#   },


]

def get_last_part_json_path(json_path):
    return json_path.split('.')[-1]

csv_data = [['229 data group id','229 parent type','229 parent id','compliance_parameter_category','compliance parameter name','compliance parameter value']]

for compliance_parameter in required_compliance_parameters:

    # if compliance_parameter["compliance_parameter"] == "status_type":
    #   breakpoint()
    
    ids = jsonpath.jsonpath(rpd, compliance_parameter["comp_param_path"] + '.' + 'id')

    values = jsonpath.jsonpath(rpd, compliance_parameter["comp_param_path"] + '.' + compliance_parameter["compliance_parameter"])

    if values is False:
      print('### Could not get data for compliance parameter: ', compliance_parameter["comp_param_path"] + '.' + compliance_parameter["compliance_parameter"])  
      continue
      
    two_twenty_nine_type = jsonpath.jsonpath(rpd, compliance_parameter["comp_param_path"] + '.' + 'json_path')
    two_twenty_nine_parent_id = jsonpath.jsonpath(rpd, compliance_parameter["comp_param_path"] + '.' + 'parent_id')
    compliance_parameter_category = compliance_parameter["compliance_parameter_category"]


    for index, id in enumerate(values):
        csv_data.append([ids[index],
        get_last_part_json_path(two_twenty_nine_type[index]),
        get_last_part_json_path(two_twenty_nine_parent_id[index]),
        compliance_parameter_category,
        compliance_parameter["compliance_parameter"],values[index]])


breakpoint()
with open('./output_comp_param.csv', 'w', newline='') as file:  # Ensure `file` is opened in write mode
    writer = csv.writer(file)  # Create a CSV writer
    writer.writerows(csv_data)  # Write the rows to the file
