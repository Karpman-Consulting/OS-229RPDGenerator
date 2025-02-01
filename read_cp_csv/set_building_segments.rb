module SetBuildingSegements

  def self.read_csv_and_set_building_segments_in_comp_param_json(csv_data,comp_param_json)

    unique_building_segments_csv_ids = csv_data.select { |row| row[:compliance_parameter_category] == "building_segment" }.map { |row| row[:group_id] }.uniq

    child_objects_of_building_segments_csv = csv_data.select { |row| unique_building_segments_csv_ids.include? row[:parent_id] } #.select { |row| row[:compliance_parameter_category] == "building_segment" }.map { |row| row[:group_id] }.uniq

    building_segments = comp_param_json.dig("ruleset_model_descriptions", 0, "buildings", 0, "building_segments")

    building_segment_ids_json = building_segments.map { |segment| segment["id"] }

    unless building_segment_ids_json.sort == unique_building_segments_csv_ids.sort

      new_building_segments_in_csv = unique_building_segments_csv_ids - building_segment_ids_json

      new_building_segments_in_csv.each do |new_building_segment_id|

        new_building_segment_compliance_parameters = csv_data.select { |row| row[:group_id] == new_building_segment_id }

        new_building_segment_obj = {
          "id" => new_building_segment_id,
          "heating_ventilating_air_conditioning_systems" => [],
          "zones" => [],
        }
        ## add compliance parameters to the building segment
        new_building_segment_compliance_parameters.each do |compliance_parameter|
          new_building_segment_obj[compliance_parameter[:compliance_parameter_name]] = compliance_parameter[:compliance_parameter_value]
        end

        child_objs_of_new_building_segment_in_csv = child_objects_of_building_segments_csv.select { |child_object| child_object[:parent_id] == new_building_segment_id }

        ### building segments ONLY have heating_ventilating_and_air_conditioning_systems and zones as child objects
        building_segments.map do |building_segment|
          building_segment["heating_ventilating_air_conditioning_systems"].each do |hvac_system|

            if child_objs_of_new_building_segment_in_csv.map { |obj| obj[:group_id]}.include? hvac_system.dig("id")
              ## Move hvac system to new building segment

              new_building_segment_obj["heating_ventilating_air_conditioning_systems"].push(hvac_system)
            end
          end

          new_building_segment_obj["heating_ventilating_air_conditioning_systems"].each { |hvac_system| building_segment["heating_ventilating_air_conditioning_systems"]
          .delete(hvac_system) }
        end

        building_segments.map do |building_segment|
          building_segment["zones"].each do |zone|
            if child_objs_of_new_building_segment_in_csv.map { |obj| obj[:group_id]}.include? zone.dig("id")
              ## Move hvac system to new building segment
              new_building_segment_obj["zones"].push(zone)
            end
          end

          new_building_segment_obj["zones"].each { |zone| building_segment["zones"].delete(zone) }

        end

        building_segments << new_building_segment_obj
      end
    end

    comp_param_json
  end

end
