# import json

# # Load the JSON file
# with open("ASHRAE901_OfficeSmall_STD2019_Denver.comp-param-empty.json", "r") as file:
#     data = json.load(file)

# def add_parent_id(obj, parent_id=None):
#     """
#     Recursively adds a parent_id to each object with an 'id' field in the JSON.
#     """
#     if isinstance(obj, dict):
#         # Add parent_id if 'id' exists in this dictionary
#         if "id" in obj:

#             obj["parent_id"] = parent_id
        
#         # Recursively process child elements
#         for key, value in obj.items():
#             add_parent_id(value, obj.get("id"))
#     elif isinstance(obj, list):
#         for item in obj:
#             add_parent_id(item, parent_id)

# # Process the JSON to add parent IDs
# add_parent_id(data)

# # Save the modified JSON to a new file
# with open("output_with_parent_ids.json", "w") as file:
#     json.dump(data, file, indent=4)

import json

# Load the JSON file
with open("ASHRAE901_OfficeSmall_STD2019_Denver.comp-param-empty.json", "r") as file:
    data = json.load(file)

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
add_parent_and_path(data)

with open("output_with_clean_paths.json", "w") as file:
    json.dump(data, file, indent=4)

# import json

# # Load the JSON file
# with open("ASHRAE901_OfficeSmall_STD2019_Denver.comp-param-empty.json", "r") as file:
#     data = json.load(file)

# def add_parent_and_path(obj, parent_id=None, path="$"):
#     """
#     Recursively adds a parent_id and JSON path to each object with an 'id' field in the JSON.
#     """
#     if isinstance(obj, dict):
#         # Add parent_id and json_path if 'id' exists in this dictionary
#         if "id" in obj:
#             obj["parent_id"] = parent_id
#             obj["json_path"] = path
        
#         # Recursively process child elements
#         for key, value in obj.items():
#             child_path = f"{path}.{key}" if path != "$" else f"{path}{key}"
#             add_parent_and_path(value, obj.get("id"), child_path)
#     elif isinstance(obj, list):
#         for index, item in enumerate(obj):
#             child_path = f"{path}[{index}]"
#             add_parent_and_path(item, parent_id, child_path)

# # Process the JSON to add parent IDs and paths
# add_parent_and_path(data)

# # Save the modified JSON to a new file
# with open("output_with_parent_and_path.json", "w") as file:
#     json.dump(data, file, indent=4)