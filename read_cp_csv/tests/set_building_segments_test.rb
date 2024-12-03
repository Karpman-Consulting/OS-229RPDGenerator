require 'openstudio'
require_relative '../set_building_segments'
require_relative '../measure'
require 'minitest/autorun'
require 'pry-byebug'

class SetBuildingSegementsTest < Minitest::Test

  def test_parse_csv_with_multiple_building_segments

    # create an instance of a runner
    runner = OpenStudio::Measure::OSRunner.new(OpenStudio::WorkflowJSON.new)

    csv_file_path = File.join(File.dirname(File.realpath(__FILE__)), 'comp_param_two_building_segments.csv')

    empty_comp_param_json_file_path = File.join(File.dirname(File.realpath(__FILE__)), 'ASHRAE901_OfficeSmall_STD2019_Denver.comp-param-empty.json')

    comp_param_json = JSON.parse(File.read(empty_comp_param_json_file_path))

    parsed_csv = ReadComplianceParameterCsvFromOsm.read_comp_param_csv_data(csv_file_path,runner)

    updated_comp_param_json = SetBuildingSegements.read_csv_and_set_building_segments_in_comp_param_json(parsed_csv,comp_param_json)

    assert updated_comp_param_json.dig("ruleset_model_descriptions", 0, "buildings", 0, "building_segments").length == 2

    assert updated_comp_param_json.dig("ruleset_model_descriptions", 0, "buildings", 0, "building_segments")
    .find { |segment| segment["id"] == "segment 1" }["heating_ventilating_air_conditioning_systems"].length == 3

    assert updated_comp_param_json.dig("ruleset_model_descriptions", 0, "buildings", 0, "building_segments")
    .find { |segment| segment["id"] == "segment 1" }["zones"].length == 3

    assert updated_comp_param_json.dig("ruleset_model_descriptions", 0, "buildings", 0, "building_segments")
    .find { |segment| segment["id"] == "segment 2" }["heating_ventilating_air_conditioning_systems"].length == 2

    assert updated_comp_param_json.dig("ruleset_model_descriptions", 0, "buildings", 0, "building_segments")
    .find { |segment| segment["id"] == "segment 2" }["zones"].length == 3

    assert updated_comp_param_json.dig("ruleset_model_descriptions", 0, "buildings", 0, "building_segments")
    .find { |segment| segment["id"] == "segment 2" }["heating_ventilating_air_conditioning_systems"].first["id"] == "PSZ-AC:4"

    assert updated_comp_param_json.dig("ruleset_model_descriptions", 0, "buildings", 0, "building_segments")
    .find { |segment| segment["id"] == "segment 2" }["zones"].first["id"] == "PERIMETER_ZN_2"

  end
end
