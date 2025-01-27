# OpenStudio-229RPDGenerator

## Authors

Anton Szilasi and Chris Balbach of Performance Systems Development of Ithaca, New York

## Purpose
Provides a command-line utility for OpenStudio users to create generate Ruleset Project Description files with supplementary compliance parameter details in a 2-step process.

## Description
This repository provides the application and source code for a compliance wizard which allows users to select OpenStudio .osm files, enter additional compliance details, and create and pre-validate RPD json files for use with the ASHRAE Standard 229 Ruleset Checking Tool (RCT).

Please note that this project is currently in its initial stages of development. It is not yet operational for practical use. We are actively working on its development and enhancement. Contributions, suggestions, and feedback are welcome as we progress towards a fully functional version. Stay tuned for updates and feel free to explore the existing codebase.

A flow chart of the implementation details can be seen at: 
https://app.diagrams.net/#G164sSBaP93pLvT9JOcaHooVvWXyb2Nhdq#%7B%22pageId%22%3A%224B5pT87SY1Ndpzb4Cms2%22%7D

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

### 1. Install Python 3
https://www.python.org/downloads/

### 2. Install Ruby 3.2.2
https://www.ruby-lang.org/en/downloads/releases/

### 3. Install OpenStudio 3.9.0
**IMPORTANT: OpenStudio 3.9.0 is required** - any other version of OpenStudio will very likely cause issues.

**When you are installing the app, ensure that you are also installing the OpenStudio CLI.** The Openstudio-229RPDGenerator uses OpenStudio measures which require the OpenStudio CLI to run. 
https://openstudiocoalition.org/getting_started/getting_started/


**the folder containing the openstudio.exe must exist in the PATH system environment variable** (it may or may not already be there).

Typically, it is the following path:

    C:\openstudio-3.9.0\bin


It is critical that the OpenStudio version and Ruby version are exactly as described. See the OpenStudio compatibility matrix here:  
https://github.com/NREL/OpenStudio/wiki/OpenStudio-SDK-Version-Compatibility-Matrix

### 4. Link OpenStudio to Ruby
https://nrel.github.io/OpenStudio-user-documentation/getting_started/getting_started/  
Under the **Optional - Install Ruby** section, follow the instructions to link OpenStudio to Ruby. For this application to work, this step is mandatory - not optional.

      To link openstudio to your Ruby installation, follow these steps:
      1. Create a text file with the following text inside (modify C:\openstudio-3.9.0 based on where your version of OpenStudio SDK is installed):

        require 'C:\openstudio-3.9.0\Ruby\openstudio.rb'

      2. Save the file as openstudio.rb to C:\ruby-2.7.2-x64-mingw32\lib\ruby\site_ruby\openstudio.rb (or wherever you installed Ruby).

**Alternatively,** 

Create a `RUBYLIB` system environment variable (if it does not exist) and add the path to the folder containing `openstudio.rb`. Typically, the path is:

        C:\openstudio-3.9.0\Ruby

### 5. Install Python dependencies
Run the following command to install the required Python packages:
```bash
pip install -r requirements.txt
```

### 6. Install Ruby dependencies
Run the following command to install the required Ruby packages:
```bash
bundle install
```

## Steps to run the OpenStudio-229RPDGenerator on a OpenStudio model (.osm)

### 1. Create the empty Compliance Parameter csv
Where  `filename.osm` is the OpenStudio model to process, this command will generate a csv named in the format
`filename-empty.csv` which contains all the compliance parameters that may be applicable to the model with their initial values set according to any values which may be stored in OS:AdditionalProperties.

Sample command to create a csv file of the OpenStudio model's compliance parameters:

`python .\createOSRulesetProjectDescription.py create_cp_csv --openstudio_model_path "./test_files/Test_E1.osm" --weather_file_name "USA_CO_Denver.Intl.AP.725650_TMYx.epw" --convert_input_format_exe_path "C:\EnergyPlusV24-2-0\ConvertInputFormat.exe"`

Where:
`--openstudio_model_path` is the path to the openstudio model, i.e. `"./test_files/Test_E1.osm"`. Path can be absolute or relative

`--weather_file_name` is the name of the weather file within the Weather directory (the Weather folder is a sibling to the OpenStudio model), i.e. `"USA_CO_Denver.Intl.AP.725650_TMYx.epw"`

`--convert_intput_format_exe_path` is the path to the EnergyPlus utility ConvertInputFormat, i.e. `"C:\EnergyPlusV24-2-0\ConvertInputFormat.exe"`

### 2. Complete the Compliance Parameter csv

Enter values for compliance parameters that are applicable to your model, and save the csv file.

### 3. Run the command 

If successful this command will produce a validated rpd.json of the OpenStudio model and the compliance parameter values
entered in step 2.

`python .\createOSRulesetProjectDescription.py create_rpd --openstudio_model_path "./test_files/Test_E1.osm" --weather_file_name "USA_CO_Denver.Intl.AP.725650_TMYx.epw" --csv_file_path "xx"`

Where:
`--openstudio_model_path` is the path to the openstudio model, i.e. `"./test_files/Test_E1.osm"`. Path can be absolute or relative

`--weather_file_name` is the name of the weather file within the Weather directory (the Weather folder is a sibling to the OpenStudio model), i.e. `"USA_CO_Denver.Intl.AP.725650_TMYx.epw"`

`--csv_file_path,` the absolute path to the csv file that was saved in Step 2, i.e. `"C:\Users\AntonSzilasi\Documents\OpenStudio20RPD20Generator\Test_E1\run\Test_E1.csv"`


### Development

Code is divided into Ruby for Ruby OpenStudio measures, which are used to generate a 229RPD files from a OpenStudio model

and Python for createOSRulesetProjectDescription.py, which can be used to generate a 229PRD file from a OpenStudio model

run all tests on Ruby measures code by running

"rake"

Run the createOSRulesetProjectDescription.py on all the test files from Appendix E and F of 229 

by running "test_create_os_ruleset_project_description.py" in the tests directory

## Disclaimer Notice
Acknowledgment: This material is based upon work supported by the U.S. Department of Energy’s Office of Energy Efficiency and Renewable Energy (EERE) under the Building Technologies Office - DE-FOA-0002813 - Bipartisan Infrastructure Law Resilient and Efficient Codes Implementation.
Award Number: DE-EE0010949
Abridged Disclaimer: The views expressed herein do not necessarily represent the view of the U.S. Department of Energy or the United States Government.
