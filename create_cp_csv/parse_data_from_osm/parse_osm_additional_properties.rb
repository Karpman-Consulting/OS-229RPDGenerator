
module ParseOsmAdditionalProperties

  def self.parse_osm_and_place_compliance_parameter_values_in_csv(osm_model,csv_data)

    ap_with_compliance_parameters = osm_model.getAdditionalPropertiess.select { |ap| ap.hasFeature("is_229_compliance_parameter") }

    if ap_with_compliance_parameters.empty?
      puts 'No 90.1 2019 prm compliance parameters found in osm model'
      return csv_data
    end

    ap_with_compliance_parameters.each do |os_additional_property|

      csv_data.each do |row_of_csv_data|

        if is_additional_property_this_compliance_parameter?(os_additional_property,row_of_csv_data)
          row_of_csv_data[:compliance_parameter_value] = get_additional_property_feature_value(os_additional_property,"compliance_parameter_value")

        end
      end
    end

    csv_data
  end

  def self.is_additional_property_this_compliance_parameter?(os_additional_property,row_of_csv_data)

    get_additional_property_feature_value(os_additional_property,"compliance_parameter_category").downcase ==
    row_of_csv_data[:compliance_parameter_category].downcase &&
    get_additional_property_feature_value(os_additional_property,"compliance_parameter_name").downcase ==
    row_of_csv_data[:compliance_parameter_name].downcase &&
    get_object_name_of_additional_property(os_additional_property).downcase == row_of_csv_data[:group_id].downcase

  end

  private

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
    if self.does_object_model_of_additional_property_have_name?(os_additional_property)
      os_additional_property.modelObject.name.get
    else
      "None"
    end
  end

  def self.does_object_model_of_additional_property_have_name?(os_additional_property)
    os_additional_property.modelObject.initialized && os_additional_property.modelObject.name.is_initialized
  end

  def self.get_additional_property_feature_value(os_additional_property, feature_name)

    if os_additional_property.hasFeature(feature_name)

      case os_additional_property.getFeatureDataType(feature_name).get
      when "Integer"
        os_additional_property.getFeatureAsInteger(feature_name).is_initialized ? os_additional_property.getFeatureAsInteger(feature_name).get : ""
      when "String"
        os_additional_property.getFeatureAsString(feature_name).is_initialized ? os_additional_property.getFeatureAsString(feature_name).get : ""
      when "Boolean"
        os_additional_property.getFeatureAsBoolean(feature_name).is_initialized ? os_additional_property.getFeatureAsBoolean(feature_name).get : ""
      when "Double"
        os_additional_property.getFeatureAsDouble(feature_name).is_initialized ? os_additional_property.getFeatureAsDouble(feature_name).get : ""
      else
        raise RuntimeError, "Feature #{feature_name} of additional property with handle #{os_additional_property.handle} has an unknown data type, please check your osm file"
      end
    else

      error_message = if self.does_object_model_of_additional_property_have_name?(os_additional_property)
        "Feature #{feature_name} not found in on additional property with handle #{os_additional_property.handle} and object #{os_additional_property.modelObject.name.get}"
      else
        "Feature #{feature_name} not found in on additional property with handle #{os_additional_property.handle} and no associated object"
      end

      raise RuntimeError, error_message
    end
  end
end
