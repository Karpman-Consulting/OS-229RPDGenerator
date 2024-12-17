# insert your copyright here

require 'openstudio'
require 'openstudio/measure/ShowRunnerOutput'
require 'minitest/autorun'
require_relative '../measure.rb'
require 'fileutils'

class CreateComplianceParameterCsvFromOsmTest < Minitest::Test

  def number_of_arguments_and_argument_names
    # TODO
    measure = CreateComplianceParameterCsvFromOsm.new

    # make an empty model
    model = OpenStudio::Model::Model.new

    arguments = measure.arguments(model)
    assert_equal(2, arguments.size)
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
    args_hash['blah'] = ''

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

    arguments = measure.arguments
    argument_map = OpenStudio::Measure.convertOSArgumentVectorToMap(arguments)

    test_file = "#{File.dirname(__FILE__)}/../../test_files/ASHRAE901_OfficeSmall_STD2019_Denver.osm"

    unless File.exist?(test_file)
      # download the test files if they are not present
      raise "Could #{test_file} not found "
    end

    translator = OpenStudio::OSVersion::VersionTranslator.new
    path = OpenStudio::Path.new(test_file)
    model = translator.loadModel(path)
    assert((not model.empty?))
    model = model.get

    # create hash of argument values.
    # If the argument has a default that you want to use, you don't need it in the hash
    args_hash = {}
    #args_hash['osm_file_path'] = test_file
    args_hash['output_csv_file_path'] = "#{File.dirname(__FILE__)}/ASHRAE901_OfficeSmall_STD2019_Denver.csv"
    args_hash['empty_comp_param_json_file_path'] = "#{File.dirname(__FILE__)}/ASHRAE901_OfficeSmall_STD2019_Denver.comp-param-empty.json"
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
