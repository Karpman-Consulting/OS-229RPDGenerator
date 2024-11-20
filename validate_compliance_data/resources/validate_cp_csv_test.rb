
require_relative './validate_cp_csv'
require 'pry-byebug'
require 'minitest/autorun'
require 'csv'

class ValidateCPCSVTest < Minitest::Test

  RULESET_MODEL_DESCRIPTION_SCHEMA_PATH = File.join(File.dirname(__FILE__), '..', '..','dependencies','ruleset-model-description-schema','docs229')

  def setup

    schema_path = File.join(RULESET_MODEL_DESCRIPTION_SCHEMA_PATH, 'ASHRAE229.schema.json')
    @json_229_schema = JSON.parse(File.read(schema_path))['definitions']
  end


  # def test_validate_csv_cp


  #   csv_to_validate = CSV.read("#{File.dirname(__FILE__)}/example_model.osm-empty_for_test.csv")[1..]

  #   ValidateCPCSV.validate_csv_cp_complete(csv_to_validate)


  # end

  # def test_get_nested_compliance_parameter


  #   ruleset_category = 'Zone.Infiltration'
  #   compliance_parameter_name = 'measured_air_leakage_rate'

  #   ValidateCPCSV.get_nested_compliance_parameter(ruleset_category,compliance_parameter_name,@json_229_schema)
  # end

  def test_build_compliance_parameter_value_array_path

    ruleset_category = 'Zone.Infiltration'
    compliance_parameter_name = 'measured_air_leakage_rate'

    value = ValidateCPCSV.get_compliance_parameter_value(ruleset_category,compliance_parameter_name,@json_229_schema)



  end


  # def test_build_compliance_parameter_value_array_path

  #   ruleset_category = 'Zone.Infiltration'
  #   compliance_parameter_name = 'measured_air_leakage_rate'

  #   array_path = ValidateCPCSV.build_compliance_parameter_value_array_path(ruleset_category,compliance_parameter_name)


  #   assert_equal array_path,["Zone", "properties", "Infiltration", "measured_air_leakage_rate"]
  # end

end
