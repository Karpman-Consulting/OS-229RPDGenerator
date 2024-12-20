# insert your copyright here

# see the URL below for information on how to write OpenStudio measures
# http://nrel.github.io/OpenStudio-user-documentation/reference/measure_writing_guide/

# start the measure
class CreatePreconditionedIdf < OpenStudio::Measure::ModelMeasure
  # human readable name
  def name
    # Measure name should be the title case of the class name.
    return 'CreatePreconditionedIdf'
  end

  # human readable description
  def description
    return 'Create pre conditioned idf.'
  end

  # human readable description of modeling approach
  def modeler_description
    return 'Create pre conditioned idf'
  end

  # define the arguments that the user will input
  def arguments(model)
    args = OpenStudio::Measure::OSArgumentVector.new
    return args
  end

  def self.set_output_json_to_true(workspace)
    if workspace.outputJSON.is_initialized
      workspace.getOutputJSON.setOutputJSON(true)
    end
  end

  def self.add_output_table_summary_report(workspace)
    if not workspace.getOptionalOutputTableSummaryReports.is_initialized or
      not workspace.getOutputTableSummaryReports.summaryReports.include? "AllSummaryAndMonthly"
      workspace.getOutputTableSummaryReports.removeAllSummaryReports

      workspace.getOutputTableSummaryReports.addSummaryReport("AllSummaryAndMonthly")
    end
  end

  def self.set_output_variable_schedule_hourly(model)

    outputVariable = model.getOutputVariables.find { |output_variable| output_variable.variableName() == 'Schedule Value' }

    if outputVariable.nil?
      outputVariable = OpenStudio::Model::OutputVariable.new('Schedule Value', model)
    end

    outputVariable.setReportingFrequency('Hourly')
    outputVariable.setKeyValue('*')

  end

  # define what happens when the measure is run
  def run(model, runner, user_arguments)
    super(model, runner, user_arguments)

    # use the built-in error checking
    if !runner.validateUserArguments(arguments(model), user_arguments)
      return false
    end

    CreatePreconditionedIdf.set_output_json_to_true(model)

    CreatePreconditionedIdf.add_output_table_summary_report(model)

    CreatePreconditionedIdf.set_output_variable_schedule_hourly(model)

    runner.registerFinalCondition("Successfully added EnergyPlus outputs required for 229 compliance parameters")

    return true
  end
end

# register the measure to be used by the application
CreatePreconditionedIdf.new.registerWithApplication
