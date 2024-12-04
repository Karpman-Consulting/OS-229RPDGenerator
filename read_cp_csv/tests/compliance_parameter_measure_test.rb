# insert your copyright here

require 'openstudio'
require 'openstudio/measure/ShowRunnerOutput'
require 'minitest/autorun'
require_relative '../measure.rb'
require 'fileutils'

class ReadComplianceParameterCsvFromOsmTest < Minitest::Test

  def number_of_arguments_and_argument_names
    # TODO
    measure = ReadComplianceParameterCsvFromOsm.new

    # make an empty model
    model = OpenStudio::Model::Model.new

    arguments = measure.arguments(model)
    assert_equal(3, arguments.size)
  end

  def bad_argument_values
    # create an instance of the measure
    measure = ReadComplianceParameterCsvFromOsm.new

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
    args_hash['csv_file_path'] = ''

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
    measure = ReadComplianceParameterCsvFromOsm.new

    # create runner with empty OSW
    osw = OpenStudio::WorkflowJSON.new
    runner = OpenStudio::Measure::OSRunner.new(osw)

    arguments = measure.arguments
    argument_map = OpenStudio::Measure.convertOSArgumentVectorToMap(arguments)

    # create hash of argument values.
    # If the argument has a default that you want to use, you don't need it in the hash
    args_hash = {}
    args_hash['osm_file_path'] = "#{File.dirname(__FILE__)}/../test_files/ASHRAE901_OfficeSmall_STD2019_Denver.osm"
    args_hash['empty_comp_param_json_file_path'] = "#{File.dirname(__FILE__)}/ASHRAE901_OfficeSmall_STD2019_Denver.comp-param-empty.json"
    args_hash['updated_comp_param_json_file_path'] = "#{File.dirname(__FILE__)}/ASHRAE901_OfficeSmall_STD2019_Denver.comp-param-updated_success.json"
    args_hash['csv_file_path'] = "#{File.dirname(__FILE__)}/ASHRAE901_OfficeSmall_STD2019_Denver.osm-empty.csv"
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
    measure.run(OpenStudio::Model::Model.new, runner, argument_map)
    result = runner.result

    # show the output
    show_output(result)

    # assert that it ran correctly
    assert_equal('Success', result.value.valueName)
  end

  def test_good_argument_values_bad_csv
    # create an instance of the measure
    measure = ReadComplianceParameterCsvFromOsm.new

    # create runner with empty OSW
    osw = OpenStudio::WorkflowJSON.new
    runner = OpenStudio::Measure::OSRunner.new(osw)

    arguments = measure.arguments
    argument_map = OpenStudio::Measure.convertOSArgumentVectorToMap(arguments)

    # create hash of argument values.
    # If the argument has a default that you want to use, you don't need it in the hash
    args_hash = {}
    args_hash['osm_file_path'] = "#{File.dirname(__FILE__)}/../test_files/ASHRAE901_OfficeSmall_STD2019_Denver.osm"
    args_hash['updated_comp_param_json_file_path'] = "#{File.dirname(__FILE__)}/ASHRAE901_OfficeSmall_STD2019_Denver.comp-param-updated.json"
    args_hash['empty_comp_param_json_file_path'] = "#{File.dirname(__FILE__)}/ASHRAE901_OfficeSmall_STD2019_Denver.comp-param-empty.json"
    args_hash['csv_file_path'] = "#{File.dirname(__FILE__)}/ASHRAE901_OfficeSmall_STD2019_Denver.osm-empty_bad.csv"
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
    measure.run(OpenStudio::Model::Model.new, runner, argument_map)
    result = runner.result

    # show the output
    show_output(result)


    # assert that it ran correctly
    assert_equal('Fail', result.value.valueName)
  end
end
