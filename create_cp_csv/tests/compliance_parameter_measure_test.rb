# insert your copyright here

require 'openstudio'
require 'openstudio/measure/ShowRunnerOutput'
require 'minitest/autorun'
require_relative '../measure.rb'
require 'fileutils'

class CreateComplianceParameterCsvFromOsmTest < Minitest::Test

  def number_of_arguments_and_argument_names
    # TODO
    measure = NewMeasure.new

    # make an empty model
    model = OpenStudio::Model::Model.new

    # get arguments and test that they are what we are expecting
    arguments = measure.arguments(model)
    assert_equal(1, arguments.size)
    assert_equal('model_name', arguments[0].name)
  end

  def bad_argument_values
    # create an instance of the measure
    measure = CreateComplianceParameterCsvFromOsm.new

    # create runner with empty OSW
    osw = OpenStudio::WorkflowJSON.new
    runner = OpenStudio::Measure::OSRunner.new(osw)

    # make an empty model
    model = OpenStudio::Model::Model.new

    # get arguments
    arguments = measure.arguments(model)
    argument_map = OpenStudio::Measure.convertOSArgumentVectorToMap(arguments)

    # create hash of argument values
    args_hash = {}
    args_hash['osm_file_path'] = ''

    # populate argument with specified hash value if specified
    arguments.each do |arg|
      temp_arg_var = arg.clone
      if args_hash.key?(arg.name)
        assert(temp_arg_var.setValue(args_hash[arg.name]))
      end
      argument_map[arg.name] = temp_arg_var
    end

    # run the measure
    measure.run(model, runner, argument_map)
    result = runner.result

    # show the output
    show_output(result)

    # assert that it ran correctly
    assert_equal('Fail', result.value.valueName)
  end

  def test_good_argument_values
    # create an instance of the measure
    measure = CreateComplianceParameterCsvFromOsm.new

    # create runner with empty OSW
    osw = OpenStudio::WorkflowJSON.new
    runner = OpenStudio::Measure::OSRunner.new(osw)

    # load the test model
    translator = OpenStudio::OSVersion::VersionTranslator.new
    path = "#{File.dirname(__FILE__)}/example_model.osm"
    model = translator.loadModel(path)
    assert(!model.empty?)
    model = model.get

    # get arguments
    arguments = measure.arguments(model)
    argument_map = OpenStudio::Measure.convertOSArgumentVectorToMap(arguments)

    # create hash of argument values.
    # If the argument has a default that you want to use, you don't need it in the hash
    args_hash = {}
    args_hash['osm_file_path'] = "#{File.dirname(__FILE__)}/example_model.osm"
    # using defaults values from measure.rb for other arguments

    # populate argument with specified hash value if specified
    arguments.each do |arg|
      temp_arg_var = arg.clone
      if args_hash.key?(arg.name)
        assert(temp_arg_var.setValue(args_hash[arg.name]))
      end
      argument_map[arg.name] = temp_arg_var
    end

    # run the measure
    measure.run(model, runner, argument_map)
    result = runner.result

    # show the output
    show_output(result)

    # assert that it ran correctly
    assert_equal('Success', result.value.valueName)
  end
end


