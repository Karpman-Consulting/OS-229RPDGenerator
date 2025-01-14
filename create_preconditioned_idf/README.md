


#### This measure will:

A third EnergyPlus Measure in the workflow will be used to append data to the translated .idf file, 
for EnergyPlus objects that may not be accessible from the OS API/SDK. This EnergyPlus measure will 
have no arguments. This measure will: 


Parse the compliance parameter .csv file to extract the values provided for the “lighting_space_type“, 
“ventilation_space_type“, and “envelope_space_type“, for each OS:Space object.  

Append the “lighting_space_type“, “ventilation_space_type“, and “service_water_heating_space_type“ 
information to the .idf snippet for each space. The resulting .idf snippet for each space should look like this, 
where: 


“Space Type” value maps to the compliance parameter “lighting_space_type“: 

“Tag 1” value maps to the compliance parameter “ventilation_space_type“ 

“Tag 2” value maps to the compliance parameter “service_water_heating_space_type “ 


###### (Automatically generated documentation)

# CreatePreconditionedIdf

## Description
Create pre conditioned idf.

## Modeler Description
Create pre conditioned idf

## Measure Type
ModelMeasure

## Taxonomy


## Arguments




This measure does not have any user arguments



