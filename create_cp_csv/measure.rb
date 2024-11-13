# insert your copyright here

# see the URL below for information on how to write OpenStudio measures
# http://nrel.github.io/OpenStudio-user-documentation/reference/measure_writing_guide/

# start the measure
class NewMeasure < OpenStudio::Measure::ModelMeasure
  # human readable name
  def name
    # Measure name should be the title case of the class name.
    return 'New Measure'
  end

  # human readable description
  def description
    return 'Replace this text with an explanation of what the measure does in terms that can be understood by a general building professional audience (building owners, architects, engineers, contractors, etc.).  This description will be used to create reports aimed at convincing the owner and/or design team to implement the measure in the actual building design.  For this reason, the description may include details about how the measure would be implemented, along with explanations of qualitative benefits associated with the measure.  It is good practice to include citations in the measure if the description is taken from a known source or if specific benefits are listed.'
  end

  # human readable description of modeling approach
  def modeler_description
    return 'Replace this text with an explanation for the energy modeler specifically.  It should explain how the measure is modeled, including any requirements about how the baseline model must be set up, major assumptions, citations of references to applicable modeling resources, etc.  The energy modeler should be able to read this description and understand what changes the measure is making to the model and why these changes are being made.  Because the Modeler Description is written for an expert audience, using common abbreviations for brevity is good practice.'
  end

  # define the arguments that the user will input
  def arguments(model)
    args = OpenStudio::Measure::OSArgumentVector.new

    # the name of the space to add to the model
    osm_file_path = OpenStudio::Measure::OSArgument.makeStringArgument('osm_file_path', true)
    osm_file_path.setDisplayName('Osm file path')
    osm_file_path.setDescription('Osm file path')
    args << osm_file_path

    output_csv_file_path = OpenStudio::Measure::OSArgument.makeStringArgument('output_csv_file_path', true)
    output_csv_file_path.setDisplayName('output csv file path')
    output_csv_file_path.setDescription('output csv file path')
    output_csv_file_path.setDefaultValue('output.csv')
    args << output_csv_file_path

    return args
  end

  # define what happens when the measure is run
  def run(model, runner, user_arguments)
    super(model, runner, user_arguments)  # Do **NOT** remove this line

    # use the built-in error checking
    if !runner.validateUserArguments(arguments(model), user_arguments)
      return false
    end

    # assign the user inputs to variables
    osm_file_path = runner.getStringArgumentValue('osm_file_path', user_arguments)

    # check the space_name for reasonableness
    if osm_file_path.nil? || osm_file_path.empty?
      runner.registerError('osm_file_path')
      return false
    end

    # report initial condition of model
    #
    #
    ##OpenStudio Measure pseudocode:

    # The measure will open the .osm file and search it for instances of “model objects” that are associated with compliance parameters. The search will be limited to OS Model objects associated with the compliance parameters listed in Appendix A

    # For each qualified parent object found, the measure will look for an attached OS:AdditionalProperties object. This is an extensible OS object that uses a “key, value” structure to attach “generic” data to specific objects within the OpenStudio data model.

    # When a pre-existing value for a compliance parameter is found, it will be written (pre-populated) in the ‘parameter value’ cell of the row of the .csv file. If a value for the compliance parameter is not found, the compliance parameter value cell of the row in the .csv file will be left empty.
    csv_name = File.basename("#{osm_file_path}_cp-empty.csv")
    # The measure will output a csv file named “filename_cp-empty.csv”

    # report final condition of model
    runner.registerFinalCondition("Out put csv file path is #{csv_name} add csv data in compliance parameter value as needed!")

    return true
  end
end

# register the measure to be used by the application
NewMeasure.new.registerWithApplication
