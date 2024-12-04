require 'minitest/autorun'
require 'openstudio'
require 'json'
require_relative './parse_osm_additional_properties'
require_relative '../../CompParamJson/generate_csv'

class GetComplianceParameterFromOsm < Minitest::Test

  def setup

    path = OpenStudio::Path.new(File.join(File.dirname(File.realpath(__FILE__)),'example_model.osm'))

    path_bad_values = OpenStudio::Path.new(File.join(File.dirname(File.realpath(__FILE__)),'example_model_with_bad_values.osm'))

    translator = OpenStudio::OSVersion::VersionTranslator.new

    @model = translator.loadModel(path).get

    translator2 = OpenStudio::OSVersion::VersionTranslator.new

    @model_bad_values = translator2.loadModel(path_bad_values).get

  end

  def test_get_object_type_of_additional_property

    additional_properties = @model.getAdditionalPropertiess.select { |ap| ap.hasFeature("is_compliance_parameter_90_1_2019_prm") }

    zone_infiltration_object = additional_properties.find { |ap| ap.handle.to_s == '{b0c16963-bf29-4919-9474-4e647b365c22}' }

    #a_additional_property = additional_properties.first

    # With no model object for additional properties (not sure if this is possible?)

    assert_equal 'OS:Space', ParseOsmAdditionalProperties.get_object_type_of_additional_property(zone_infiltration_object)

    assert_equal 'Zone.Infiltration',ParseOsmAdditionalProperties.get_additional_property_feature_value(zone_infiltration_object,'compliance_parameter_category')

    assert_equal 'measured_air_leakage_rate',ParseOsmAdditionalProperties.get_additional_property_feature_value(zone_infiltration_object,'compliance_parameter_name')

    assert_equal 22,ParseOsmAdditionalProperties.get_additional_property_feature_value(zone_infiltration_object,'compliance_parameter_value')

  end

  def test_get_additional_property_empty_value
    ### This Additional properties shoudl return an empty value for compliance_parameter_value
    # OS:AdditionalProperties,
    # {b0c16963-bf29-4919-9474-4e647b365c23}, !- Handle
    # {30fea77d-d1c6-417c-9fd9-e5ee4bea434a}, !- Object Name
    # is_compliance_parameter_90_1_2019_prm,        !- Feature Name 1
    # Boolean,                                 !- Feature Data Type 1
    # true,                     !- Feature Value 1
    # compliance_parameter_category,        !- Feature Name 2
    # String,                                 !- Feature Data Type 2
    # Zone.Infiltration,                   !- Feature Value 2
    # compliance_parameter_name,        !- Feature Name 3
    # String,                                 !- Feature Data Type 3
    # measured_air_leakage_rate, !- Feature Value 3
    # compliance_parameter_value,        !- Feature Name 4
    # Double,                                 !- Feature Data Type 4
    # ;                     !- Feature Value 4

    additional_properties = @model.getAdditionalPropertiess.select { |ap| ap.hasFeature("is_compliance_parameter_90_1_2019_prm") }

    zone_infiltration_object_no_value = additional_properties.find { |ap| ap.handle.to_s == '{b0c16963-bf29-4919-9474-4e647b365c23}' }

    assert_equal 'OS:Space', ParseOsmAdditionalProperties.get_object_type_of_additional_property(zone_infiltration_object_no_value)

    assert_equal 'Zone.Infiltration',ParseOsmAdditionalProperties.get_additional_property_feature_value(zone_infiltration_object_no_value,'compliance_parameter_category')

    assert_equal 'measured_air_leakage_rate',ParseOsmAdditionalProperties.get_additional_property_feature_value(zone_infiltration_object_no_value,'compliance_parameter_name')

    assert_equal "",ParseOsmAdditionalProperties.get_additional_property_feature_value(zone_infiltration_object_no_value,'compliance_parameter_value')
  end

  def test_get_additional_property_no_value
    ### Shoudl throw an error as compliance_parameter_value is not defined
    #   OS:AdditionalProperties,
    # {b0c16963-bf29-4919-9474-4e647b365c24}, !- Handle
    # {1c7487fe-94e4-4b4b-924e-bc15951fc750}, !- Object Name
    # is_compliance_parameter_90_1_2019_prm,        !- Feature Name 1
    # Boolean,                                 !- Feature Data Type 1
    # true,                     !- Feature Value 1
    # compliance_parameter_category,        !- Feature Name 2
    # String,                                 !- Feature Data Type 2
    # Zone.Infiltration,                   !- Feature Value 2
    # compliance_parameter_name,        !- Feature Name 3
    # String,                                 !- Feature Data Type 3
    # measured_air_leakage_rate; !- Feature Value 3

    additional_properties = @model_bad_values.getAdditionalPropertiess.select { |ap| ap.hasFeature("is_compliance_parameter_90_1_2019_prm") }

    zone_infiltration_object_no_value = additional_properties.find { |ap| ap.handle.to_s == '{b0c16963-bf29-4919-9474-4e647b365c24}' }

    assert_equal 'OS:Space', ParseOsmAdditionalProperties.get_object_type_of_additional_property(zone_infiltration_object_no_value)

    assert_equal 'Zone.Infiltration',ParseOsmAdditionalProperties.get_additional_property_feature_value(zone_infiltration_object_no_value,'compliance_parameter_category')

    assert_equal 'measured_air_leakage_rate',ParseOsmAdditionalProperties.get_additional_property_feature_value(zone_infiltration_object_no_value,'compliance_parameter_name')

    error = assert_raises(RuntimeError) do
      ParseOsmAdditionalProperties.get_additional_property_feature_value(zone_infiltration_object_no_value,'compliance_parameter_value')
    end

    assert_equal "Feature compliance_parameter_value not found in on additional property with handle {b0c16963-bf29-4919-9474-4e647b365c24} and object aim0640",
     error.message

  end

