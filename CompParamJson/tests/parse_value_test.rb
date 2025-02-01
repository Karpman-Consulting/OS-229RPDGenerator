require 'minitest/autorun'

require_relative '../generate_csv'

class TestParseValue < Minitest::Test
  def test_parse_float
    assert_equal 123.45, GenerateCompParamJsonCsv.parse_value('123.45')
    assert_equal -123.45, GenerateCompParamJsonCsv.parse_value('-123.45')
    assert_equal 0.0, GenerateCompParamJsonCsv.parse_value('0.0')
  end

  def test_parse_boolean
    assert_equal true, GenerateCompParamJsonCsv.parse_value('true')
    assert_equal true, GenerateCompParamJsonCsv.parse_value('TRUE')
    assert_equal false, GenerateCompParamJsonCsv.parse_value('false')
    assert_equal false, GenerateCompParamJsonCsv.parse_value('FALSE')
  end

  def test_parse_string
    assert_equal 'hello', GenerateCompParamJsonCsv.parse_value('hello')
    assert_equal '123abc', GenerateCompParamJsonCsv.parse_value('123abc')
    assert_equal '', GenerateCompParamJsonCsv.parse_value('')
  end

  def test_parse_edge_cases
    assert_equal 'trueish', GenerateCompParamJsonCsv.parse_value('trueish')
    assert_equal 'falsey', GenerateCompParamJsonCsv.parse_value('falsey')
    assert_equal '123.45.67', GenerateCompParamJsonCsv.parse_value('123.45.67')
  end
end
