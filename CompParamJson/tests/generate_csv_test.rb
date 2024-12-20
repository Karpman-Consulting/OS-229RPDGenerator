require 'minitest/autorun'
require_relative '../generate_csv'
require 'pry-byebug'

class GenerateCsvDataTest < Minitest::Test

  ## TODO write tests for generate_csv
  def setup

    @empty_cp_json_file_path = File.join(File.dirname(File.realpath(__FILE__)), 'ASHRAE901_OfficeSmall_STD2019_Denver.comp-param-empty.json')

    @empty_cp_json = JSON.parse(File.read(@empty_cp_json_file_path))

    @empty_cp_json_file_path_e1 = File.join(File.dirname(File.realpath(__FILE__)), 'E1.comp-param-empty.json')

    @empty_cp_json_e1 = JSON.parse(File.read(@empty_cp_json_file_path_e1))
  end

  def test_generate_comp_param_empty_csv

    # # Set the path to the JSON file
    # # Read and parse the JSON file
    # #
    # #File.write('./output_with_parent.json', JSON.pretty_generate(@rpd))
    #
    csv_data = GenerateTwoTwoNineCompParamJsonCsv.produce_csv_data_from_comp_param_json(@empty_cp_json)

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


  def test_comp_param_json_to_csv_data


    csv_data = GenerateTwoTwoNineCompParamJsonCsv.produce_csv_data_from_comp_param_json(@empty_cp_json)

    new_status_type = "a_test_of_status_type_update"

    new_zone_aggregation_factor = 0.7

    zn_two_wall_east_window_four_updated_framing_type = "a_test_of_framing_type_update"

    ### Update zone aggreation factor for PERIMETER_ZN_1

    csv_row_of_perimeter_zn_one_ag_factor = csv_data.find { |csv_row_data| csv_row_data[:two_twenty_nine_group_id].downcase == "PERIMETER_ZN_1".downcase &&
    csv_row_data[:compliance_parameter_name].downcase == "aggregation_factor" }

    csv_row_of_perimeter_zn_one_ag_factor[:compliance_parameter_value] = new_zone_aggregation_factor

    ### Update PSZ-AC:3

    csv_row_of_psz_ac_3 = csv_data.find { |csv_row_data| csv_row_data[:two_twenty_nine_group_id].downcase == "PSZ-AC:3".downcase &&
    csv_row_data[:compliance_parameter_name].downcase == "status_type" }

    csv_row_of_psz_ac_3[:compliance_parameter_value] = new_status_type

    ### Update PERIMETER_ZN_2_WALL_EAST_WINDOW_4 framing_type

    csv_row_of_zn_two_wall_east_window_four_framing_type = csv_data.find { |csv_row_data| csv_row_data[:two_twenty_nine_group_id].downcase == "PERIMETER_ZN_2_WALL_EAST_WINDOW_4".downcase &&
    csv_row_data[:compliance_parameter_name].downcase == "framing_type" }

    csv_row_of_zn_two_wall_east_window_four_framing_type[:compliance_parameter_value] = zn_two_wall_east_window_four_updated_framing_type

    ### Run the code

    updated_cp_json = GenerateTwoTwoNineCompParamJsonCsv.set_comp_param_json_from_csv_data(@empty_cp_json,csv_data)

    csv_row_of_perimeter_zn_one_updated = GenerateTwoTwoNineCompParamJsonCsv.find_by_id(updated_cp_json, "PERIMETER_ZN_1".downcase)

    assert_equal new_zone_aggregation_factor, csv_row_of_perimeter_zn_one_updated["aggregation_factor"]

    csv_row_of_psz_ac_3_updated = GenerateTwoTwoNineCompParamJsonCsv.find_by_id(updated_cp_json, "PSZ-AC:3".downcase)

    assert_equal new_status_type, csv_row_of_psz_ac_3_updated["status_type"]

    zn_two_wall_east_window_four = GenerateTwoTwoNineCompParamJsonCsv.find_by_id(updated_cp_json, "PERIMETER_ZN_2_WALL_EAST_WINDOW_4".downcase)

    assert_equal zn_two_wall_east_window_four_updated_framing_type, zn_two_wall_east_window_four["framing_type"]

  end

  def test_comp_param_json_to_csv_data_e1

    csv_data = GenerateTwoTwoNineCompParamJsonCsv.produce_csv_data_from_comp_param_json(@empty_cp_json_e1)

    assert csv_data.length > 0

  end

end
