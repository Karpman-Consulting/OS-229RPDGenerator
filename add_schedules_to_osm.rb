require 'openstudio'
require 'openstudio-standards'
require 'pry-byebug'

@sch = OpenstudioStandards::Schedules

# Initialize model
model = OpenStudio::Model::Model.new

def array_of_fractions_to_array_of_arrays_with_fractions_and_hours(array_of_fractions)
  array_of_fractions.map.with_index { |value, index| [index + 1, value] }
end


rules = []

rules << ['Sat','1/1-12/31', 'Sat',
array_of_fractions_to_array_of_arrays_with_fractions_and_hours([0, 0, 0, 0, 0, 0, 0.1, 0.1, 0.3, 0.3, 0.3, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.05, 0.05, 0, 0, 0, 0, 0])
.flatten(1)]

rules << ['Sun','1/1-12/31', 'Sun',
array_of_fractions_to_array_of_arrays_with_fractions_and_hours([0, 0, 0, 0, 0, 0, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0, 0, 0, 0, 0, 0])
.flatten(1)]

# Define the schedule data
schedule_data_occ = {
  'name' => '229_occupancy',
  'default_day' => array_of_fractions_to_array_of_arrays_with_fractions_and_hours(
  [0, 0, 0, 0, 0, 0, 0.1, 0.2, 0.95, 0.95, 0.95, 0.95, 0.5, 0.95, 0.95, 0.95, 0.95, 0.3, 0.1, 0.1, 0.1, 0.1, 0.05, 0.05]),
  'rules' => rules
}

#binding.prycle
# Create schedule using create_complex_schedule method
@sch.create_complex_schedule(model,schedule_data_occ)

# Save the model
model_path = 'output_schedules.osm'
model.save(OpenStudio::Path.new(model_path), true)
puts "Model saved to #{model_path}"
