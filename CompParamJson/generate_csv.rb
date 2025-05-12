require 'json'
require 'csv'
require 'jsonpath'

module GenerateCompParamJsonCsv
##
REQUIRED_COMPLIANCE_PARAMETERS = [
### Project and building
  {
    compliance_parameter_category: "RulesetProjectDescription",
    compliance_parameter: "compliance_path",
    comp_param_path: '$',
  },
  {
    compliance_parameter_category: "Weather",
    compliance_parameter: "climate_zone",
    comp_param_path: '$.weather',
    compliance_parameter_has_no_id: true
  },
#   {
#     compliance_parameter_category: "RulesetModelDescription",
#     compliance_parameter: "site_zone_type",
#     comp_param_path: '$.ruleset_model_descriptions[0]'
#   },
  {
    compliance_parameter_category: "RulesetModelDescription",
    compliance_parameter: "type",
    comp_param_path: '$.ruleset_model_descriptions[0]'
  },
#   {
#     compliance_parameter_category: "RulesetModelDescription",
#     compliance_parameter: "is_measured_infiltration_based_on_test",
#     comp_param_path: '$.ruleset_model_descriptions[0]'
#   },
  {
    compliance_parameter_category: "RulesetModelDescription",
    compliance_parameter: "measured_infiltration_pressure_difference",
    comp_param_path: '$.ruleset_model_descriptions[0]'
  },
  {
    compliance_parameter_category: "Building",
    compliance_parameter: "building_open_schedule",
    comp_param_path: '$.ruleset_model_descriptions[0].buildings[0]'
  },
  {
    compliance_parameter_category: "BuildingSegment",
    compliance_parameter: "is_all_new",
    comp_param_path: '$.ruleset_model_descriptions[0].buildings[0].building_segments[0]'
  },
  {
    compliance_parameter_category: "BuildingSegment",
    compliance_parameter: "lighting_building_area_type",
    comp_param_path: '$.ruleset_model_descriptions[0].buildings[0].building_segments[0]'
  },
#   {
#     compliance_parameter_category: "BuildingSegment",
#     compliance_parameter: "area_type_vertical_fenestration",
#     comp_param_path: '$.ruleset_model_descriptions[0].buildings[0].building_segments[0]'
#   },
#   {
#     compliance_parameter_category: "BuildingSegment",
#     compliance_parameter: "area_type_heating_ventilating_air_conditioning_system",
#     comp_param_path: '$.ruleset_model_descriptions[0].buildings[0].building_segments[0]'
#   },
### Zone
#   {
#     compliance_parameter_category: "Zone",
#     compliance_parameter: "conditioning_type",
#     comp_param_path: '$.ruleset_model_descriptions[0].buildings[0].building_segments[0].zones[*]'
#   },
  {
    compliance_parameter_category: "Zone",
    compliance_parameter: "aggregation_factor",
    comp_param_path: '$.ruleset_model_descriptions[0].buildings[0].building_segments[0].zones[*]'
  },
### HeatingVentilatingAirConditioningSystem
#   {
#     compliance_parameter_category: "HeatingVentilatingAirConditioningSystem",
#     compliance_parameter: "status_type",
#     comp_param_path: '$.ruleset_model_descriptions[0].buildings[0].building_segments[0].heating_ventilating_air_conditioning_systems[*]'
#   },
### Zone.Infiltration
  {
    compliance_parameter_category: "Infiltration",
    compliance_parameter: "measured_air_leakage_rate",
    comp_param_path: '$.ruleset_model_descriptions[0].buildings[0].building_segments[0].zones[*].infiltration'
  },
### FanSystem
  {
    compliance_parameter_category: "FanSystem",
    compliance_parameter: "air_filter_merv_rating",
    comp_param_path: '$.ruleset_model_descriptions[0].buildings[0].building_segments[0].heating_ventilating_air_conditioning_systems[*].fan_system'
  },
  {
    compliance_parameter_category: "FanSystem",
    compliance_parameter: "has_fully_ducted_return",
    comp_param_path: '$.ruleset_model_descriptions[0].buildings[0].building_segments[0].heating_ventilating_air_conditioning_systems[*].fan_system'
  },
### Fan
#   {
#     compliance_parameter_category: "Fan",
#     compliance_parameter: "status_type",
#     comp_param_path: '$.ruleset_model_descriptions[0].buildings[0].building_segments[0].heating_ventilating_air_conditioning_systems[*].fan_system.supply_fans[*]'
#   },
#   {
#     compliance_parameter_category: "Fan",
#     compliance_parameter: "status_type",
#     comp_param_path: '$.ruleset_model_descriptions[0].buildings[0].building_segments[0].heating_ventilating_air_conditioning_systems[*].fan_system.return_fans[*]'
#   },
#   {
#     compliance_parameter_category: "Fan",
#     compliance_parameter: "status_type",
#     comp_param_path: '$.ruleset_model_descriptions[0].buildings[0].building_segments[0].heating_ventilating_air_conditioning_systems[*].fan_system.exhaust_fans[*]'
#   },
#   {
#     compliance_parameter_category: "Fan",
#     compliance_parameter: "status_type",
#     comp_param_path: '$.ruleset_model_descriptions[0].buildings[0].building_segments[0].heating_ventilating_air_conditioning_systems[*].fan_system.relief_fans[*]'
#   },
#   {
#     compliance_parameter_category: "Fan",
#     compliance_parameter: "status_type",
#     comp_param_path: '$.ruleset_model_descriptions[0].buildings[0].building_segments[0].zones[*].zonal_exhaust_fan'
#   },
#   {
#     compliance_parameter_category: "Fan",
#     compliance_parameter: "status_type",
#     comp_param_path: '$.ruleset_model_descriptions[0].buildings[0].building_segments[0].zones[*].terminals[*].fan'
#   },
### Terminals
  {
    compliance_parameter_category: "Terminal",
    compliance_parameter: "is_supply_ducted",
    comp_param_path: '$.ruleset_model_descriptions[0].buildings[0].building_segments[0].zones[*].terminals[*]'
  },
### Spaces
#   {
#     compliance_parameter_category: "Space",
#     compliance_parameter: "status_type",
#     comp_param_path: '$.ruleset_model_descriptions[0].buildings[0].building_segments[0].zones[*].spaces[*]'
#   },
  {
    compliance_parameter_category: "Space",
    compliance_parameter: "lighting_space_type",
    comp_param_path: '$.ruleset_model_descriptions[0].buildings[0].building_segments[0].zones[*].spaces[*]'
  },
#   {
#     compliance_parameter_category: "Space",
#     compliance_parameter: "ventilation_space_type",
#     comp_param_path: '$.ruleset_model_descriptions[0].buildings[0].building_segments[0].zones[*].spaces[*]'
#   },
#   {
#     compliance_parameter_category: "Space",
#     compliance_parameter: "envelope_space_type",
#     comp_param_path: '$.ruleset_model_descriptions[0].buildings[0].building_segments[0].zones[*].spaces[*]'
#   },
### InteriorLighting
  {
    compliance_parameter_category: "InteriorLighting",
    compliance_parameter: "occupancy_control_type",
    comp_param_path: '$.ruleset_model_descriptions[0].buildings[0].building_segments[0].zones[*].spaces[*].interior_lighting[*]'
  },
#   {
#     compliance_parameter_category: "InteriorLighting",
#     compliance_parameter: "purpose_type",
#     comp_param_path: '$.ruleset_model_descriptions[0].buildings[0].building_segments[0].zones[*].spaces[*].interior_lighting[*]'
#   },
### Miscellenous equipment
  {
    compliance_parameter_category: "MiscellaneousEquipment",
    compliance_parameter: "type",
    comp_param_path: '$.ruleset_model_descriptions[0].buildings[0].building_segments[0].zones[*].spaces[*].miscellaneous_equipment[*]'
  },
  {
    compliance_parameter_category: "MiscellaneousEquipment",
    compliance_parameter: "has_automatic_control",
    comp_param_path: '$.ruleset_model_descriptions[0].buildings[0].building_segments[0].zones[*].spaces[*].miscellaneous_equipment[*]'
  },
### Surfaces
#   {
#     compliance_parameter_category: "Surface",
#     compliance_parameter: "status_type",
#     comp_param_path: '$.ruleset_model_descriptions[0].buildings[0].building_segments[0].zones[*].surfaces[*]'
#   },
### Subsurfaces
  {
    compliance_parameter_category: "Subsurface",
    compliance_parameter: "subclassification",
    comp_param_path: '$.ruleset_model_descriptions[0].buildings[0].building_segments[0].zones[*].surfaces[*].subsurfaces[*]'
  },
  {
    compliance_parameter_category: "Subsurface",
    compliance_parameter: "has_manual_interior_shades",
    comp_param_path: '$.ruleset_model_descriptions[0].buildings[0].building_segments[0].zones[*].surfaces[*].subsurfaces[*]'
  },
#   {
#     compliance_parameter_category: "Subsurface",
#     compliance_parameter: "is_operable",
#     comp_param_path: '$.ruleset_model_descriptions[0].buildings[0].building_segments[0].zones[*].surfaces[*].subsurfaces[*]'
#   },
#   {
#     compliance_parameter_category: "Subsurface",
#     compliance_parameter: "framing_type",
#     comp_param_path: '$.ruleset_model_descriptions[0].buildings[0].building_segments[0].zones[*].surfaces[*].subsurfaces[*]'
#   },
#   {
#     compliance_parameter_category: "Subsurface",
#     compliance_parameter: "status_type",
#     comp_param_path: '$.ruleset_model_descriptions[0].buildings[0].building_segments[0].zones[*].surfaces[*].subsurfaces[*]'
#   },
#   {
#     compliance_parameter_category: "Subsurface",
#     compliance_parameter: "has_open_sensor",
#     comp_param_path: '$.ruleset_model_descriptions[0].buildings[0].building_segments[0].zones[*].surfaces[*].subsurfaces[*]'
#   },
### Construction
  {
    compliance_parameter_category: "Construction",
    compliance_parameter: "classification",
    comp_param_path: '$.ruleset_model_descriptions[0].buildings[0].building_segments[0].zones[*].surfaces[*].construction'
  },
### Schedules
#   {
#     compliance_parameter_category: "Schedule",
#     compliance_parameter: "prescribed_type",
#     comp_param_path: '$.ruleset_model_descriptions[0].schedules[*]'
#   },
#   {
#     compliance_parameter_category: "Schedule",
#     compliance_parameter: "is_modified_for_workaround",
#     comp_param_path: '$.ruleset_model_descriptions[0].schedules[*]'
#   },
### Pump
  {
    compliance_parameter_category: "Pump",
    compliance_parameter: "impeller_efficiency",
    comp_param_path: '$.ruleset_model_descriptions[0].pumps[*]'
  },
### Boiler
  {
    compliance_parameter_category: "Boiler",
    compliance_parameter: "draft_type",
    comp_param_path: '$.ruleset_model_descriptions[0].boilers[*]'
  },
### Chiller
  {
    compliance_parameter_category: "Chiller",
    compliance_parameter: "compressor_type",
    comp_param_path: '$.ruleset_model_descriptions[0].chillers[*]'
  },
]

  def self.parse_value(value)
    return value.to_f if (Float(value) rescue false)
    return true if value.to_s.downcase == 'true'
    return false if value.to_s.downcase == 'false'

    value.to_s
  end

  def self.set_value_using_jsonpath(json_data, json_path, new_value)
    ## See https://www.rubydoc.info/gems/jsonpath/1.1.5
    modified_json_data = JsonPath.for(json_data).gsub(json_path) { |value| new_value }.to_hash
    json_data.replace(modified_json_data)
  end

  def self.produce_csv_data_from_comp_param_json(comp_param_json)
    add_parent_ids_and_path(comp_param_json)

    csv_data = []

    # Process compliance parameters
    REQUIRED_COMPLIANCE_PARAMETERS.each do |param|

      group_ids = param[:compliance_parameter_has_no_id] ? [""] : JsonPath.new("#{param[:comp_param_path]}.id").on(comp_param_json)
      parent_ids = JsonPath.new("#{param[:comp_param_path]}.parent_id").on(comp_param_json)
      parent_keys = JsonPath.new("#{param[:comp_param_path]}.json_path").on(comp_param_json)

      group_ids.each_with_index do |group_id, index|
        csv_data << {
          parent_id: get_last_part_json_path(parent_ids[index].to_s),
          parent_key: get_last_part_json_path(parent_keys[index].to_s),
          group_id: param[:compliance_parameter_has_no_id] ? "n/a" : group_id,
          compliance_parameter_category: param[:compliance_parameter_category],
          compliance_parameter_name: param[:compliance_parameter],
          ### NOTE do not read values from comp param empty json
          compliance_parameter_value: ""
      }
      end
    end

    csv_data
  end

  def self.set_comp_param_json_from_csv_data(comp_param_json,csv_data)

    csv_data.each_with_index do |csv_row_data,index|

      if csv_row_data[:compliance_parameter_name].nil?
        raise ArgumentError, "Compliance parameter name is
        nil at csv row #{index+1}"
      end

      if csv_row_data[:compliance_parameter_value].nil?
        next
      end

      REQUIRED_COMPLIANCE_PARAMETERS.each do |compliance_parameter|
        if csv_row_data[:compliance_parameter_name] != compliance_parameter[:compliance_parameter]
          next
        end

        if !csv_row_data[:compliance_parameter_has_no_id] &&  csv_row_data[:group_id].nil?
          raise ArgumentError, "group_id is
          nil at csv row #{index+1} it cannot be"
        end

        ## Ignore if em,pty compliance parameter value
        if (csv_row_data[:compliance_parameter_name].is_a?(String) && csv_row_data[:compliance_parameter_name].empty?)
          print("### #{csv_row_data[:compliance_parameter_name]} Compliance parameter value is empty")
          next
        end

        unless compliance_parameter[:compliance_parameter_has_no_id]

          ids = JsonPath.new("#{compliance_parameter[:comp_param_path]}.id").on(comp_param_json)

          if ids.include?(csv_row_data[:group_id])

            the_id = ids.find { |id| id == csv_row_data[:group_id] }
            data_in_comp_param_json = find_by_id(comp_param_json, the_id)

            updated_compliace_parameter_value = parse_value(csv_row_data[:compliance_parameter_value])

            data_in_comp_param_json[compliance_parameter[:compliance_parameter]] = updated_compliace_parameter_value
          end
        else

          updated_compliace_parameter_value = parse_value(csv_row_data[:compliance_parameter_value])

          #if csv_row_data[:compliance_parameter_name] == "compliance_path" then binding.pry end

          set_value_using_jsonpath(comp_param_json, "#{compliance_parameter[:comp_param_path]}.#{compliance_parameter[:compliance_parameter]}",
          updated_compliace_parameter_value)

        end
      end
    end

    comp_param_json

  end

  def self.find_by_id(data, target_id)
    if data.is_a?(Hash)
      return data if data['id'].downcase == target_id.downcase

      # Recurse into each value
      data.each_value do |value|
        result = find_by_id(value, target_id)
        return result unless result.nil?
      end
    elsif data.is_a?(Array)
      # Recurse into each item
      data.each do |item|
        result = find_by_id(item, target_id)
        return result unless result.nil?
      end
    end
    nil
  end


  def self.add_parent_ids_and_path(obj, parent_ids = [], path = "")
    # Recursively adds a parent_id and simplified JSON path (keys only, no $ or indices)
    if obj.is_a?(Hash)
      obj["parent_id"] = parent_ids.join(".")
      obj["json_path"] = path.gsub(/^\.|\.$/, "")  # Remove leading/trailing dots

      # Update parent_ids for child objects
      new_parent_ids = obj.key?("id") ? parent_ids + [obj["id"]] : parent_ids

      # Recursively process child elements
      obj.each do |key, value|
        child_path = path.empty? ? key.to_s : "#{path}.#{key}"
        add_parent_ids_and_path(value, new_parent_ids, child_path)
      end
    elsif obj.is_a?(Array)
      obj.each { |item| add_parent_ids_and_path(item, parent_ids, path) }
    end
  end

  def self.get_last_part_json_path(json_path)
    json_path.include?('.') ? json_path.split('.').last : json_path
  end

  private_class_method :add_parent_ids_and_path, :get_last_part_json_path

end