end


class ParseOsmAndPlaceComplianceParametersInOsm < Minitest::Test

  def setup

    test_file_path = File.join(File.dirname(File.realpath(__FILE__)),'ASHRAE901_OfficeSmall_STD2019_Denver.osm')
    path = OpenStudio::Path.new(test_file_path)

    unless File.exist?(test_file_path)
      raise "Test file not found: #{test_file_path}"
    end

    translator = OpenStudio::OSVersion::VersionTranslator.new

    @test_model = translator.loadModel(path).get

    # Parse the JSON
    @comp_param_json = JSON.parse(File.read(File.join(File.dirname(File.realpath(__FILE__)),
    'ASHRAE901_OfficeSmall_STD2019_Denver.comp-param-empty.json')))

    @csv_data = GenerateTwoTwoNineCompParamJsonCsv.produce_csv_data_from_comp_param_json(@comp_param_json)

    ### This code will count the number of times that the compliance_parameter_value
    ### has been set
    @csv_data.each do |row|
      def row.[]=(key, value)
        @set_counter ||= 0
        @set_counter += 1 if key == :compliance_parameter_value
        super
      end

      def row.get_set_count
        @set_counter || 0
      end

      def row.reset_set_count
        @set_counter = 0
      end
    end

  end

  def teardown

    @csv_data.each do |row|
      row.reset_set_count
    end
  end

  def test_is_additional_property_this_compliance_parameter?

    compliance_parameters = @test_model.getAdditionalPropertiess.select { |ap| ap.hasFeature("is_compliance_parameter_90_1_2019_prm") }

    additional_property_of_subsurface_with_compliance_parameter = compliance_parameters.find { |ap| ap.handle.to_s == '{b0c16963-bf29-4919-9474-4e647b365c38}' }

    ## If ALL OF two_twenty_nine_group_id & compliance_parameter_category & compliance_parameter_name
    #### do match additional property and its associated object is_additional_property_this_compliance_parameter? should return true

    assert ParseOsmAdditionalProperties.is_additional_property_this_compliance_parameter?(
      additional_property_of_subsurface_with_compliance_parameter,
      ### Test csv row is copied directly from the output_comp_param.csv
      {
        two_twenty_nine_group_id: 'Perimeter_ZN_1_wall_south_Window_2',
        two_twenty_nine_parent_type: 'subsurfaces',
        two_twenty_nine_parent_id: 'PERIMETER_ZN_1_WALL_SOUTH',
        compliance_parameter_category: 'subsurface',
        compliance_parameter_name: 'has_open_sensor',
        compliance_parameter_value: 'true'
      }
    )

    ## If ANY OF two_twenty_nine_group_id OR compliance_parameter_category OR compliance_parameter_name
    #### do not match additional property and its associated object is_additional_property_this_compliance_parameter? should return false

    refute ParseOsmAdditionalProperties.is_additional_property_this_compliance_parameter?(
      additional_property_of_subsurface_with_compliance_parameter,
      ### Test csv row is copied directly from the output_comp_param.csv
      {
        two_twenty_nine_group_id: 'Perimeter_ZN_1_wall_south_Window_1',
        two_twenty_nine_parent_type: 'subsurfaces',
        two_twenty_nine_parent_id: 'PERIMETER_ZN_1_WALL_SOUTH',
        compliance_parameter_category: 'subsurface',
        compliance_parameter_name: 'has_open_sensor',
        compliance_parameter_value: 'true'
      }
    )

    refute ParseOsmAdditionalProperties.is_additional_property_this_compliance_parameter?(
      additional_property_of_subsurface_with_compliance_parameter,
      ### Test csv row is copied directly from the output_comp_param.csv
      {
        two_twenty_nine_group_id: 'Perimeter_ZN_1_wall_south_Window_2',
        two_twenty_nine_parent_type: 'subsurfaces',
        two_twenty_nine_parent_id: 'PERIMETER_ZN_1_WALL_SOUTH',
        compliance_parameter_category: 'subsurface1',
        compliance_parameter_name: 'has_open_sensor',
        compliance_parameter_value: 'true'
      }
    )

    refute ParseOsmAdditionalProperties.is_additional_property_this_compliance_parameter?(
      additional_property_of_subsurface_with_compliance_parameter,
      ### Test csv row is copied directly from the output_comp_param.csv
      {
        two_twenty_nine_group_id: 'Perimeter_ZN_1_wall_south_Window_2',
        two_twenty_nine_parent_type: 'subsurfaces',
        two_twenty_nine_parent_id: 'PERIMETER_ZN_1_WALL_SOUTH',
        compliance_parameter_category: 'subsurface',
        compliance_parameter_name: 'has_open_sensor1',
        compliance_parameter_value: 'true'
      }
    )
  end


  def test_fill_compliance_parameter_values_in_osm_to_csv
    ## No values in the csv data should been set
    assert_equal @csv_data.sum { |row| row.get_set_count },0

    test_case_string_data_type_row = @csv_data.select { |row_of_csv_data|  (row_of_csv_data[:two_twenty_nine_group_id].downcase == 'ATTIC_FLOOR_CORE'.downcase &&
    row_of_csv_data[:compliance_parameter_name] == "status_type" &&
    row_of_csv_data[:compliance_parameter_category] == "surface"
    ) }

    test_case_boolean_data_type_row = @csv_data.select { |row_of_csv_data|  (row_of_csv_data[:two_twenty_nine_group_id].downcase == 'Perimeter_ZN_1_wall_south_Window_1'.downcase &&
    row_of_csv_data[:compliance_parameter_name] == "has_manual_interior_shades" &&
    row_of_csv_data[:compliance_parameter_category] == "subsurface"
    )}

    csv_data_with_updated_values1 = ParseOsmAdditionalProperties.
    parse_osm_and_place_compliance_parameter_values_in_csv(@test_model, test_case_string_data_type_row)

    csv_data_with_updated_values2 = ParseOsmAdditionalProperties.
    parse_osm_and_place_compliance_parameter_values_in_csv(@test_model, test_case_boolean_data_type_row)

    ## Should now match additional property values in osm for compliance parameter
    assert_equal csv_data_with_updated_values1.first[:compliance_parameter_value],"status_type_updated"
    assert_equal csv_data_with_updated_values2.first[:compliance_parameter_value], false
    ## Assert that data within the csv has been updated twice from the method parse_osm_and_place_compliance_parameter_values_in_csv
    assert_equal @csv_data.sum { |row| row.get_set_count },2

  end
end
