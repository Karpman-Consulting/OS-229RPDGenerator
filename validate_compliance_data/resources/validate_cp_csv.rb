



require 'json'
require 'pry-byebug'

module ValidateCPCSV

  RULESET_MODEL_DESCRIPTION_SCHEMA_PATH = File.join(File.dirname(__FILE__), '..', '..','dependencies','ruleset-model-description-schema','docs229')
  #ruleset-model-description-schema\docs229\ASHRAE229.schema.json
  def self.get_ashrae_229_schema_definition
    schema_path = File.join(RULESET_MODEL_DESCRIPTION_SCHEMA_PATH, 'ASHRAE229.schema.json')
    JSON.parse(File.read(schema_path))['definitions']
  end

  def self.generate_validation_errors(validation_errors)
    print('blah ')
  end


  def self.build_compliance_parameter_value_array_path(ruleset_category,compliance_parameter_name)

    array_path = ruleset_category.split('.')
    array_path.insert(1,"properties")
    array_path << "properties"
    array_path << compliance_parameter_name

    array_path
  end

  def self.get_compliance_parameter_value(ruleset_category,compliance_parameter_name,json_229_schema)

    compliance_parameter_path_keys = build_compliance_parameter_value_array_path(ruleset_category,compliance_parameter_name)
    binding.pry
    value = compliance_parameter_path_keys.reduce(json_229_schema) { |acc, key| binding.pry ;acc[key] }


  end

  def self.get_compliance_parameter_definition(ruleset_category,compliance_parameter_name)

    if @json_229_schema[ruleset_category][compliance_parameter_name].nil?
      validation_errors << "compliance_parameter_name: #{compliance_parameter_name} is not found in the schema for ruleset_category: #{ruleset_category}"
      return validation_errors
    end

    if is_nested_compliance_parameter(compliance_parameter_name,ruleset_category)

    else
      @json_229_schema[ruleset_category][compliance_parameter_name]
    end

  end

  # def self.validate_compliance_parameter(compliance_parameter)

  #   validation_errors = []

  #   if ruleset_category.nil? || ruleset_category.empty?
  #     validation_errors << " is empty for compliance_parameter_name: #{compliance_parameter_name}"
  #   end

  #   if is_nested_compliance_parameter(compliance_parameter)
  #     validation_errors << "compliance_parameter: #{compliance_parameter} has . in it. It should not have . in it"
  #   end

  #   if @json_229_schema[compliance_parameter].nil?
  #     validation_errors << "compliance_parameter: #{compliance_parameter} is not found in the schema"
  #   end

  #   validation_errors
  # end


  def self.validate_csv_cp_complete(csv_to_validate)


    validation_errors = []
    ### TODO raise error if columsns dont match exactly
    #
    @json_229_schema = get_ashrae_229_schema_definition

    csv_to_validate.each do |row|

      ruleset_category = row[2]
      compliance_parameter_name = row[3]
      compliance_parameter_value = row[4]

      self.validate_ruleset_category(ruleset_category)

      if compliance_parameter_value.nil? || compliance_parameter_value.empty?
        validation_errors << "compliance_parameter_value is empty for compliance_parameter_name: #{compliance_parameter_name}"
      end

    end

    print(csv_to_validate)

  end
end
