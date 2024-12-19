# insert your copyright here

require 'openstudio'
require 'openstudio/measure/ShowRunnerOutput'
require 'minitest/autorun'
require_relative '../measure.rb'
require 'fileutils'
require 'pry-byebug'

class CreatePreconditionedIdfTest < Minitest::Test

  def setup

    translator = OpenStudio::OSVersion::VersionTranslator.new
    path = "#{File.dirname(__FILE__)}/example_model_all_required_outputs.osm"
    model = translator.loadModel(path)
    assert(!model.empty?)
    @model_with_outputs = model.get


    translator = OpenStudio::OSVersion::VersionTranslator.new
    path = "#{File.dirname(__FILE__)}/Test_E1.osm"
    model = translator.loadModel(path)
    assert(!model.empty?)
    @empty_model = model.get

    @empty_model = OpenStudio::Model::Model.new

  end

  def test_add_output_table_summary_report

    CreatePreconditionedIdf.add_output_table_summary_report(@model_with_outputs)

    assert @model_with_outputs.getOutputTableSummaryReports.summaryReports.include? "AllSummaryAndMonthly"

    CreatePreconditionedIdf.add_output_table_summary_report(@empty_model)

    assert @empty_model.getOutputTableSummaryReports.summaryReports.include? "AllSummaryAndMonthly"
  end

  def test_set_output_variable_schedule_hourly

    CreatePreconditionedIdf.set_output_variable_schedule_hourly(@model_with_outputs)

    outputVariable = @model_with_outputs.getOutputVariables.find { |output_variable| output_variable.variableName() == 'Schedule Value' }

    assert_equal '*', outputVariable.keyValue
    assert_equal 'Hourly', outputVariable.reportingFrequency

    CreatePreconditionedIdf.set_output_variable_schedule_hourly(@empty_model)

    outputVariable = @empty_model.getOutputVariables.find { |output_variable| output_variable.variableName() == 'Schedule Value' }

    assert_equal '*', outputVariable.keyValue
    assert_equal 'Hourly', outputVariable.reportingFrequency
  end

  # def test_write_out_idf_from_empty_model
  #   # create an instance of the measure
  #   measure = CreatePreconditionedIdf.new

  #   # create runner with empty OSW
  #   osw = OpenStudio::WorkflowJSON.new
  #   runner = OpenStudio::Measure::OSRunner.new(osw)

  #   model = OpenStudio::Model::Model.new

  #   # get arguments
  #   arguments = measure.arguments(model)
  #   argument_map = OpenStudio::Measure.convertOSArgumentVectorToMap(arguments)

  #   # create hash of argument values.
  #   # If the argument has a default that you want to use, you don't need it in the hash
  #   args_hash = {}
  #   # using defaults values from measure.rb for other arguments
  #   #args_hash['osm_file_path'] = './empty_model.osm'
  #   # populate argument with specified hash value if specified
  #   arguments.each do |arg|
  #     temp_arg_var = arg.clone
  #     if args_hash.key?(arg.name)
  #       assert(temp_arg_var.setValue(args_hash[arg.name]))
  #     end
  #     argument_map[arg.name] = temp_arg_var
  #   end

  #   # run the measure
  #   measure.run(model, runner, argument_map)
  #   result = runner.result

  #   assert_equal('success', result.value.valueName.downcase)

  #   assert model.getObjectsByType('Output:Schedules'.to_IddObjectType).first.getString(0).get, 'Hourly'

  #   assert model.getOutputJSON.outputJSON, true

  #   outputVariable = model.getOutputVariables.find { |output_variable| output_variable.variableName() == 'Schedule Value' }

  #   assert '*', outputVariable.keyValue
  #   assert 'Hourly', outputVariable.reportingFrequency

  #   assert model.getOutputTableSummaryReports.summaryReports.include? "AllSummaryAndMonthly"

  #   assert model.getObjectsByType('OutputControl:Table:Style'.to_IddObjectType).first.getString(1).get, "None"

  #   model.save('empty_model_with_output.osm', true)

  #   translator = OpenStudio::EnergyPlus::ForwardTranslator.new
  #   idf = translator.translateModel(model)
  #   idf.save(OpenStudio::Path.new('empty_model_with_output.idf'), true)

  # end

  # def test_write_out_idf_from_existing_model
  #   # create an instance of the measure
  #   measure = CreatePreconditionedIdf.new

  #   # create runner with empty OSW
  #   osw = OpenStudio::WorkflowJSON.new
  #   runner = OpenStudio::Measure::OSRunner.new(osw)

  #   model = @model_with_outputs

  #   # get arguments
  #   arguments = measure.arguments(model)
  #   argument_map = OpenStudio::Measure.convertOSArgumentVectorToMap(arguments)

  #   # create hash of argument values.
  #   # If the argument has a default that you want to use, you don't need it in the hash
  #   args_hash = {}
  #   # using defaults values from measure.rb for other arguments
  #   #args_hash['osm_file_path'] = './empty_model.osm'
  #   # populate argument with specified hash value if specified
  #   arguments.each do |arg|
  #     temp_arg_var = arg.clone
  #     if args_hash.key?(arg.name)
  #       assert(temp_arg_var.setValue(args_hash[arg.name]))
  #     end
  #     argument_map[arg.name] = temp_arg_var
  #   end

  #   # run the measure
  #   measure.run(model, runner, argument_map)
  #   result = runner.result

  #   assert_equal('success', result.value.valueName.downcase)

  #   assert model.getObjectsByType('Output:Schedules'.to_IddObjectType).first.getString(0).get, 'Hourly'

  #   assert model.getOutputJSON.outputJSON, true

  #   outputVariable = model.getOutputVariables.find { |output_variable| output_variable.variableName() == 'Schedule Value' }

  #   assert '*', outputVariable.keyValue
  #   assert 'Hourly', outputVariable.reportingFrequency

  #   assert model.getOutputTableSummaryReports.summaryReports.include? "AllSummaryAndMonthly"

  #   assert model.getObjectsByType('OutputControl:Table:Style'.to_IddObjectType).first.getString(1).get, "None"

  #   model.save('existing_model_with_output.osm', true)

  #   translator = OpenStudio::EnergyPlus::ForwardTranslator.new
  #   idf = translator.translateModel(model)
  #   idf.save(OpenStudio::Path.new('existing_model_with_output.idf'), true)

  # end
end
