require 'rake/testtask'

# desc 'Run all tests'
Rake::TestTask.new(:test) do |t|
  t.libs << 'test' # Add the test directory to the load path
  t.pattern = '**/*_test.rb' # Pattern to find all test files
  t.verbose = true # Print detailed output
end

# Default task to run tests
task default: :test
