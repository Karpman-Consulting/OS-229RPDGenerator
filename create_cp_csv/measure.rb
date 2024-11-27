# insert your copyright here

# see the URL below for information on how to write OpenStudio measures
# http://nrel.github.io/OpenStudio-user-documentation/reference/measure_writing_guide/
require 'openstudio'
require 'csv'
require 'pry-byebug'

# start the measure
class CreateComplianceParameterCsvFromOsm < OpenStudio::Measure::ModelMeasure
  # human readable name
  def name
    # Measure name should be the title case of the class name.
    return 'CreateComplianceParameterCsvFromOsm'
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
  def arguments(model = OpenStudio::OpenStudio::Model::Model.new)
    args = OpenStudio::Measure::OSArgumentVector.new

    osm_file_path = OpenStudio::Measure::OSArgument.makeStringArgument('osm_file_path', true)
    osm_file_path.setDisplayName('Osm file path')
    osm_file_path.setDescription('Osm file path')
    args << osm_file_path

    output_csv_file_path = OpenStudio::Measure::OSArgument.makeStringArgument('output_csv_file_path', true)
    output_csv_file_path.setDisplayName('output csv file path')
    output_csv_file_path.setDescription('output csv file path')
    output_csv_file_path.setDefaultValue('create_cp_csv.csv')
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
    if osm_file_path.nil? || osm_file_path.empty? || !File.exist?(osm_file_path)
      runner.registerError('Invalid osm file path was entered.')
      return false
    end

    ##OpenStudio Measure pseudocode:

    translator = OpenStudio::OSVersion::VersionTranslator.new
    path = OpenStudio::Path.new(osm_file_path)

    model = translator.loadModel(path)

    @model = model.get

    csv_name = "#{File.basename(osm_file_path)}-empty.csv"

    CSV.open(csv_name, "w") do |csv|
      csv_data.each do |row|
        csv << row
      end
    end

    # report final condition of model
    runner.registerFinalCondition("Out put csv file path is #{csv_name} add csv data in compliance parameter value as needed!")

    return true
  end
end

# register the measure to be used by the application
CreateComplianceParameterCsvFromOsm.new.registerWithApplication
