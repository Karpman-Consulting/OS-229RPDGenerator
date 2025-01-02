# insert your copyright here

require 'openstudio'
require 'openstudio/measure/ShowRunnerOutput'
require 'minitest/autorun'
require_relative '../measure.rb'
require 'fileutils'


class TestSetValuesToEmpty < Minitest::Test
  def test_set_values_to_empty_with_hash
    input = {
      "name" => "Building",
      "id" => 123,
      "details" => {
        "location" => "City",
        "id" => 456
      }
    }
    expected_output = {
      "name" => "",
      "id" => 123,
      "details" => {
        "location" => "",
        "id" => 456
      }
    }
    assert_equal expected_output, ReadComplianceParameterCsvFromOsm.set_values_to_empty(input)
  end

  def test_set_values_to_empty_with_array
    input = [
      {
        "name" => "Building",
        "id" => 123
      },
      {
        "location" => "City",
        "id" => 456
      }
    ]
    expected_output = [
      {
        "name" => "",
        "id" => 123
      },
      {
        "location" => "",
        "id" => 456
      }
    ]
    assert_equal expected_output, ReadComplianceParameterCsvFromOsm.set_values_to_empty(input)
  end

  def test_set_values_to_empty_with_nested_array
    input = {
      "name" => "Building",
      "id" => 123,
      "details" => [
        {
          "location" => "City",
          "id" => 456
        },
        {
          "location" => "Town",
          "id" => 789
        }
      ]
    }
    expected_output = {
      "name" => "",
      "id" => 123,
      "details" => [
        {
          "location" => "",
          "id" => 456
        },
        {
          "location" => "",
          "id" => 789
        }
      ]
    }
    assert_equal expected_output, ReadComplianceParameterCsvFromOsm.set_values_to_empty(input)
  end
end
