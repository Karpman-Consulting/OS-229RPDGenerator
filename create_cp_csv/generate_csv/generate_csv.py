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

# # Write JSON data to a file
# with open("parent_data.json", "w") as json_file:
#     json.dump(rpd, json_file, indent=4)  # `indent` for pretty formatting

required_compliance_parameters = [

  ### Project and building
  {
    "compliance_parameter_category": "ruleset_project_description",
    "compliance_parameter": "compliance_path",
    "comp_param_path":'$.ruleset_model_descriptions[0]'
  },
  {
    "compliance_parameter_category": "ruleset_project_description",
    "compliance_parameter": "type",
    "comp_param_path":'$.ruleset_model_descriptions[0]'
  },
  {
    "compliance_parameter_category": "ruleset_project_description",
    "compliance_parameter": "measured_infiltration_pressure_difference",
    "comp_param_path":'$.ruleset_model_descriptions[0]'
  },
  {
    "compliance_parameter_category": "ruleset_project_description",
    "compliance_parameter": "is_measured_infiltration_based_on_test",
    "comp_param_path":'$.ruleset_model_descriptions[0]'
  },
  {
    "compliance_parameter_category": "ruleset_project_description",
    "compliance_parameter": "site_zone_type",
    "comp_param_path":'$.ruleset_model_descriptions[0].buildings[0].building_segments[0]'
  },
  {
    "compliance_parameter_category": "building",
    "compliance_parameter": "building_open_schedule",
    "comp_param_path":'$.ruleset_model_descriptions[0].buildings[0]'
  },
    {
    "compliance_parameter_category":"building_segment",
    "compliance_parameter":"is_all_new",
    "comp_param_path":'$.ruleset_model_descriptions[0].buildings[0].building_segments[0]'
  },
      {
    "compliance_parameter_category":"building_segment",
    "compliance_parameter":"is_all_new",
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
    # HeatingVentilatingAirConditioningSystem
    {
    "compliance_parameter_category":"HeatingVentilatingAirConditioningSystem",
    "compliance_parameter": "status_type",
    "comp_param_path":'$.ruleset_model_descriptions[0].buildings[0].building_segments[0].heating_ventilating_air_conditioning_systems[*]'
  },
  ###HeatingVentilatingAirConditioningSystem.FanSystem
  {
    "compliance_parameter_category":"HeatingVentilatingAirConditioningSystem.FanSystem",
    "compliance_parameter": "air_filter_merv_rating",
    "comp_param_path":'$.ruleset_model_descriptions[0].buildings[0].building_segments[0].heating_ventilating_air_conditioning_systems[*]'
  },
  {
    "compliance_parameter_category":"HeatingVentilatingAirConditioningSystem.FanSystem",
    "compliance_parameter": "has_fully_ducted_return",
    "comp_param_path":'$.ruleset_model_descriptions[0].buildings[0].building_segments[0].heating_ventilating_air_conditioning_systems[*]'
  },
  ### Zone 
    {
    "compliance_parameter_category":"Zone",
    "compliance_parameter": "aggregation_factor",
    "comp_param_path":'$.ruleset_model_descriptions[0].buildings[0].building_segments[0].zones[*]'
  },
  {
    "compliance_parameter_category":"Zone",
    "compliance_parameter": "conditioning_type",
    "comp_param_path":'$.ruleset_model_descriptions[0].buildings[0].building_segments[0].zones[*]'
  },
  

  ### Zone.Infiltration
  {
    "compliance_parameter_category":"infiltration",
    "compliance_parameter": "measured_air_leakage_rate",
    "comp_param_path":'$.ruleset_model_descriptions[0].buildings[0].building_segments[0].zones[*].infiltration'
  },
  ### Terminals
  {
    "compliance_parameter_category":"terminal",
    "compliance_parameter": "is_supply_ducted",
    "comp_param_path":'$.ruleset_model_descriptions[0].buildings[0].building_segments[0].zones[*].terminals[*]'
  },

  ### SUrfaces
  {
    "compliance_parameter_category":"surface",
    "compliance_parameter": "status_type",
    "comp_param_path":'$.ruleset_model_descriptions[0].buildings[0].building_segments[0].zones[*].surfaces[*]'
  },

  ### Subsurfaces
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
    "compliance_parameter_category":"subsurface",
    "compliance_parameter": "is_operable",
    "comp_param_path":'$.ruleset_model_descriptions[0].buildings[0].building_segments[0].zones[*].surfaces[*].subsurfaces[*]'
  },
      {
    "compliance_parameter_category":"subsurface",
    "compliance_parameter": "framing_type",
    "comp_param_path":'$.ruleset_model_descriptions[0].buildings[0].building_segments[0].zones[*].surfaces[*].subsurfaces[*]'
  },
        {
    "compliance_parameter_category":"subsurface",
    "compliance_parameter": "status_type",
    "comp_param_path":'$.ruleset_model_descriptions[0].buildings[0].building_segments[0].zones[*].surfaces[*].subsurfaces[*]'
  },
          {
    "compliance_parameter_category":"subsurface",
    "compliance_parameter": "has_open_sensor",
    "comp_param_path":'$.ruleset_model_descriptions[0].buildings[0].building_segments[0].zones[*].surfaces[*].subsurfaces[*]'
  },
  ### Spaces
  {
    "compliance_parameter_category":"space",
    "compliance_parameter": "status_type",
    "comp_param_path":'$.ruleset_model_descriptions[0].buildings[0].building_segments[0].zones[*].spaces[*]'
  },
    {
    "compliance_parameter_category":"space",
    "compliance_parameter": "lighting_space_type",
    "comp_param_path":'$.ruleset_model_descriptions[0].buildings[0].building_segments[0].zones[*].spaces[*]'
  },
    {
    "compliance_parameter_category":"space",
    "compliance_parameter": "function",
    "comp_param_path":'$.ruleset_model_descriptions[0].buildings[0].building_segments[0].zones[*].spaces[*]'
  },
    {
    "compliance_parameter_category":"space",
    "compliance_parameter": "ventilation_space_type",
    "comp_param_path":'$.ruleset_model_descriptions[0].buildings[0].building_segments[0].zones[*].spaces[*]'
  },
      {
    "compliance_parameter_category":"space",
    "compliance_parameter": "envelope_space_type",
    "comp_param_path":'$.ruleset_model_descriptions[0].buildings[0].building_segments[0].zones[*].spaces[*]'
  },
  {
    "compliance_parameter_category":"space",
    "compliance_parameter": "occupancy_control_type",
    "comp_param_path":'$.ruleset_model_descriptions[0].buildings[0].building_segments[0].zones[*].spaces[*].interior_lighting[*]'
  },
  ## Schedules
  {
    "compliance_parameter_category":"schedule",
    "compliance_parameter": "prescribed_type",
    "comp_param_path":'$.ruleset_model_descriptions[0].schedules[*]'
  },
  {
    "compliance_parameter_category":"schedule",
    "compliance_parameter": "is_modified_for_workaround",
    "comp_param_path":'$.ruleset_model_descriptions[0].schedules[*]'
  },
  ### Pump

    {
    "compliance_parameter_category":"pump",
    "compliance_parameter": "impeller_efficiency",
    "comp_param_path":'$.ruleset_model_descriptions[0].pumps[*]'
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

    ids = jsonpath.jsonpath(rpd, compliance_parameter["comp_param_path"] + '.' + 'id')

    values = jsonpath.jsonpath(rpd, compliance_parameter["comp_param_path"] + '.' + compliance_parameter["compliance_parameter"])

    if values is False:
      print('### Could not get data for compliance parameter: ', compliance_parameter["comp_param_path"] + '.' + compliance_parameter["compliance_parameter"])  
      continue
      
    two_twenty_nine_type = jsonpath.jsonpath(rpd, compliance_parameter["comp_param_path"] + '.' + 'json_path')
    two_twenty_nine_parent_id = jsonpath.jsonpath(rpd, compliance_parameter["comp_param_path"] + '.' + 'parent_id')
    compliance_parameter_category = compliance_parameter["compliance_parameter_category"]

    for index in range(len(values)):
        csv_data.append([ids[index],
        get_last_part_json_path(two_twenty_nine_type[index]),
        get_last_part_json_path(two_twenty_nine_parent_id[index]),
        compliance_parameter_category,
        compliance_parameter["compliance_parameter"],values[index]])

with open('./output_comp_param.csv', 'w', newline='') as file:  # Ensure `file` is opened in write mode
    writer = csv.writer(file)  # Create a CSV writer
    writer.writerows(csv_data)  # Write the rows to the file