class CreateComplianceParameterCsvFromOsmTestMethods < Minitest::Test

  def setup

    path = OpenStudio::Path.new('./example_model.osm')

    path_bad_values = OpenStudio::Path.new('./example_model_with_bad_values.osm')

    translator = OpenStudio::OSVersion::VersionTranslator.new

    @model = translator.loadModel(path).get

    translator2 = OpenStudio::OSVersion::VersionTranslator.new

    @model_bad_values = translator2.loadModel(path_bad_values).get

  end

  def test_get_object_type_of_additional_property

    additional_properties = @model.getAdditionalPropertiess.select { |ap| ap.hasFeature("is_compliance_parameter_90_1_2019_prm") }

    zone_infiltration_object = additional_properties.find { |ap| ap.handle.to_s == '{b0c16963-bf29-4919-9474-4e647b365c22}' }

    #a_additional_property = additional_properties.first

    # With no model object for additional properties (not sure if this is possible?)

    print(CreateComplianceParameterCsvFromOsm.get_object_type_of_additional_property(zone_infiltration_object))

    assert_equal 'OS:Space', CreateComplianceParameterCsvFromOsm.get_object_type_of_additional_property(zone_infiltration_object)

    assert_equal 'Zone.Infiltration',CreateComplianceParameterCsvFromOsm.get_additional_property_feature_value(zone_infiltration_object,'compliance_parameter_category')

    assert_equal 'measured_air_leakage_rate',CreateComplianceParameterCsvFromOsm.get_additional_property_feature_value(zone_infiltration_object,'compliance_parameter_name')

    assert_equal 22,CreateComplianceParameterCsvFromOsm.get_additional_property_feature_value(zone_infiltration_object,'compliance_parameter_value')

  end

  def test_get_additional_property_empty_value
    ### This Additional properties shoudl return an empty value for compliance_parameter_value
    # OS:AdditionalProperties,
    # {b0c16963-bf29-4919-9474-4e647b365c23}, !- Handle
    # {30fea77d-d1c6-417c-9fd9-e5ee4bea434a}, !- Object Name
    # is_compliance_parameter_90_1_2019_prm,        !- Feature Name 1
    # Boolean,                                 !- Feature Data Type 1
    # true,                     !- Feature Value 1
    # compliance_parameter_category,        !- Feature Name 2
    # String,                                 !- Feature Data Type 2
    # Zone.Infiltration,                   !- Feature Value 2
    # compliance_parameter_name,        !- Feature Name 3
    # String,                                 !- Feature Data Type 3
    # measured_air_leakage_rate, !- Feature Value 3
    # compliance_parameter_value,        !- Feature Name 4
    # Double,                                 !- Feature Data Type 4
    # ;                     !- Feature Value 4

    additional_properties = @model.getAdditionalPropertiess.select { |ap| ap.hasFeature("is_compliance_parameter_90_1_2019_prm") }

    zone_infiltration_object_no_value = additional_properties.find { |ap| ap.handle.to_s == '{b0c16963-bf29-4919-9474-4e647b365c23}' }

    assert_equal 'OS:Space', CreateComplianceParameterCsvFromOsm.get_object_type_of_additional_property(zone_infiltration_object_no_value)

    assert_equal 'Zone.Infiltration',CreateComplianceParameterCsvFromOsm.get_additional_property_feature_value(zone_infiltration_object_no_value,'compliance_parameter_category')

    assert_equal 'measured_air_leakage_rate',CreateComplianceParameterCsvFromOsm.get_additional_property_feature_value(zone_infiltration_object_no_value,'compliance_parameter_name')

    assert_equal "",CreateComplianceParameterCsvFromOsm.get_additional_property_feature_value(zone_infiltration_object_no_value,'compliance_parameter_value')
  end

  def test_get_additional_property_no_value
    ### Shoudl throw an error as compliance_parameter_value is not defined
    #   OS:AdditionalProperties,
    # {b0c16963-bf29-4919-9474-4e647b365c24}, !- Handle
    # {1c7487fe-94e4-4b4b-924e-bc15951fc750}, !- Object Name
    # is_compliance_parameter_90_1_2019_prm,        !- Feature Name 1
    # Boolean,                                 !- Feature Data Type 1
    # true,                     !- Feature Value 1
    # compliance_parameter_category,        !- Feature Name 2
    # String,                                 !- Feature Data Type 2
    # Zone.Infiltration,                   !- Feature Value 2
    # compliance_parameter_name,        !- Feature Name 3
    # String,                                 !- Feature Data Type 3
    # measured_air_leakage_rate; !- Feature Value 3

    additional_properties = @model_bad_values.getAdditionalPropertiess.select { |ap| ap.hasFeature("is_compliance_parameter_90_1_2019_prm") }

    zone_infiltration_object_no_value = additional_properties.find { |ap| ap.handle.to_s == '{b0c16963-bf29-4919-9474-4e647b365c24}' }

    assert_equal 'OS:Space', CreateComplianceParameterCsvFromOsm.get_object_type_of_additional_property(zone_infiltration_object_no_value)

    assert_equal 'Zone.Infiltration',CreateComplianceParameterCsvFromOsm.get_additional_property_feature_value(zone_infiltration_object_no_value,'compliance_parameter_category')

    assert_equal 'measured_air_leakage_rate',CreateComplianceParameterCsvFromOsm.get_additional_property_feature_value(zone_infiltration_object_no_value,'compliance_parameter_name')

    error = assert_raises(RuntimeError) do
      CreateComplianceParameterCsvFromOsm.get_additional_property_feature_value(zone_infiltration_object_no_value,'compliance_parameter_value')
    end

    assert_equal "Feature compliance_parameter_value not found in on additional property with handle {b0c16963-bf29-4919-9474-4e647b365c24} and object aim0640",
     error.message

  end

end
