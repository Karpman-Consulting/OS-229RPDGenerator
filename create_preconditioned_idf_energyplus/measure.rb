# insert your copyright here

# see the URL below for information on how to write OpenStudio measures
# http://nrel.github.io/OpenStudio-user-documentation/reference/measure_writing_guide/

# start the measure
class CreatePreconditionedIdfEnergyPlus < OpenStudio::Measure::EnergyPlusMeasure
  # human readable name
  def name
    # Measure name should be the title case of the class name.
    return 'CreatePreconditionedIdfEnergyPlus'
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

  def self.set_output_json_to_true(workspace)

    output_control_table = workspace.getObjectsByType('Output:JSON'.to_IddObjectType)

    if output_control_table.empty?
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
      output_control_table = workspace.getObjectsByType('Output:JSON'.to_IddObjectType)
      output_control_table.first.setString(1, 'Yes')
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

    CreatePreconditionedIdfEnergyPlus.set_output_json_to_true(model)

    CreatePreconditionedIdfEnergyPlus.set_output_schedules(model)

    CreatePreconditionedIdfEnergyPlus.set_output_table_style(model)

    runner.registerFinalCondition("Successfully added EnergyPlus outputs required for 229 compliance parameters")

    return true
  end
end

# register the measure to be used by the application
CreatePreconditionedIdfEnergyPlus.new.registerWithApplication
