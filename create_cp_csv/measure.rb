# insert your copyright here

# see the URL below for information on how to write OpenStudio measures
# http://nrel.github.io/OpenStudio-user-documentation/reference/measure_writing_guide/
require 'openstudio'
require 'csv'
require_relative '../CompParamJson/generate_csv'
require_relative './parse_data_from_osm/parse_osm_additional_properties'

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
  def arguments(model = OpenStudio::Model::Model.new)
    args = OpenStudio::Measure::OSArgumentVector.new

    empty_comp_param_json_file_path = OpenStudio::Measure::OSArgument.makeStringArgument('empty_comp_param_json_file_path', true)
    empty_comp_param_json_file_path.setDisplayName('path to empty comp param json file')
    empty_comp_param_json_file_path.setDescription('path to empty comp param json file')
    args << empty_comp_param_json_file_path

    osm_file_path = OpenStudio::Measure::OSArgument.makeStringArgument('osm_file_path', true)
    osm_file_path.setDisplayName('Osm file path')
    osm_file_path.setDescription('Osm file path')
    args << osm_file_path

    output_csv_file_path = OpenStudio::Measure::OSArgument.makeStringArgument('output_csv_file_path', true)
    output_csv_file_path.setDisplayName('output csv file path')
    output_csv_file_path.setDescription('output csv file path')
    output_csv_file_path.setDefaultValue('./')
    args << output_csv_file_path

    return args
  end

  # define what happens when the measure is run
  def run(model, runner, user_arguments)
    super(model, runner, user_arguments)

    # use the built-in error checking
    if !runner.validateUserArguments(arguments(model), user_arguments)
      return false
    end


    ### the original compliance parameter json will ONLY ever have one building segment
    # assign the user inputs to variables
    osm_file_path = runner.getStringArgumentValue('osm_file_path', user_arguments)

    output_csv_file_path = runner.getStringArgumentValue('output_csv_file_path', user_arguments)

    empty_comp_param_json_file_path = runner.getStringArgumentValue('empty_comp_param_json_file_path', user_arguments)

    if empty_comp_param_json_file_path.nil? || empty_comp_param_json_file_path.empty? || !File.exist?(empty_comp_param_json_file_path)
      runner.registerError("Could not find file #{empty_comp_param_json_file_path}.")
      return false
    end

    csv_data = GenerateCsvOfCompParamJson.produce_csv_data_from_comp_param_json(Json.parse(File.read(empty_comp_param_json_file_path)))

    if !osm_file_path.nil? && !osm_file_path.empty? && File.exist?(osm_file_path)

      translator = OpenStudio::OSVersion::VersionTranslator.new
      path = OpenStudio::Path.new(osm_file_path)

      model = translator.loadModel(path)

      if !model.is_initialized
        runner.registerError("A osm was provided but could not be loaded. Aborting")
        return false
      end

      csv_data = ParseOsmAdditionalProperties.parse_osm_and_place_compliance_parameter_values_in_csv(model.get,csv_data)

    end

    csv_name = "#{File.basename(osm_file_path)}-empty.csv"

    CSV.open(File.join(output_csv_file_path,csv_name), 'w') do |csv_data_as_excel|

      csv_data_as_excel <<
          ['229 data group id',
          '229 parent type',
          '229 parent id',
          'compliance parameter category',
          'compliance parameter name',
          'compliance parameter value']

          csv_data.each { |row_as_hash_of_data|
            csv_data_as_excel << [
                row_as_hash_of_data[:two_twenty_nine_group_id],
                row_as_hash_of_data[:two_twenty_nine_parent_type],
                row_as_hash_of_data[:two_twenty_nine_parent_id],
                row_as_hash_of_data[:compliance_parameter_category],
                row_as_hash_of_data[:compliance_parameter_name],
                row_as_hash_of_data[:compliance_parameter_value]
              ]
            }
    end

    # report final condition of model
    runner.registerFinalCondition("Out put csv file path is #{csv_name} add csv data in compliance parameter value as needed!")

    return true
  end
end

# register the measure to be used by the application
CreateComplianceParameterCsvFromOsm.new.registerWithApplication
