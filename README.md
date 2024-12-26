OpenStudio-229RPDGenerator


This repository provides the application and source code for a compliance wizard which allows users to select OpenStudio .osm files, enter additional compliance details, and create and pre-validate RPD json files for use with the ASHRAE Standard 229 Ruleset Checking Tool (RCT).

Please note that this project is currently in its initial stages of development. It is not yet operational for practical use. We are actively working on its development and enhancement. Contributions, suggestions, and feedback are welcome as we progress towards a fully functional version. Stay tuned for updates and feel free to explore the existing codebase.

About ASHRAE 229P
ASHRAE Standard 229P is a proposed standard entitled "Protocols for Evaluating Ruleset Implementation in Building Performance Modeling Software". To learn more about the title/scope/purpose and status of the proposed standard development visit the standards project committee site at ASHRAE SPC 229.

ASHRAE Standard 229 RPD Schema
The RPD schema development continues at: https://github.com/open229/ruleset-model-description-schema

ASHRAE Standard 229 RCT
The RCT development continues at: https://github.com/pnnl/ruleset-checking-tool/tree/develop

This is an early alpha version and is highly unstable!

This package will change significantly during the next several versions.


Using the OpenStudio-229RPDGenerator

Setup:
    1. The Openstudio-229RPDGenerator contains OpenStudio measures which requires the OpenStudio CLI to run,
    which be installed through the OpenStudio app, please see here: https://openstudiocoalition.org/getting_started/getting_started/
    
    Please ensure that when you are installing the app that you are also installing the CLI.
    
    2. The Openstudio-229RPDGenerator requires Python3 and Ruby 3.2.2 installed

    3. Run `bundle install` to install Ruby dependencies

    4. Run `pip install -r requirements.txt` to install Python dependencies



1. Run command

python .\createOSRulesetProjectDescription.py create_cp_csv --openstudio_model_path "./test_files/Test_E1.osm" --weather_file_name "USA_CO_Denver.Intl.AP.725650_TMYx.epw" --convert_input_format_exe_path "C:\EnergyPlusV24-2-0\ConvertInputFormat.exe"

Where:
--openstudio_model_path is the path to the openstudio model ie "./test_files/Test_E1.osm"
--weather_file_name "USA_CO_Denver.Intl.AP.725650_TMYx.epw" ie a weather file places in the directory weather
--convert_intput_format_exe_path, The path to the EnergyPlus utility ConvertInputFormat ie "C:\EnergyPlusV24-2-0\ConvertInputFormat.exe"

where  filename.osm is osm to process, this command will generate a csv 
filename_cp-empty.csv

2. Open filename_cp-empty.csv, enter values in the compliance parameter value column, these values will be read back into the comp-param json

3. Run the command 

Developing the OpenStudio-229RPDGenerator


This package is developed using Pipenv to manage packages during the build process. First, make sure Pipenv is installed on your system using the following commands. Any new dependencies that are added to the package must be included in the Pipfile. The package is currently being developed for Python 3.11. IMPORTANT - 32-bit version of Python must be installed on your machine and selected as your interpreter for Pipenv to work properly.

Install pipenv using pip with the following command. pip install pipenv

All project dependencies can be installed with the following command. pipenv install --dev

Developer Notes
GitFlow
Long-running branches include the default branch development, and the production branch main. All other branches are short-lived branches that should be deleted after merging into development. The development branch will merge into the main branch only for major releases.

Branch and Pull Request naming convention:
The branch or PR name should have the form: FEATURE/INITIALS/DESCRIPTOR
FEATURE is one of the following:

ENG: (Engine) for changes related to core algorithms and data structures
RI: (Read Input) for changes related to the processing of DOE-2 input files
RO: (Read Output) for changes related to the processing of DOE-2 output files
GUI: (Graphic User Inteface) for changes related to the application interface
REF: (Refactoring/Reference) for changes related to nonfunctional attributes of the software (renaming files or variables, restructuring files or directories, or functions related to processing of DOE2/schema reference documentation)
INIITIALS refers to the initials of the owner of the branch or PR.

Disclaimer Notice
Acknowledgment: This material is based upon work supported by the U.S. Department of Energy’s Office of Energy Efficiency and Renewable Energy (EERE) under the Building Technologies Office - DE-FOA-0002813 - Bipartisan Infrastructure Law Resilient and Efficient Codes Implementation.
Award Number: DE-EE0010949
Abridged Disclaimer: The views expressed herein do not necessarily represent the view of the U.S. Department of Energy or the United States Government.









3. createOSRulesetProjectDescription --create_rmd filename.osm filename_cp-complete.csv 

----

Dependencies

https://github.com/JasonGlazer/createRulesetProjectDescription

-----

Resources

https://github.com/JasonGlazer/createRulesetProjectDescription


https://github.com/open229/ruleset-model-description-schema

Two commands



createOSRulesetProjectDescription --create_rmd 

