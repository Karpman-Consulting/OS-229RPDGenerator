import subprocess
import argparse
import json
from pathlib import Path
import os
import shutil
from rpdvalidator import validate_rpd


def return_openstudio_workflow_add_analysis_outputs(seed_model_path, weather_file_name):
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
              "measure_dir_name": "create_preconditioned_idf_energyplus",
              "name": "CreatePreconditionedIdfEnergyPlus",
              "arguments": {
              }
          },
        ],
        "run_options": {
        "fast": False,
        "skip_expand_objects": False,
        "skip_energyplus_preprocess": False
        }
    }

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


def return_open_studio_workflow_create_cp_csv(seed_model_path, 
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
          # {
          #   "measure_dir_name": "create_preconditioned_idf",
          #   "name": "CreatePreconditionedIdf",
          #   "arguments": {
          #   }
          # },
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

def analysis_run_path(analysis_path):
    return analysis_path / 'run'

def inepJSON_path(openstudio_model_path):
    return openstudio_model_path.parent / 'run/in.epJSON'

def idf_path(openstudio_model_path):
    return openstudio_model_path.parent / 'run/in.idf'

def succcessfully_ran_convert_input_format(convert_input_format_exe_path, idf_file_path):
  # IE # C:\EnergyPlusV24-2-0\ConvertInputFormat.exe "full_path/in.idf"
    try:
        subprocess.check_call([convert_input_format_exe_path, idf_file_path])
        return True
    except subprocess.CalledProcessError:
        print(f"Failed to run the command {convert_input_format_exe_path} on {idf_file_path}")
        return False

def create_empty_cp_json_file_success(analysis_run_path):
    # IE # C:\EnergyPlusV24-2-0\ConvertInputFormat.exe "full_path/in.idf"
    breakpoint()
    try:
        subprocess.check_call(['createRulesetProjectDescription','--create_empty_cp', 'in.epJSON'], cwd=analysis_run_path)
        return True
    except subprocess.CalledProcessError:
        print(f"Failed to run the command createRulesetProjectDescript in {analysis_run_path}")
        return False

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
    subparsers1.add_argument("--convert_input_format_exe_path", type=str, required=True, help="The path to the EnergyPlus Convert Input Format executable")
    subparsers1.add_argument("--openstudio_model_path", type=str, required=True, help=" The OpenStudio model file path")
    subparsers1.add_argument("--weather_file_name", type=str, required=True, help="weather file name, the weather file must be placed in the weather directory")

    subparsers2 = subparsers.add_parser("create_rpd", help="Read CSV with compliance parameters and validate")
    subparsers2.add_argument("--openstudio_model_path", type=str, required=True, help=" The OpenStudio model file path")
    subparsers2.add_argument("--weather_file_name", type=str, required=True, help="weather file name, the weather file must be placed in the weather directory")
    subparsers2.add_argument("--csv_file_path", type=str, required=True, help="Csv file path with filled in compliance parameter values")
    subparsers2.add_argument("--empty_comp_param_json_file_path", type=str,required=False, help="The path of the empty compliance parameter json (no updated values)")
    subparsers2.add_argument("--comp_param_json_file_path", type=str, required=False, help="The path of compliance parameter json with updated values")

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

    empty_comp_param_json_file_path = analysis_path / f'empty_cp_{openstudio_model_path.stem}.json'

    if args.command == "create_cp_csv":

        if not Path(args.convert_input_format_exe_path).exists():
            raise FileNotFoundError(f"Could not find executable for "
                                    f"EnergyPlus utility ConvertInputFormat.exe "
                                    f"at {args.convert_input_format_exe_path}")

        simulate_model_with_outputs = analysis_path / f'{openstudio_model_path.stem}_simulate_model.osw'

        path_to_move_osm_to = analysis_path / openstudio_model_path.name

        shutil.copy(str(openstudio_model_path), path_to_move_osm_to)
        # Convert the data to a JSON-formatted string

        run_osm_osw = json.dumps(
            return_openstudio_workflow_add_analysis_outputs(str(path_to_move_osm_to), weather_file_name),
            indent=4
        )

        # Write the JSON string to a file
        with open(simulate_model_with_outputs.as_posix(), "w") as file:
            file.write(run_osm_osw)

        if is_osw_success(simulate_model_with_outputs.as_posix()):
            
            idf_file_path = idf_path(path_to_move_osm_to)

            if not idf_file_path.exists():
                raise FileNotFoundError(f'Could not find the idf file at {idf_file_path}, did the simulation run correctly?')

            if succcessfully_ran_convert_input_format(args.convert_input_format_exe_path, idf_file_path):

                if create_empty_cp_json_file_success(analysis_run_path(analysis_path).as_posix()):

                    create_cp_csv_osw = json.dumps(
                        return_open_studio_workflow_create_cp_csv(
                            path_to_move_osm_to.as_posix(), 
                            weather_file_name,
                            empty_comp_param_json_file_path.as_posix(),
                            args.csv_file_path
                        ),
                        indent=4
                    )

                    # Write the JSON string to a file
                    with open(analysis_path / f'{openstudio_model_path.stem}_create_cp_csv.osw', "w") as file:
                        file.write(create_cp_csv_osw)

                    if is_osw_success(analysis_path / f'{openstudio_model_path.stem}_create_cp_csv.osw'):

                        print(f"""\033[92mSuccessfully created the CSV file with compliance parameters for the model {openstudio_model_path.name} 
                        and have updated the compliance parameter json file #{empty_comp_param_json_file_path.name} with the values.\033[0m""")

                    else:
                        print(f"""\033[91mFailed to create the CSV file with compliance parameters for the model {openstudio_model_path.name}, 
                        please ensure that the openstudio model simulated correctly.\033[0m""")

                else: 
                    print(f"""\033[91m Failed to run command createRulesetProjectDescription to create empty cp json file at path 
                    {analysis_run_path(analysis_path).as_posix()},
                    and try again.\033[0m""")

            else:
                print(f"""\033[91m Failed to convert idf at #{idf_file_path} to .epJson using EnergyPlus
                utilty ConvertInputFormat.exe. Please ensure that the idf file and the path to the exe is correct
                and try again.\033[0m""")

        else:
            print(f"""\033[91mFailed to create the CSV file with compliance parameters for the model {openstudio_model_path.name}, "
                  "please ensure that the openstudio model simulated correctly.\033[0m""")

    elif args.command == "create_rpd":

        osw_path = analysis_path / f'{openstudio_model_path.stem}_create_rpd.osw'

        path_to_move_osm_to = analysis_path / openstudio_model_path.name

        shutil.copy(str(openstudio_model_path), path_to_move_osm_to)

        if not args.csv_file_path.exists():
            raise FileNotFoundError(
                f"The csv file '{args.csv_file_path}' does not exist, the csv with compliance parameter values must be provided, "
                "you can create it by running the command 'create_cp_csv' first."
            )
        
        if args.empty_comp_param_json_file_path is not None:
            empty_comp_param_json_file_path = args.empty_comp_param_json_file_path

        if empty_comp_param_json_file_path.exists():
            raise FileNotFoundError(
              f"comp param json file generated by running the command create_cp_csv first cannot be found "
              f"'{empty_comp_param_json_file_path}' does not exist, this is required."
            )

        if args.comp_param_json_file_path is not None:
            comp_param_json_file_path = args.comp_param_json_file_path

        create_cp_csv_osw = json.dumps(
              return_open_studio_workflow_read_cp_csv(
                  path_to_move_osm_to.as_posix(), 
                  weather_file_name,
                  empty_comp_param_json_file_path.as_posix(),
                  comp_param_json_file_path.as_posix(),
                  args.csv_file_path.as_posix(),
              ),
              indent=4
        )

        # Write the JSON string to a file
        with open(osw_path.as_posix(), "w") as file:
            file.write(create_cp_csv_osw)

        if is_osw_success(osw_path.as_posix()):

            print(f"""\033[92mSuccessfully read the CSV file with compliance parameters values for the model 
            {openstudio_model_path.name} 
            and have updated the compliance parameter json file #{comp_param_json_file_path.name}
            with the values. 
            Attempting to validate with rpd validator
            """)

            validate_rpd()

        else:
            print(f"""\033[91mFailed to read the CSV file with compliance parameters
             values for the model {openstudio_model_path.name}, .\033[0m""")

if __name__ == "__main__":
  main()