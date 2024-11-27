require 'minitest/autorun'
require_relative '../generate_csv'
require 'pry-byebug'

class GenerateCsvDataTest < Minitest::Test

  ## TODO write tests for generate_csv
  def setup

    @empty_cp_json_file_path = File.join(File.dirname(File.realpath(__FILE__)), 'ASHRAE901_OfficeSmall_STD2019_Denver.comp-param-empty.json')

    @empty_cp_json = JSON.parse(File.read(@empty_cp_json_file_path))
  end

  def test_generate_comp_param_empty_csv

    # # Set the path to the JSON file
    # # Read and parse the JSON file
    # #
    # #File.write('./output_with_parent.json', JSON.pretty_generate(@rpd))
    #
    csv_data = GenerateCsvOfCompParamJson.produce_csv_data(@empty_cp_json)

    # # Define required compliance parameters
    # # # Initialize CSV data
    # csv_data = GenerateCsvOfCompParamJson.produce_csv_data(@rpd)

    CSV.open(File.join('./','comp_param_empty.csv'), 'w') do |csv_data_as_excel|

      csv_data_as_excel <<
      ['229 data group id',
      '229 parent type',
      '229 parent id',
      'compliance parameter category',
      'compliance parameter name',
      'compliance parameter value']

      csv_data.each { |row_as_hash_of_data|
        csv_data_as_excel << [
            row_as_hash_of_data[:two_twenty_nine_group_id],
            row_as_hash_of_data[:two_twenty_nine_parent_type],
            row_as_hash_of_data[:two_twenty_nine_parent_id],
            row_as_hash_of_data[:compliance_parameter_category],
            row_as_hash_of_data[:compliance_parameter_name],
            row_as_hash_of_data[:compliance_parameter_value]
          ]
        }
  end

    # GenerateCsvOfCompParamJson.write_csv_data(csv_data,'./output_comp_param.csv')
    # # Write CSV data to a file
  end


  def test_set_comp_param_json_from_csv_data


    csv_data = GenerateCsvOfCompParamJson.produce_csv_data(@empty_cp_json)


    csv_row_of_perimeter_zn_one = csv_data.find { |csv_row_data| csv_row_data[:two_twenty_nine_group_id].downcase == "PERIMETER_ZN_1".downcase &&
      csv_row_data[:compliance_parameter_name].downcase == "aggregation_factor" }

    csv_row_of_perimeter_zn_one[:compliance_parameter_value] = 0.5

    #binding.pry
    updated_cp_json = GenerateCsvOfCompParamJson.set_comp_param_json_from_csv_data(@empty_cp_json,csv_data)

    csv_row_of_perimeter_zn_one_updated = GenerateCsvOfCompParamJson.find_by_id(updated_cp_json, "PERIMETER_ZN_1".downcase)


    assert_equal 0.5, csv_row_of_perimeter_zn_one_updated["aggregation_factor"]



    # # Set the path to the JSON file
    # # Read and parse the JSON file
    # #
    # #File.write('./output_with_parent.json', JSON.pretty_generate(@rpd))

    # # Define required compliance parameters
    # # # Initialize CSV data
    # csv_data = GenerateCsvOfCompParamJson.produce_csv_data(@rpd)

    # GenerateCsvOfCompParamJson.write_csv_data(csv_data,'./output_comp_param.csv')
    # # Write CSV data to a file
  end

end
