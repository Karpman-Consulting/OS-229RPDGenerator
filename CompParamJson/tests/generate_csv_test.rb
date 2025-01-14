require 'minitest/autorun'
require_relative '../generate_csv'

class GenerateCsvDataTest < Minitest::Test

  ## TODO write tests for generate_csv
  def setup

    @empty_cp_json_file_path = File.join(File.dirname(File.realpath(__FILE__)), 'ASHRAE901_OfficeSmall_STD2019_Denver.comp-param-empty.json')

    @empty_cp_json = JSON.parse(File.read(@empty_cp_json_file_path))

    @empty_cp_json_file_path_e1 = File.join(File.dirname(File.realpath(__FILE__)), '229_E1.comp-param-empty.json')

    @empty_cp_json_e1 = JSON.parse(File.read(@empty_cp_json_file_path_e1))
  end

  def test_generate_comp_param_empty_csv
    ## Writes out csv for inspection
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

  end


  def test_comp_param_json_to_csv_data


    csv_data = GenerateTwoTwoNineCompParamJsonCsv.produce_csv_data_from_comp_param_json(@empty_cp_json)

    new_status_type_two = "a_test_of_status_type_update2"

    new_zone_aggregation_factor = 0.7

    zn_two_wall_east_window_four_updated_framing_type = "a_test_of_framing_type_update"

    ### Update zone aggreation factor for PERIMETER_ZN_1
    #
    csv_row_of_climate_zone = csv_data.find { |csv_row_data| csv_row_data[:compliance_parameter_name].downcase == "climate_zone".downcase }

    csv_row_of_climate_zone[:compliance_parameter_value] = "CZ_111"

    csv_row_of_perimeter_zn_one_ag_factor = csv_data.find { |csv_row_data| csv_row_data[:two_twenty_nine_group_id].downcase == "PERIMETER_ZN_1".downcase &&
    csv_row_data[:compliance_parameter_name].downcase == "aggregation_factor" }

    csv_row_of_perimeter_zn_one_ag_factor[:compliance_parameter_value] = new_zone_aggregation_factor

    ### Update PSZ-AC:3

    csv_row_of_psz_ac_3 = csv_data.select { |csv_row_data| csv_row_data[:two_twenty_nine_group_id] == "PSZ-AC:3" &&
    csv_row_data[:compliance_parameter_name].downcase == "status_type" }

    assert !csv_row_of_psz_ac_3.empty?
    ## In this case there are multiple complilance parameter values
    csv_row_of_psz_ac_3.each do |row|
      row[:compliance_parameter_value] = new_status_type_two
    end

    csv_row_of_psz_ac_3_fan = csv_data.find { |csv_row_data| csv_row_data[:two_twenty_nine_group_id] == "PSZ-AC:3 FAN-fansystem" &&
    csv_row_data[:compliance_parameter_name].downcase == "air_filter_merv_rating" }

    assert !csv_row_of_psz_ac_3_fan.nil?

    csv_row_of_psz_ac_3_fan[:compliance_parameter_value] = 'new_fan_system_air_filter_merv_rating'

    ### Update PERIMETER_ZN_2_WALL_EAST_WINDOW_4 framing_type

    csv_row_of_zn_two_wall_east_window_four_framing_type = csv_data.find { |csv_row_data| csv_row_data[:two_twenty_nine_group_id].downcase == "PERIMETER_ZN_2_WALL_EAST_WINDOW_4".downcase &&
    csv_row_data[:compliance_parameter_name].downcase == "framing_type" }

    ###

    csv_row_of_zn_two_wall_east_window_four_framing_type[:compliance_parameter_value] = zn_two_wall_east_window_four_updated_framing_type

    measured_air_leakage_rates = csv_data.select { |csv_row_data| csv_row_data[:compliance_parameter_name] == "measured_air_leakage_rate" }

    measured_air_leakage_rates.each do |row|
      row[:compliance_parameter_value] = 9.999
    end

    csv_row_of_zn_two_wall_east_window_four_framing_type[:compliance_parameter_value] = zn_two_wall_east_window_four_updated_framing_type

    ### Run the code
    updated_cp_json = GenerateTwoTwoNineCompParamJsonCsv.set_comp_param_json_from_csv_data(@empty_cp_json,csv_data)

    assert_equal "CZ_111" ,updated_cp_json.dig('weather',"climate_zone")

    assert_equal updated_cp_json.dig("ruleset_model_descriptions", 0, "buildings", 0, "building_segments",0,"zones").first["infiltration"]["measured_air_leakage_rate"], 9.999

    csv_row_of_perimeter_zn_one_updated = GenerateTwoTwoNineCompParamJsonCsv.find_by_id(updated_cp_json, "PERIMETER_ZN_1".downcase)

    assert_equal new_zone_aggregation_factor, csv_row_of_perimeter_zn_one_updated["aggregation_factor"]

    csv_row_of_psz_ac_3_updated = GenerateTwoTwoNineCompParamJsonCsv.find_by_id(updated_cp_json, "PSZ-AC:3")

    assert_equal new_status_type_two, csv_row_of_psz_ac_3_updated["status_type"]

    csv_row_of_asz_ac_fan = GenerateTwoTwoNineCompParamJsonCsv.find_by_id(updated_cp_json, "PSZ-AC:3 FAN-fansystem")

    assert_equal 'new_fan_system_air_filter_merv_rating', csv_row_of_asz_ac_fan['air_filter_merv_rating']

    zn_two_wall_east_window_four = GenerateTwoTwoNineCompParamJsonCsv.find_by_id(updated_cp_json, "PERIMETER_ZN_2_WALL_EAST_WINDOW_4".downcase)

    assert_equal zn_two_wall_east_window_four_updated_framing_type, zn_two_wall_east_window_four["framing_type"]

  end

  def test_comp_param_json_to_csv_data_e1

    csv_data = GenerateTwoTwoNineCompParamJsonCsv.produce_csv_data_from_comp_param_json(@empty_cp_json_e1)

    assert csv_data.length > 0

  end

end
