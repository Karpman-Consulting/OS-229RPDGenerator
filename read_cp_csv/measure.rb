# insert your copyright here

# see the URL below for information on how to write OpenStudio measures
# http://nrel.github.io/OpenStudio-user-documentation/reference/measure_writing_guide/
require 'openstudio'
require 'csv'
require 'json'
require 'open3'
require 'tmpdir'
require_relative './set_building_segments'

# start the measure
class ReadComplianceParameterCsvFromOsm < OpenStudio::Measure::ReportingMeasure

  REQUIRED_DATA_ELEMENTS = [
    'id',
    'data_source_type',
    'data_timestamp',
    'loop',
    'loop_or_piping',
    'cooling_loop',
    'distribution_system',
    'served_by_distribution_system'
]

  def self.remove_backticks_from_headers(headers)
    ### Sometimes the headers have backticks in them, so that the headers look like this
    ### ["229 data group id``", "229 parent type", "229 parent id",
    ### "compliance parameter category", "compliance parameter name", "compliance parameter value"]
    ### make sure that they are removed

    headers.map { |header| header.gsub('`', '') }
  end

  def self.read_comp_param_csv_data(csv_file_path,runner)
    ### Only read rows that contain a value ignore the rest
    csv_data = []

    expected_headers = {
      '229 data group id' => :group_id,
      '229 parent type' => :parent_key,
      '229 parent id' => :parent_id,
      'compliance parameter category' => :compliance_parameter_category,
      'compliance parameter name' => :compliance_parameter_name,
      'compliance parameter value' => :compliance_parameter_value
    }

    csv = CSV.read(csv_file_path, headers: true)

    if self.remove_backticks_from_headers(csv.headers) != expected_headers.keys
      runner.registerError("Expected headers #{expected_headers.keys} but got #{csv.headers} headers in
      the csv must be exactly the same headers produced by the create_cp_csv measure")
    end

    csv.each do |row|
      # Map headers to their snake_case symbols
      row_hash = row.to_h.transform_keys { |key| expected_headers[key] }
      csv_data << row_hash
    end

    csv_data
  end
  # human readable name
  def name
    # Measure name should be the title case of the class name.
    return 'ReadComplianceParameterCsvFromOsm'
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

    updated_comp_param_json_file_path = OpenStudio::Measure::OSArgument.makeStringArgument('updated_comp_param_json_file_path', true)
    updated_comp_param_json_file_path.setDisplayName('path to updated comp param json file')
    updated_comp_param_json_file_path.setDescription('path to updated comp param json file')
    args << updated_comp_param_json_file_path

    output_csv_file_path = OpenStudio::Measure::OSArgument.makeStringArgument('csv_file_path', true)
    output_csv_file_path.setDisplayName('csv_file_path')
    output_csv_file_path.setDescription('csv_file_path')
    args << output_csv_file_path

    return args
  end

  def self.set_values_to_empty(data)
    if data.is_a?(Hash)
      data.each do |key, value|
        if not ReadComplianceParameterCsvFromOsm::REQUIRED_DATA_ELEMENTS.include?(key)
          if value.is_a?(Hash) || value.is_a?(Array)
            set_values_to_empty(value)
          else
            data[key] = ""
          end
        end
      end
    elsif data.is_a?(Array)
      data.each do |item|
        set_values_to_empty(item)
      end
    end

    data
  end

  def remove_empty_keys(json_data)
    case json_data
    when Hash
      json_data.each do |key, value|
        if value.nil? || (value.respond_to?(:empty?) && value.empty?)
          json_data.delete(key)
        else
          remove_empty_keys(value)
        end
      end
    when Array
      json_data.each do |item|
        remove_empty_keys(item)
      end
    end
    json_data
  end

  # define what happens when the measure is run
  def run(runner, user_arguments)
    super(runner, user_arguments)

    # use the built-in error checking
    if !runner.validateUserArguments(arguments(), user_arguments)
      return false
    end

    # assign the user inputs to variables
    csv_file_path = runner.getStringArgumentValue('csv_file_path', user_arguments)

    empty_comp_param_json_file_path = runner.getStringArgumentValue('empty_comp_param_json_file_path', user_arguments)

    updated_comp_param_json_file_path = runner.getStringArgumentValue('updated_comp_param_json_file_path', user_arguments)

    if empty_comp_param_json_file_path.nil? || empty_comp_param_json_file_path.empty? || !File.exist?(empty_comp_param_json_file_path)
      runner.registerError("Could not find file #{empty_comp_param_json_file_path} to write to.")
      return false
    end

    if csv_file_path.nil? || csv_file_path.empty? || !File.exist?(csv_file_path)
      runner.registerError("Could not find csv file #{csv_file_path} to read from")
      return false
    end

    csv_data = ReadComplianceParameterCsvFromOsm.read_comp_param_csv_data(csv_file_path,runner)

    comp_param_json = SetBuildingSegements.read_csv_and_set_building_segments_in_comp_param_json(csv_data,
    ReadComplianceParameterCsvFromOsm.set_values_to_empty(JSON.parse(File.read(empty_comp_param_json_file_path))))

    comp_param_json = self.remove_empty_keys(comp_param_json)

    set_comp_param_script_path = File.expand_path('set_comp_param_json_from_csv_data.rb', __dir__)

    runner.registerInfo("Running script to generate comp param json: #{set_comp_param_script_path}")

    updated_comp_param_json = nil
    Dir.mktmpdir do |dir|

      comp_param_json_file = File.join(dir, 'comp_param_json.json')
      csv_data_file = File.join(dir, 'csv_data.json')

      # Write the JSON data to files in the temporary directory
      File.write(comp_param_json_file, comp_param_json.to_json)
      File.write(csv_data_file, csv_data.to_json)

      # Run the separate Ruby script using Open3 and pass the paths of the temporary files as arguments

      stdout, stderr, status = Open3.capture3("ruby", set_comp_param_script_path, comp_param_json_file, csv_data_file)

      if status.success?
        updated_comp_param_json = JSON.parse(stdout)
      else
        runner.registerError("Failed to generate CSV data: #{stderr}")
        return false
      end
    end
    ### TODO - not critical path write out additional properties to osm

    File.write(updated_comp_param_json_file_path, JSON.pretty_generate(updated_comp_param_json))

    runner.registerFinalCondition("Successfully wrote out updated comp param json to #{updated_comp_param_json_file_path}")

    return true
  end
end

# register the measure to be used by the application
ReadComplianceParameterCsvFromOsm.new.registerWithApplication
