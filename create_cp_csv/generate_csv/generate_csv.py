import jsonpath
import os
import json
import csv

empty_cp_json_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),'ASHRAE901_OfficeSmall_STD2019_Denver.comp-param-empty.json')

with open(empty_cp_json_file_path, 'r') as file:
    rpd = json.load(file)

def add_parent_and_path(obj, parent_id=None, path=""):
    """
    Recursively adds a parent_id and simplified JSON path (keys only, no $ or indices)
    to each object with an 'id' field in the JSON.
    """
    if isinstance(obj, dict):
        # Add parent_id and json_path if 'id' exists in this dictionary
        if "id" in obj:
            obj["parent_id"] = parent_id
            obj["json_path"] = path.strip(".")  # Remove leading/trailing dots
        
        # Recursively process child elements
        for key, value in obj.items():
            child_path = f"{path}.{key}" if path else key  # Build the key-based path
            add_parent_and_path(value, obj.get("id"), child_path)

    elif isinstance(obj, list):
        for item in obj:
            add_parent_and_path(item, parent_id, path)  # Keep the current path for lists

# Process the JSON to add parent IDs and simplified paths
add_parent_and_path(rpd)

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
    "building_segment": "is_all_new",
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
    "comp_param_path":'$.ruleset_model_descriptions[0].buildings[0].building_segments[0].zones[*].terminals'
  },
    {
    "compliance_parameter_category":"terminal",
    "compliance_parameter": "is_supply_ducted",
    "comp_param_path":'$.ruleset_model_descriptions[0].buildings[0].building_segments[0].zones[*].terminals'
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

  ### TODO solve this problem
  ### No clear match between surface and zone id
  # "229_parent_id":"$.ruleset_model_descriptions[0].buildings[0].building_segments[0].zones[*].id
  # "compliance_parameter_category":"Infiltration",
  # "compliance_parameter": "status_type",
  # "id_path":'$.ruleset_model_descriptions[0].buildings[0].building_segments[0].zones[*].surfaces[*].id',
  # "comp_param_path":'$.ruleset_model_descriptions[0].buildings[0].building_segments[0].zones[*].surfaces[*].status_type'



#num_of_rows = $.ruleset_model_descriptions[0].buildings[0].building_segments[0].zones[*]

csv_data = [['229 parent id','compliance_parameter_category','compliance parameter name','compliance parameter value']]

for compliance_parameter in required_compliance_parameters:
    
    ids = jsonpath.jsonpath(rpd, compliance_parameter["id_path"])
    values = jsonpath.jsonpath(rpd, compliance_parameter["comp_param_path"])

    two_twenty_nine_parent_id = jsonpath.jsonpath(rpd,compliance_parameter["229_parent_id"])
    compliance_parameter_category = compliance_parameter["compliance_parameter_category"]
    
    print(compliance_parameter["comp_param_path"],'compliance_parameter["comp_param_path"]')
    print(two_twenty_nine_parent_id,'two_twenty_nine_parent_id')
    print(compliance_parameter_category,'compliance_parameter_category')
    print(ids,'ids')
    print(values,'values')

    for index, id in enumerate(values):
        #print(index)
        csv_data.append([two_twenty_nine_parent_id,compliance_parameter_category,ids[index],values[index]])

    # print(two_twenty_nine_parent_id,'two_twenty_nine_parent_id')
    # print(compliance_parameter_category,'compliance_parameter_category')
    # print(values,'values')
    # print(ids,'ids')

    #csv.append([list(x) for x in zip(two_twenty_nine_parent_id,compliance_parameter_category,ids, values)].flatten)

    #print(zipped)


with open('output_comp_param.csv', 'w', newline='') as file:  # Ensure `file` is opened in write mode
    writer = csv.writer(file)  # Create a CSV writer
    writer.writerows(csv_data)  # Write the rows to the file

    # breakpoint()

    # id_value_dict = zip(two_twenty_nine_parent_id,compliance_parameter_category,ids, values)



    # print(list(id_value_dict),'id_value_dict')

    
            

# # with open('people.csv', mode='w', newline='') as file:
# #     writer = csv.writer(file)


# # zones_json_key_path = "$.ruleset_model_descriptions[0].buildings[0].building_segments[0].zones[*]"

# # json_zones_list = find_all(zones_json_key_path, rpd)
# # breakpoint()
# # print(json_zones_list)


# with open('cp_parameters_csv', "w") as json_file:
#     json.dump(json_zones_list, json_file, indent=4)
