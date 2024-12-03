require 'json'
require 'csv'
require 'jsonpath'

module GenerateTwoTwoNineCompParamJsonCsv
  ##
  REQUIRED_COMPLIANCE_PARAMETERS = [
  ### com_param_path is taken from comp param file
  ### Project and building
  # {
  #   "compliance_parameter_category": "ruleset_project_description",
  #   "compliance_parameter": "compliance_path",
  #   "comp_param_path":'$.ruleset_model_descriptions[0]'
  # },
  {
    "compliance_parameter_category": "ruleset_project_description",
    "compliance_parameter": "type",
    "comp_param_path":'$.ruleset_model_descriptions[0]'
  },
  {
    "compliance_parameter_category": "ruleset_project_description",
    "compliance_parameter": "measured_infiltration_pressure_difference",
    "comp_param_path":'$.ruleset_model_descriptions[0]'
  },
  {
    "compliance_parameter_category": "ruleset_project_description",
    "compliance_parameter": "is_measured_infiltration_based_on_test",
    "comp_param_path":'$.ruleset_model_descriptions[0]'
  },
  {
    "compliance_parameter_category": "ruleset_project_description",
    "compliance_parameter": "site_zone_type",
    "comp_param_path":'$.ruleset_model_descriptions[0]'
  },
  # {
  #   "compliance_parameter_category": "building",
  #   "compliance_parameter": "building_open_schedule",
  #   "comp_param_path":'$.ruleset_model_descriptions[0].buildings[0]'
  # },
    {
    "compliance_parameter_category":"building_segment",
    "compliance_parameter":"is_all_new",
    "comp_param_path":'$.ruleset_model_descriptions[0].buildings[0].building_segments[0]'
  },
      {
    "compliance_parameter_category":"building_segment",
    "compliance_parameter":"is_all_new",
    "comp_param_path":'$.ruleset_model_descriptions[0].buildings[0].building_segments[0]'
  },
  {
    "compliance_parameter_category":"building_segment",
    "compliance_parameter":"lighting_building_area_type",
    "comp_param_path":'$.ruleset_model_descriptions[0].buildings[0].building_segments[0]'
  },
  {
    "compliance_parameter_category":"building_segment",
    "compliance_parameter":"area_type_vertical_fenestration",
    "comp_param_path":'$.ruleset_model_descriptions[0].buildings[0].building_segments[0]'
  },
  {
    "compliance_parameter_category":"building_segment",
    "compliance_parameter": "area_type_heating_ventilating_air_conditioning_system",
    "comp_param_path":'$.ruleset_model_descriptions[0].buildings[0].building_segments[0]'
  },
    # HeatingVentilatingAirConditioningSystem
    {
    "compliance_parameter_category":"heating_ventilating_air_conditioning_systems",
    "compliance_parameter": "status_type",
    "comp_param_path":'$.ruleset_model_descriptions[0].buildings[0].building_segments[0].heating_ventilating_air_conditioning_systems[*]'
  },
  ###HeatingVentilatingAirConditioningSystem.FanSystem
  {
    "compliance_parameter_category":"heating_ventilation_airconditioning_system",
    "compliance_parameter": "air_filter_merv_rating",
    "comp_param_path":'$.ruleset_model_descriptions[0].buildings[0].building_segments[0].heating_ventilating_air_conditioning_systems[*]'
  },
  {
    "compliance_parameter_category":"heating_ventilation_airconditioning_system",
    "compliance_parameter": "has_fully_ducted_return",
    "comp_param_path":'$.ruleset_model_descriptions[0].buildings[0].building_segments[0].heating_ventilating_air_conditioning_systems[*]'
  },
  ### Zone
    {
    "compliance_parameter_category":"zone",
    "compliance_parameter": "aggregation_factor",
    "comp_param_path":'$.ruleset_model_descriptions[0].buildings[0].building_segments[0].zones[*]'
  },
  {
    "compliance_parameter_category":"zone",
    "compliance_parameter": "conditioning_type",
    "comp_param_path":'$.ruleset_model_descriptions[0].buildings[0].building_segments[0].zones[*]'
  },


  ### Zone.Infiltration
  {
    "compliance_parameter_category":"infiltration",
    "compliance_parameter": "measured_air_leakage_rate",
    "comp_param_path":'$.ruleset_model_descriptions[0].buildings[0].building_segments[0].zones[*].infiltration'
  },
  ### Terminals
  {
    "compliance_parameter_category":"terminal",
    "compliance_parameter": "is_supply_ducted",
    "comp_param_path":'$.ruleset_model_descriptions[0].buildings[0].building_segments[0].zones[*].terminals[*]'
  },

  ### SUrfaces
  {
    "compliance_parameter_category":"surface",
    "compliance_parameter": "status_type",
    "comp_param_path":'$.ruleset_model_descriptions[0].buildings[0].building_segments[0].zones[*].surfaces[*]'
  },

  ### Subsurfaces
  {
    "compliance_parameter_category":"subsurface",
    "compliance_parameter": "subclassification",
    "comp_param_path":'$.ruleset_model_descriptions[0].buildings[0].building_segments[0].zones[*].surfaces[*].subsurfaces[*]'
  },
  {
    "compliance_parameter_category":"subsurface",
    "compliance_parameter": "has_manual_interior_shades",
    "comp_param_path":'$.ruleset_model_descriptions[0].buildings[0].building_segments[0].zones[*].surfaces[*].subsurfaces[*]'
  },
  {
    "compliance_parameter_category":"subsurface",
    "compliance_parameter": "is_operable",
    "comp_param_path":'$.ruleset_model_descriptions[0].buildings[0].building_segments[0].zones[*].surfaces[*].subsurfaces[*]'
  },
      {
    "compliance_parameter_category":"subsurface",
    "compliance_parameter": "framing_type",
    "comp_param_path":'$.ruleset_model_descriptions[0].buildings[0].building_segments[0].zones[*].surfaces[*].subsurfaces[*]'
  },
        {
    "compliance_parameter_category":"subsurface",
    "compliance_parameter": "status_type",
    "comp_param_path":'$.ruleset_model_descriptions[0].buildings[0].building_segments[0].zones[*].surfaces[*].subsurfaces[*]'
  },
          {
    "compliance_parameter_category":"subsurface",
    "compliance_parameter": "has_open_sensor",
    "comp_param_path":'$.ruleset_model_descriptions[0].buildings[0].building_segments[0].zones[*].surfaces[*].subsurfaces[*]'
  },
  ### Spaces
  {
    "compliance_parameter_category":"space",
    "compliance_parameter": "status_type",
    "comp_param_path":'$.ruleset_model_descriptions[0].buildings[0].building_segments[0].zones[*].spaces[*]'
  },
    {
    "compliance_parameter_category":"space",
    "compliance_parameter": "lighting_space_type",
    "comp_param_path":'$.ruleset_model_descriptions[0].buildings[0].building_segments[0].zones[*].spaces[*]'
  },
    {
    "compliance_parameter_category":"space",
    "compliance_parameter": "function",
    "comp_param_path":'$.ruleset_model_descriptions[0].buildings[0].building_segments[0].zones[*].spaces[*]'
  },
    {
    "compliance_parameter_category":"space",
    "compliance_parameter": "ventilation_space_type",
    "comp_param_path":'$.ruleset_model_descriptions[0].buildings[0].building_segments[0].zones[*].spaces[*]'
  },
      {
    "compliance_parameter_category":"space",
    "compliance_parameter": "envelope_space_type",
    "comp_param_path":'$.ruleset_model_descriptions[0].buildings[0].building_segments[0].zones[*].spaces[*]'
  },
  {
    "compliance_parameter_category":"space",
    "compliance_parameter": "occupancy_control_type",
    "comp_param_path":'$.ruleset_model_descriptions[0].buildings[0].building_segments[0].zones[*].spaces[*].interior_lighting[*]'
  },
  ## Schedules
  {
    "compliance_parameter_category":"schedule",
    "compliance_parameter": "prescribed_type",
    "comp_param_path":'$.ruleset_model_descriptions[0].schedules[*]'
  },
  {
    "compliance_parameter_category":"schedule",
    "compliance_parameter": "is_modified_for_workaround",
    "comp_param_path":'$.ruleset_model_descriptions[0].schedules[*]'
  },
  ### Pump

    {
    "compliance_parameter_category":"pump",
    "compliance_parameter": "impeller_efficiency",
    "comp_param_path":'$.ruleset_model_descriptions[0].pumps[*]'
  },


#   {
#     "Boiler": "draft_type"
#   },
#   {
#     "Chiller": "compressor_type"
#   },
#   {
#     "HeatRejection": "fan_type"
#   },
#   {
#     "heating_ventilating_air_conditioning_systems": "status_type"
#   },
#   {
#     "heating_ventilating_air_conditioning_systems.fan_system": "air_filter_merv_rating"
#   },
#   {
#     "zone": "aggregation_factor"
#   },
#   {
#     "zone.infiltration": "measured_air_leakage_rate"
#   },


  ]

  def self.produce_csv_data_from_comp_param_json(comp_param_json)

    add_parent_ids_and_path(comp_param_json)

    csv_data = []

    # Process compliance parameters
    REQUIRED_COMPLIANCE_PARAMETERS.each do |compliance_parameter|
      ids = JsonPath.new("#{compliance_parameter[:comp_param_path]}.id").on(comp_param_json)
      #values = JsonPath.new("#{compliance_parameter[:comp_param_path]}.#{compliance_parameter[:compliance_parameter]}").on(comp_param_json)

      if ids.empty?
        puts "### Could not get ids #{compliance_parameter[:comp_param_path]}.#{compliance_parameter[:compliance_parameter]}"
        next
      end

      two_twenty_nine_type = JsonPath.new("#{compliance_parameter[:comp_param_path]}.json_path").on(comp_param_json)
      two_twenty_nine_parent_id = JsonPath.new("#{compliance_parameter[:comp_param_path]}.parent_id").on(comp_param_json)
      compliance_parameter_category = compliance_parameter[:compliance_parameter_category]

      ids.each_with_index do |id, index|
        csv_data << {
          two_twenty_nine_group_id: id,
          two_twenty_nine_parent_type: self.get_last_part_json_path(two_twenty_nine_type[index]),
          two_twenty_nine_parent_id: self.get_last_part_json_path(two_twenty_nine_parent_id[index]),
          compliance_parameter_category: compliance_parameter_category,
          compliance_parameter_name: compliance_parameter[:compliance_parameter],
          compliance_parameter_value: ""
      }
      end
    end

    csv_data
  end

  def self.set_comp_param_json_from_csv_data(comp_param_json,csv_data)

    csv_data.each_with_index do |csv_row_data,index|

      REQUIRED_COMPLIANCE_PARAMETERS.each do |compliance_parameter|
        if csv_row_data[:compliance_parameter_name] != compliance_parameter[:compliance_parameter]
          next
        end
        ## Ignore if em,pty compliance parameter value
        if csv_row_data[:compliance_parameter_value].nil? ||
          (csv_row_data[:compliance_parameter_name].is_a?(String) && csv_row_data[:compliance_parameter_name].empty?)

          next
        end

        ids = JsonPath.new("#{compliance_parameter[:comp_param_path]}.id").on(comp_param_json)

        if ids.include?(csv_row_data[:two_twenty_nine_group_id])

          the_id = ids.find { |id| id == csv_row_data[:two_twenty_nine_group_id] }
          data_in_comp_param_json = find_by_id(comp_param_json, the_id)

          if data_in_comp_param_json[compliance_parameter[:compliance_parameter]].nil?
            ### TODO need to resolve these parameters
            if ["lighting_space_type","air_filter_merv_rating","has_fully_ducted_return","ventilation_space_type","envelope_space_type"]
              .include? compliance_parameter[:compliance_parameter]
              next
            end

            raise "Something has gone wrong cannot find compliance parameter: #{compliance_parameter[:compliance_parameter]} in comp_param_json"
          end

          updated_compliace_parameter_value = csv_row_data[:compliance_parameter_value]
          #if the_id.downcase == "PERIMETER_ZN_1".downcase then binding.pry end
          data_in_comp_param_json[compliance_parameter[:compliance_parameter]] = updated_compliace_parameter_value

          print("Updated compliance parameter: #{compliance_parameter[:compliance_parameter]} of object with id #{the_id}
          with value: #{updated_compliace_parameter_value} in comp_param_json")

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
      # If the current object has an 'id', update its 'parent_id' and 'json_path'
      if obj.key?("id")
        # Join the parent ids into a path and assign it to the parent_id field
        obj["parent_id"] = parent_ids.join(".")
        obj["json_path"] = path.gsub(/^\.|\.$/, "")  # Remove leading/trailing dots
      end

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
    json_path.split('.').last
  end

  private_class_method :add_parent_ids_and_path, :get_last_part_json_path

end
