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
  def arguments(model)
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

  def self.get_object_type_of_additional_property(os_additional_property)
    ### Should return OS:Building etc
    if os_additional_property.modelObject.initialized
      os_additional_property.modelObject.to_s.split(',').first
    else
      "None"
    end
  end

  def self.get_object_name_of_additional_property(os_additional_property)
    ### Should return Building 1
    if os_additional_property.modelObject.initialized && os_additional_property.modelObject.name.is_initialized
      os_additional_property.modelObject.name.get
    else
      "None"
    end
  end

  def self.get_additional_property_feature_value(os_object, feature_name)
    if os_object.hasFeature(feature_name)
      case os_object.getFeatureDataType(feature_name).get
      when "Integer"
        os_object.getFeatureAsInteger(feature_name).get
      when "String"
        os_object.getFeatureAsString(feature_name).get
      when "Boolean"
        os_object.getFeatureAsBoolean(feature_name).get
      when "Double"
        os_object.getFeatureAsDouble(feature_name).get
      else
        raise RuntimeError, "Feature #{feature_name} of #{os_object.name.get} has an unknown data type, please check your osm file"
      end
    else
      raise RuntimeError, "Feature #{feature_name} not found in on additional property #{os_object.name.get}"
    end
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

    ##OpenStudio Measure pseudocode:

    translator = OpenStudio::OSVersion::VersionTranslator.new
    path = OpenStudio::Path.new(osm_file_path)

    model = translator.loadModel(path)

    @model = model.get

    compliance_parameters = @model.getAdditionalPropertiess.select { |ap| ap.hasFeature("is_compliance_parameter_90_1_2019_prm") }

    #compliance_cps
    csv_data = [['OS Parent Object','OS Parent Object Name','Ruleset Category','compliance parameter name','compliance parameter value']]

    compliance_parameters.each do |os_compliance_parameter|

      csv_data << [
      CreateComplianceParameterCsvFromOsm.get_object_type_of_additional_property(os_compliance_parameter),
      CreateComplianceParameterCsvFromOsm.get_object_name_of_additional_property(os_compliance_parameter),
      CreateComplianceParameterCsvFromOsm.get_additional_property_feature_value(os_compliance_parameter, 'compliance_parameter_category'),
      CreateComplianceParameterCsvFromOsm.get_additional_property_feature_value(os_compliance_parameter, 'compliance_parameter_name'),
      CreateComplianceParameterCsvFromOsm.get_additional_property_feature_value(os_compliance_parameter, 'compliance_parameter_value')]

    end

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