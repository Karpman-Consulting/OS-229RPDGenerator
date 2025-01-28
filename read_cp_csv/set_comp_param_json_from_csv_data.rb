require 'json'
require_relative '../CompParamJson/generate_csv'


comp_param_json_file_path = ARGV[0]
csv_data_file_path = ARGV[1]

comp_param_json = JSON.parse(File.read(comp_param_json_file_path))
csv_data = JSON.parse(File.read(csv_data_file_path)).map { |csv_row| csv_row.transform_keys(&:to_sym) }

# Process the data
updated_comp_param_json = GenerateTwoTwoNineCompParamJsonCsv.set_comp_param_json_from_csv_data(comp_param_json,csv_data)

# Output the result
puts updated_comp_param_json.to_json
