# OpenStudio-229RPDGenerator

This repository provides the application and source code for a compliance wizard which allows users to select OpenStudio .osm files, enter additional compliance details, and create and pre-validate RPD json files for use with the ASHRAE Standard 229 Ruleset Checking Tool (RCT).

Please note that this project is currently in its initial stages of development. It is not yet operational for practical use. We are actively working on its development and enhancement. Contributions, suggestions, and feedback are welcome as we progress towards a fully functional version. Stay tuned for updates and feel free to explore the existing codebase.

# About ASHRAE 229P
ASHRAE Standard 229P is a proposed standard entitled "Protocols for Evaluating Ruleset Implementation in Building Performance Modeling Software". To learn more about the title/scope/purpose and status of the proposed standard development visit the standards project committee site at ASHRAE SPC 229.

ASHRAE Standard 229 RPD Schema
The RPD schema development continues at: https://github.com/open229/ruleset-model-description-schema

ASHRAE Standard 229 RCT
The RCT development continues at: https://github.com/pnnl/ruleset-checking-tool/tree/develop

This is an early alpha version and is highly unstable!

This package will change significantly during the next several versions.

# Using the OpenStudio-229RPDGenerator

## Setup

### 1. 
The Openstudio-229RPDGenerator contains OpenStudio measures which requires the OpenStudio CLI to run,
which be installed through the OpenStudio app, please see here: https://openstudiocoalition.org/getting_started/getting_started/

    Please ensure that when you are installing the app that you are also installing the OpenStudio CLI.

### 2. 
The Openstudio-229RPDGenerator requires Python3 > 3.13 and Ruby 3.2.2 installed

### 3. 
Run `bundle install` to install Ruby dependencies

### 4. 
Run `pip install -r requirements.txt` to install Python dependencies

## Steps to run the OpenStudio-229RPDGenerator on a OpenStudio model (.osm)

### 1. 
Run command, to create a csv file of the OpenStudio model's compliance parameters

    python .\createOSRulesetProjectDescription.py create_cp_csv --openstudio_model_path "./test_files/Test_E1.osm" --weather_file_name "USA_CO_Denver.Intl.AP.725650_TMYx.epw" --convert_input_format_exe_path "C:\EnergyPlusV24-2-0\ConvertInputFormat.exe"

Where:
--openstudio_model_path is the path to the openstudio model ie "./test_files/Test_E1.osm", can be absolute or relative

--weather_file_name "USA_CO_Denver.Intl.AP.725650_TMYx.epw" ie a weather file places in the directory weather

--convert_intput_format_exe_path, The path to the EnergyPlus utility ConvertInputFormat ie "C:\EnergyPlusV24-2-0\ConvertInputFormat.exe"

where  filename.osm is osm to process, this command will generate a csv named in the format
filename_cp-empty.csv which contains all the compliance parameters of a particular .osm where compliance parameters
set in the osm using the OS:AdditionalProperties will be prefilled in the csv

### 2. Open the filename_cp-empty.csv

Enter values in the compliance parameter value column, these values will be used in step 3.

### 3. Run the command 

    python .\createOSRulesetProjectDescription.py create_rpd --openstudio_model_path "./test_files/Test_E1.osm" --weather_file_name "USA_CO_Denver.Intl.AP.725650_TMYx.epw" --csv_file_path "xx"

Where:
--openstudio_model_path is the path to the openstudio model ie "./test_files/Test_E1.osm", can be absolute or relative

--weather_file_name "USA_CO_Denver.Intl.AP.725650_TMYx.epw" ie a weather file places in the directory weather

--csv_file_path, the absolute path to the csv were values in 2. where entered ie "C:\Users\AntonSzilasi\Documents\OpenStudio20RPD20Generator\Test_E1\run\Test_E1.csv"

If successful this command will produce a validated rpd.json of the OpenStudio model and the compliance parameter values
entered in step 2.



## Tests, run all tests by running "rake"

## Disclaimer Notice
Acknowledgment: This material is based upon work supported by the U.S. Department of Energy’s Office of Energy Efficiency and Renewable Energy (EERE) under the Building Technologies Office - DE-FOA-0002813 - Bipartisan Infrastructure Law Resilient and Efficient Codes Implementation.
Award Number: DE-EE0010949
Abridged Disclaimer: The views expressed herein do not necessarily represent the view of the U.S. Department of Energy or the United States Government.
