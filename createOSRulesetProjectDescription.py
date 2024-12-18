import subprocess
import argparse
import json
from pathlib import Path
import os
import shutil
from rpdvalidator import validate_rpd

def return_open_studio_workflow_read_cp_csv(seed_model_path, 
                                            weather_file_name, 
                                            empty_comp_param_json_file_path,
                                            updated_comp_param_json_file_path,
                                            csv_file_path):
    
    return {
        "seed_file": seed_model_path,
        "weather_file": weather_file_name,
        "measure_paths": [
          "..",
          "../measures/"
        ],
        "file_paths": [
          "../weather",
          "./weather",
          "./seed",
          "."
        ],
        "run_directory": "./run",
        "steps": [
          {
            "measure_dir_name": "read_cp_csv",
            "name": "ReadComplianceParameterCsvFromOsm",
            "arguments": {
              "empty_comp_param_json_file_path": empty_comp_param_json_file_path,
              "updated_comp_param_json_file_path": updated_comp_param_json_file_path,
              "csv_file_path": csv_file_path
            }
          }
        ]
    }

def return_open_studio_workflow_create_cp(seed_model_path, 
                                                      weather_file_name,
                                                      empty_comp_param_json_file_path,
                                                      output_csv_file_path
                                                  ):
    
    return {
        "seed_file": seed_model_path,
        "weather_file": weather_file_name,
        "measure_paths": [
          "..",
          "../measures/"
        ],
        "file_paths": [
          "../weather",
          "./weather",
          "./seed",
          "."
        ],
        "run_directory": "./run",
        "steps": [
          {
            "measure_dir_name": "create_preconditioned_idf",
            "name": "CreatePreconditionedIdf",
            "arguments": {
            }
          },
          {
            "measure_dir_name": "create_cp_csv",
            "name": "CreateComplianceParameterCsvFromOsm",
            "arguments": {
              "empty_comp_param_json_file_path": empty_comp_param_json_file_path,
              'output_csv_file_path': output_csv_file_path
            }
          }
        ]
    }

