# insert your copyright here

# see the URL below for information on how to write OpenStudio measures
# http://nrel.github.io/OpenStudio-user-documentation/reference/measure_writing_guide/
require 'csv'
require_relative 'resources/validate_cp_csv'

# start the measure
class ValidateComplianceParameter < OpenStudio::Measure::ModelMeasure
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
  def arguments(model = OpenStudio::OpenStudio::Model::Model.new)
    args = OpenStudio::Measure::OSArgumentVector.new

    osm_file_path = OpenStudio::Measure::OSArgument.makeStringArgument('osm_file_path', true)
    osm_file_path.setDisplayName('Osm file path')
    osm_file_path.setDescription('Osm file path')
    args << osm_file_path

    # the name of the space to add to the model
    space_name = OpenStudio::Measure::OSArgument.makeStringArgument('csv_cp_complete', true)
    space_name.setDisplayName('csv_cp_complete')
    space_name.setDescription('Csv cp complete')
    args << space_name

    return args
  end

  # define what happens when the measure is run
  def run(model, runner, user_arguments)
    super(model, runner, user_arguments)  # Do **NOT** remove this line

    ### NOTE from Jackon just use ASHRAE229.schema.json

    # use the built-in error checking
    if !runner.validateUserArguments(arguments(model), user_arguments)
      return false
    end

    # assign the user inputs to variables
    cp_csv_to_validate = runner.getStringArgumentValue('csv_cp_complete', user_arguments)

    # check the space_name for reasonableness
    # check the space_name for reasonableness
    if cp_csv_to_validate.nil? || cp_csv_to_validate.empty? || !File.exist?(cp_csv_to_validate)
      runner.registerError('Invalid csv file path was entered.')
      return false
    end

    osm_file_path = runner.getStringArgumentValue('osm_file_path', user_arguments)

    # check the space_name for reasonableness
    if osm_file_path.nil? || osm_file_path.empty? || !File.exist?(osm_file_path)
      runner.registerError('Invalid osm file path was entered.')
      return false
    end

    csv_data = nil

    begin
      # Skip the first row thats a header
      csv_data = CSV.read(path)[1..]
    rescue CSV::MalformedCSVError => e
      runner.registerError("#{cp_csv_to_validate} The file appears to be malformed: #{e.message}")
      return false
    end


    ValidateCPCSV.validate_csv_cp_complete(csv_data)

    ### CAB 11.18.2024
    #
    #### At least one of htese has to have a valid value
    # lighting_building_area_type
    # area_type_vertical_fenestration
    # area_type_heating_ventilating_air_conditioning_system
    ### TODO figure out how to validate these - THEY would not be in the initial osm
    # BuildingSegment	is_all_new
    # BuildingSegment	lighting_building_area_type
    # BuildingSegment	area_type_vertical_fenestration
    # BuildingSegment	area_type_heating_ventilating_air_conditioning_system

    return true
  end
end

# register the measure to be used by the application
ValidateComplianceParameter.new.registerWithApplication
