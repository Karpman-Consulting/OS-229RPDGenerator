# insert your copyright here

# see the URL below for information on how to write OpenStudio measures
# http://nrel.github.io/OpenStudio-user-documentation/reference/measure_writing_guide/
require 'openstudio'
require 'json'
require 'csv'
require 'open3'
#require_relative '../CompParamJson/generate_csv'
require_relative './parse_data_from_osm/parse_osm_additional_properties'
### TODO rename everything - is_229_compliance_parameter as per Jacksons request

# start the measure
class CreateComplianceParameterCsvFromOsm < OpenStudio::Measure::ReportingMeasure
  # human readable name
  def name
    # Measure name should be the title case of the class name.
    return 'Create ComplianceParameter Csv From Osm'
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
  def arguments(model = nil)
    args = OpenStudio::Measure::OSArgumentVector.new

    empty_comp_param_json_file_path = OpenStudio::Measure::OSArgument.makeStringArgument('empty_comp_param_json_file_path', true)
    empty_comp_param_json_file_path.setDisplayName('path to empty comp param json file')
    empty_comp_param_json_file_path.setDescription('path to empty comp param json file')
    args << empty_comp_param_json_file_path

    output_csv_file_path = OpenStudio::Measure::OSArgument.makeStringArgument('output_csv_file_path', true)
    output_csv_file_path.setDisplayName('output csv file path')
    output_csv_file_path.setDescription('output csv file path')
    args << output_csv_file_path

    return args
  end

  # define what happens when the measure is run
  def run(runner, user_arguments)
    super(runner, user_arguments)

    runner.registerInfo("blah blah")

    # use the built-in error checking
    if !runner.validateUserArguments(arguments(), user_arguments)
      return false
    end

    model = runner.lastOpenStudioModel
    if model.empty?
      runner.registerError('Cannot find last model.')
      return false
    end
    model = model.get

    ### the original compliance parameter json will ONLY ever have one building segment
    # assign the user inputs to variables
    output_csv_file_path = runner.getStringArgumentValue('output_csv_file_path', user_arguments)

    empty_comp_param_json_file_path = runner.getStringArgumentValue('empty_comp_param_json_file_path', user_arguments)

    if empty_comp_param_json_file_path.nil? || empty_comp_param_json_file_path.empty? || !File.exist?(empty_comp_param_json_file_path)
      runner.registerInfo("Getting here")
      runner.registerError("Could not find file #{empty_comp_param_json_file_path}.")
      return false
    end

    # Run the method in a child process using Open3
    generate_csv_script_path = File.expand_path('produce_csv_data_from_comp_param_json.rb', __dir__)

    runner.registerInfo("Running script to generate CSV data from empty comp param json: #{generate_csv_script_path}")

    stdout, stderr, status = Open3.capture3("ruby", generate_csv_script_path, empty_comp_param_json_file_path)

    if status.success?
      csv_data = JSON.parse(stdout).each { |row| row.transform_keys!(&:to_sym) }
    else
      runner.registerError("Failed to generate CSV data: #{stderr}")
      return false
    end

    csv_data = ParseOsmAdditionalProperties.parse_osm_and_place_compliance_parameter_values_in_csv(model,csv_data)

    CSV.open(File.join(output_csv_file_path), 'w') do |csv_data_as_excel|

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
    runner.registerFinalCondition("CSV with 229 compliance parameters has been created at path
     #{File.basename(output_csv_file_path)}
     add compliance parameter values as needed")

    return true
  end
end

# register the measure to be used by the application
CreateComplianceParameterCsvFromOsm.new.registerWithApplication