def is_osw_success(command_args):
    try:
        run_osw = ['openstudio', 'run','-w']
        # Run the command
        if isinstance(command_args, str):
            command_args = [command_args]

        full_command = run_osw + command_args
        subprocess.check_call(full_command)
        
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    parser = argparse.ArgumentParser(description="Run 229 compliance commands")
    #group = parser.add_mutually_exclusive_group(required=True)

    subparsers = parser.add_subparsers(title="Commands", dest="command", required=True)
    ### Create cp csv
    subparsers1 = subparsers.add_parser("create_cp_csv", help="Create CSV with compliance parameters")
    subparsers1.add_argument("--openstudio_model_path", type=str, required=True, help=" The OpenStudio model file path")
    subparsers1.add_argument("--weather_file_name", type=str, required=True, help="weather file name, the weather file must be placed in the weather directory")

    subparsers2 = subparsers.add_parser("create_rpd", help="Read CSV with compliance parameters and validate")
    subparsers2.add_argument("--empty_comp_param_json_file_path", type=str, required=True, help=" The OpenStudio model file path")
    subparsers2.add_argument("--csv_file_path", type=str, required=True, help=" The OpenStudio model file path")
    subparsers2.add_argument("--weather_file_name", type=str, required=True, help="weather file name, the weather file must be placed in the weather directory")
    subparsers2.add_argument("--openstudio_model_path", type=str, required=True, help=" The OpenStudio model file path")

    ### Create rmd
    args = parser.parse_args()
    
    openstudio_model_path = Path(args.openstudio_model_path)
    weather_file_name = args.weather_file_name

    weather_file_path = Path(os.path.join(Path(__file__).resolve().parent, 'weather', weather_file_name))

    if not openstudio_model_path.exists():
        raise FileNotFoundError(f"The seed model file '{openstudio_model_path}' does not exist.")

    if not weather_file_path.exists():
        raise FileNotFoundError(
          f"The weather file '{weather_file_name}' does not exist in the weather directory. "
          "Please ensure that it is placed there."
        )

    analysis_path = Path(__file__).resolve().parent / openstudio_model_path.stem
    analysis_path.mkdir(parents=True, exist_ok=True)
    
    if args.command == "create_cp_csv":

        osw_path = analysis_path / f'{openstudio_model_path.stem}_create_cp_csv.osw'

        path_to_move_osm_to = analysis_path / openstudio_model_path.name

        shutil.copy(str(openstudio_model_path), path_to_move_osm_to)
        # Convert the data to a JSON-formatted string
        empty_comp_param_json_file_path = analysis_path / f'empty_comp_param.json'
        output_csv_file_path = Path(os.path.join(Path(__file__).resolve().parent, 'compliance_parameters.csv'))

        #breakpoint()
        create_cp_csv_osw = json.dumps(
            return_open_studio_workflow_create_cp(
                path_to_move_osm_to.as_posix(),
                weather_file_name,
                empty_comp_param_json_file_path.as_posix(),
                output_csv_file_path.as_posix()
            ),
            indent=4
        )

        # Write the JSON string to a file
        with open(osw_path.as_posix(), "w") as file:
            file.write(create_cp_csv_osw)

        if is_osw_success(osw_path.as_posix()):

            print(f"""\033[92mSuccessfully created the CSV file with compliance parameters for the model 
            {openstudio_model_path.name} please fill in compliance parameter values in the file 
            {openstudio_model_path.name + 'compliance_parameters.csv'} """)
        else:
            print(f"""\033[91mFailed to create the CSV file with compliance parameters for the model {openstudio_model_path.name}, "
                  "please ensure that the openstudio model simulated correctly.\033[0m""")

    elif args.command == "create_rpd":

        osw_path = analysis_path / f'{openstudio_model_path.stem}_create_rpd.osw'

        path_to_move_osm_to = analysis_path / openstudio_model_path.name

        shutil.copy(str(openstudio_model_path), path_to_move_osm_to)


        empty_comp_param_json_file_path = Path(args.empty_comp_param_json_file_path)
        csv_file_path = Path(args.csv_file_path)

        ### User will call - createOSRulesetProjectDescription --create_rmd filename.osm filename_cp-complete.csv 
        ## Requires csv and filename.comp,param json

        shutil.copy(str(openstudio_model_path), str(osw_path.parent / openstudio_model_path.name ))

        weather_file_path = Path(os.path.join(Path(__file__).resolve().parent, 'weather', weather_file_name))

        create_cp_csv_osw = json.dumps(
              return_open_studio_workflow_read_cp_csv(
                  openstudio_model_path, 
                  weather_file_name
              ),
              indent=4
        )

        # Write the JSON string to a file
        with open(osw_path.as_posix(), "w") as file:
            file.write(create_cp_csv_osw)

        if is_osw_success(f'./{openstudio_model_path.stem}/{openstudio_model_path.stem}.osw'):
            pass
        else :
            print("Failed to create the RPD file, please ensure that the openstudio model simulated correctly.")

        ### After this python script will call

        ### Convert .idf file into .epjson format for a given .osm file  -
        # ConvertInputFormat in.idf from (step 4)

        ## Create initial .rmd file for a given .osm file  call energyplus_create_rmd in.epJSON”,  
        # # where “in.epJSON (step 5)

        ## 

        # Step 6

        # In this step, the initial .rmd file generated from the step above will be merged with compliance data retrieved from the validated .csv file. This will be accomplished by transforming the ‘new’ compliance parameter data read from the .csv file (by object class) into json dictionary structures, and merging the json structures into the existing .json structure of the previously generated .rmd file.  

        # The merged file will be named “filename.rmd”. This file will be used as input into the Ruleset Checking Tool being developed by PNNL.  

    # A command will be available to combine merge multiple .RMD files into a single RPD file. This command will take the (3) .RMD file names as command arguments and will produce (output) a single .RPD file.    The command will be called “combine_rmds”. 


if __name__ == "__main__":
  main()