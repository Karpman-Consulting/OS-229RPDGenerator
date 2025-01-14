


### This measure will:

The measure will open the .osm file and search it for instances of “model objects” 
that are associated with compliance parameters. 
The search will be limited to OS Model objects associated with the compliance parameters listed in Appendix A 

For each qualified parent object found, the measure will look for an 
attached OS:AdditionalProperties object. This is an extensible OS object that uses a 
“key, value” structure to attach “generic” data to specific objects within the OpenStudio data model.  

When a pre-existing value for a compliance parameter is found, it will be written (pre-populated) 
in the ‘parameter value’ cell of the row of the .csv file. If a value for the compliance parameter is not found,
 the compliance parameter value cell of the row in the .csv file will be left empty.  


###### (Automatically generated documentation)

# ReadComplianceParameterCsvFromOsm

## Description
Replace this text with an explanation of what the measure does in terms that can be understood by a general building professional audience (building owners, architects, engineers, contractors, etc.).  This description will be used to create reports aimed at convincing the owner and/or design team to implement the measure in the actual building design.  For this reason, the description may include details about how the measure would be implemented, along with explanations of qualitative benefits associated with the measure.  It is good practice to include citations in the measure if the description is taken from a known source or if specific benefits are listed.

## Modeler Description
Replace this text with an explanation for the energy modeler specifically.  It should explain how the measure is modeled, including any requirements about how the baseline model must be set up, major assumptions, citations of references to applicable modeling resources, etc.  The energy modeler should be able to read this description and understand what changes the measure is making to the model and why these changes are being made.  Because the Modeler Description is written for an expert audience, using common abbreviations for brevity is good practice.

## Measure Type
ReportingMeasure

## Taxonomy


## Arguments


### path to empty comp param json file
path to empty comp param json file
**Name:** empty_comp_param_json_file_path,
**Type:** String,
**Units:** ,
**Required:** true,
**Model Dependent:** false


### path to updated comp param json file
path to updated comp param json file
**Name:** updated_comp_param_json_file_path,
**Type:** String,
**Units:** ,
**Required:** true,
**Model Dependent:** false


### csv_file_path
csv_file_path
**Name:** csv_file_path,
**Type:** String,
**Units:** ,
**Required:** true,
**Model Dependent:** false






