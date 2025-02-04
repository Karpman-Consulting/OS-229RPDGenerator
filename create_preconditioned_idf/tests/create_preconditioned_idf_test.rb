# insert your copyright here

require 'openstudio'
require 'openstudio/measure/ShowRunnerOutput'
require 'minitest/autorun'
require_relative '../measure.rb'
require 'fileutils'


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

end
