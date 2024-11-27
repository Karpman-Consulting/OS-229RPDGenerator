require 'minitest/autorun'
require_relative './generate_csv'

class GenerateCsvDataTest < Minitest::Test

  def setup

    @empty_cp_json_file_path = File.join(File.dirname(File.realpath(__FILE__)), 'ASHRAE901_OfficeSmall_STD2019_Denver.comp-param-empty.json')

    @rpd = JSON.parse(File.read(@empty_cp_json_file_path))
  end

  def test_generate_comp_param_empty_csv_with_parent_ids_and_path

    File.write('./output_with_parent.json',JSON.pretty_generate(GenerateCsvOfCompParamJson.add_parent_ids_and_path(@rpd)))

  end

  def test_write_out_csv_data

    # Set the path to the JSON file
    # Read and parse the JSON file
    #
    #File.write('./output_with_parent.json', JSON.pretty_generate(@rpd))

    # Define required compliance parameters
    # # Initialize CSV data
    csv_data = GenerateCsvOfCompParamJson.produce_csv_data(@rpd)

    GenerateCsvOfCompParamJson.write_csv_data(csv_data,'./output_comp_param.csv')
    # Write CSV data to a file
  end
end
