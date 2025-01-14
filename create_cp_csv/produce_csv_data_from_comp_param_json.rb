require 'json'
require_relative '../CompParamJson/generate_csv'

empty_comp_param_json_file_path = ARGV[0]
empty_comp_param_json = JSON.parse(File.read(empty_comp_param_json_file_path))
csv_data = GenerateTwoTwoNineCompParamJsonCsv.produce_csv_data_from_comp_param_json(empty_comp_param_json)
puts csv_data.to_json
