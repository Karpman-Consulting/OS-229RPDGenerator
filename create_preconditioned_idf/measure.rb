# insert your copyright here

# see the URL below for information on how to write OpenStudio measures
# http://nrel.github.io/OpenStudio-user-documentation/reference/measure_writing_guide/

# start the measure
class CreatePreconditionedIdf < OpenStudio::Measure::EnergyPlusMeasure
  # human readable name
  def name
    # Measure name should be the title case of the class name.
    return 'Create pre conditioned idf'
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
    osm_file_path = OpenStudio::Measure::OSArgument.makeStringArgument('osm_file_path', true)
    osm_file_path.setDisplayName('Osm file path')
    osm_file_path.setDescription('Osm file path')
    osm_file_path.setDefaultValue('')
    args << osm_file_path
    return args
  end

  def self.set_output_table_style(workspace)

    output_control_table = workspace.getObjectsByType('OutputControl:Table:Style'.to_IddObjectType)

    if output_control_table.empty?
      new_output_schedule = "
        OutputControl:Table:Style,
          HTML,                    !- Column Separator
          None;                    !- Unit Conversion
      "

      idfObject = OpenStudio::IdfObject.load(new_output_schedule)
      object = idfObject.get

      workspace.addObject(object)
    else
      output_control_table.first.setString(1, 'None')
    end

  end

  def self.add_output_table_summary_report(workspace)
    if not workspace.getOptionalOutputTableSummaryReports.is_initialized or
      not workspace.getOutputTableSummaryReports.summaryReports.include? "AllSummaryAndMonthly"

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

  def self.set_output_json_to_true(workspace)

    if not workspace.outputJSON.is_initialized
      output_table_summary_report = "
        Output:JSON,
          TimeSeriesAndTabular,                   !- Option Type
          Yes,                                    !- Output JSON
          No,                                     !- Output CBOR
          No;                                     !- Output MessagePack
      "

      idfObject = OpenStudio::IdfObject.load(output_table_summary_report)
      object = idfObject.get

      workspace.addObject(object)
    else
      workspace.getOutputJSON.setOutputJSON(true)
    end

  end

  def self.set_output_schedules(workspace)

    output_schedules = workspace.getObjectsByType('Output:Schedules'.to_IddObjectType)

    if output_schedules.empty?
      new_output_schedule = "
        Output:Schedules,
        Hourly;                  !- Key Field
      "

      idfObject = OpenStudio::IdfObject.load(new_output_schedule)
      object = idfObject.get

      workspace.addObject(object)
    else
      output_schedules.first.setString(0, 'Hourly')
    end
  end

  # define what happens when the measure is run
  def run(model, runner, user_arguments)
    super(model, runner, user_arguments)

    # use the built-in error checking
    if !runner.validateUserArguments(arguments(model), user_arguments)
      return false
    end

    CreatePreconditionedIdf.add_output_table_summary_report(model)

    CreatePreconditionedIdf.set_output_variable_schedule_hourly(model)

    CreatePreconditionedIdf.set_output_json_to_true(model)

    CreatePreconditionedIdf.set_output_schedules(model)

    CreatePreconditionedIdf.set_output_table_style(model)

    runner.registerInitialCondition("Added reports required for 229")

    return true
  end
end

# register the measure to be used by the application
CreatePreconditionedIdf.new.registerWithApplication
