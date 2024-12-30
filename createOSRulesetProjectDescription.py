import subprocess
import argparse
import json
from pathlib import Path, WindowsPath
import os
import shutil
from pprint import pprint
from rpdvalidator.validate import schema_validate


def return_openstudio_workflow_simulate_model_and_add_analysis_outputs(
    seed_model_path, weather_file_name
):
    return {
        "seed_file": seed_model_path,
        "weather_file": weather_file_name,
        "measure_paths": ["..", "../measures/"],
        "file_paths": ["../weather", "./weather", "./seed", "."],
        "run_directory": "./run",
        "steps": [
            {
                "measure_dir_name": "create_preconditioned_idf",
                "name": "CreatePreconditionedIdf",
                "arguments": {},
            },
            {
                "measure_dir_name": "create_preconditioned_idf_energyplus",
                "name": "CreatePreconditionedIdfEnergyPlus",
                "arguments": {},
            },
        ],
        "run_options": {
            "fast": False,
            "skip_expand_objects": False,
            "skip_energyplus_preprocess": False,
        },
    }


def return_open_studio_workflow_read_cp_csv(
    seed_model_path,
    weather_file_name,
    empty_comp_param_json_file_path,
    updated_comp_param_json_file_path,
    csv_file_path,
):

    return {
        "seed_file": seed_model_path,
        "weather_file": weather_file_name,
        "measure_paths": ["..", "../measures/"],
        "file_paths": ["../weather", "./weather", "./seed", "."],
        "run_directory": "./run",
        "steps": [
            {
                "measure_dir_name": "read_cp_csv",
                "name": "ReadComplianceParameterCsvFromOsm",
                "arguments": {
                    "empty_comp_param_json_file_path": empty_comp_param_json_file_path,
                    "updated_comp_param_json_file_path": updated_comp_param_json_file_path,
                    "csv_file_path": csv_file_path,
                },
            }
        ],
    }


def return_open_studio_workflow_create_cp_csv(
    seed_model_path,
    weather_file_name,
    empty_comp_param_json_file_path,
    output_csv_file_path,
):
    return {
        "seed_file": seed_model_path,
        "weather_file": weather_file_name,
        "measure_paths": ["..", "../measures/"],
        "file_paths": ["../weather", "./weather", "./seed", "."],
        "run_directory": "./run",
        "steps": [
            {
                "measure_dir_name": "create_cp_csv",
                "name": "CreateComplianceParameterCsvFromOsm",
                "arguments": {
                    "empty_comp_param_json_file_path": empty_comp_param_json_file_path,
                    "output_csv_file_path": output_csv_file_path,
                },
            }
        ],
    }


def analysis_run_path(analysis_path):
    return analysis_path / "run"


def inepJSON_path(openstudio_model_path):
    return openstudio_model_path.parent / "run/in.epJSON"


def idf_path(openstudio_model_path):
    return openstudio_model_path.parent / "run/in.idf"


def empty_comp_param_json_path(openstudio_model_path):
    return openstudio_model_path.parent / "run/in.comp-param-empty.json"


def construct_csv_file_path(openstudio_model_path):

    return openstudio_model_path.parent / f"run/{openstudio_model_path.stem}-empty.csv"


def succcessfully_ran_convert_input_format(
    convert_input_format_exe_path, idf_file_path
):
    """
    Runs the ConvertInputFormat executable on the specified IDF file to produce in.epJSON
    and checks if it ran successfully.

    Args:
        convert_input_format_exe_path (str): The full path to the ConvertInputFormat executable.
        idf_file_path (str): The full path to the IDF file to be converted.

    Returns:
        bool: True if the command ran successfully, False otherwise.

    Raises:
        subprocess.CalledProcessError: If the command fails to execute.
    """
    # IE # C:\EnergyPlusV24-2-0\ConvertInputFormat.exe "full_path/in.idf"
    try:
        subprocess.check_call([convert_input_format_exe_path, idf_file_path])
        return True
    except subprocess.CalledProcessError:
        print(
            f"Failed to run the command {convert_input_format_exe_path} on {idf_file_path}"
        )
        return False


def create_empty_cp_json_file_success(analysis_run_path):
    """
    Attempts to create an empty cp JSON file by running the 'createRulesetProjectDescription' command.

    Args:
        analysis_run_path (str): The path to the directory where the command should be executed.

    Returns:
        bool: True if the command was executed successfully, False otherwise.

    Raises:
        subprocess.CalledProcessError: If the command execution fails.
    """
    try:
        subprocess.check_call(
            ["createRulesetProjectDescription", "--create_empty_cp", "in.epJSON"],
            cwd=analysis_run_path,
        )
        return True
    except subprocess.CalledProcessError:
        print(
            f"Failed to run the command createRulesetProjectDescription --create_empty_cp in {analysis_run_path}"
        )
        return False


def create_add_cp_json_file_success(analysis_run_path):
    try:
        subprocess.check_call(
            ["createRulesetProjectDescription", "--add_cp", "in.epJSON"],
            cwd=analysis_run_path,
        )
        return True
    except subprocess.CalledProcessError:
        return False


def remove_output_object(json_file_path):
    # Read the JSON file
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    # Remove the 'output' object if it exists
    for description in data.get("ruleset_model_descriptions", []):
        if "output" in description:
            del description["output"]

    # Write the modified JSON data back to the file
    with open(json_file_path, 'w') as file:
        json.dump(data, file, indent=4)


def is_osw_success(
    osw, path_to_osw, measures_only=False, reporting_measures_only=False
):
    """
    Determines if an OpenStudio Workflow (OSW) run is successful.
    This function writes the OSW JSON string to a file, constructs the appropriate
    command to run the OSW using the OpenStudio CLI, and executes the command.
    It returns True if the OSW run is successful, and False otherwise.
    Args:
        osw (str): The OSW JSON string to be written to a file.
        path_to_osw (str): The path to the OSW file.
        measures_only (bool, optional): If True, only the measures will be run. Defaults to False.
        reporting_measures_only (bool, optional): If True, only the reporting measures will be run. Defaults to False.
    Returns:
        bool: True if the OSW run is successful, False otherwise.
    Raises:
        ValueError: If both measures_only and reporting_measures_only are set to True.
    """

    if isinstance(path_to_osw, WindowsPath):
        raise ValueError("Path to OSW must be a string or array of strings")
    # Write the JSON string to a file
    with open(path_to_osw, "w") as file:
        file.write(osw)

    try:
        run_osw = ["openstudio", "run", "-w"]

        if measures_only and reporting_measures_only:
            raise ValueError(
                "Only one of measures_only and reporting_measures_only can be True."
            )

        if measures_only:
            run_osw = ["openstudio", "run", "--measures_only", "-w"]
        if reporting_measures_only:
            run_osw = ["openstudio", "run", "--postprocess_only", "-w"]

        command_args = path_to_osw
        # Run the command
        if isinstance(path_to_osw, str):
            command_args = [path_to_osw]
        full_command = run_osw + command_args
        subprocess.check_call(full_command)

        return True
    except subprocess.CalledProcessError:
        return False


def get_resource_path(script_arg, default_path=None):

    if script_arg is None and default_path is None:
        raise ValueError("You must provide either a script_arg or a default_path")

    if script_arg is None:

        if not Path(default_path).exists():

            raise FileNotFoundError(
                f"Attempted to find {Path(default_path).name} at {default_path}, as you did not specify a path in the command arguments "
                f"but could not find the file {default_path}, something went wrong sorry"
            )
        else:
            return Path(default_path)

    else:
        if not Path(script_arg).exists():
            raise FileNotFoundError(
                f"The file '{script_arg}' which you specified in the command arguements does not exist."
            )


def main():
    parser = argparse.ArgumentParser(description="Run 229 compliance commands")
    # group = parser.add_mutually_exclusive_group(required=True)

    subparsers = parser.add_subparsers(title="Commands", dest="command", required=True)
    # Create cp csv
    subparsers1 = subparsers.add_parser(
        "create_cp_csv", help="Create CSV with compliance parameters"
    )
    subparsers1.add_argument(
        "--convert_input_format_exe_path",
        type=str,
        required=True,
        help="The path to the EnergyPlus Convert Input Format executable",
    )
    subparsers1.add_argument(
        "--openstudio_model_path",
        type=str,
        required=True,
        help=" The OpenStudio model file path",
    )
    subparsers1.add_argument(
        "--weather_file_name",
        type=str,
        required=True,
        help="weather file name, the weather file must be placed in the weather directory",
    )

    subparsers2 = subparsers.add_parser(
        "create_rpd", help="Read CSV with compliance parameters and validate"
    )
    subparsers2.add_argument(
        "--openstudio_model_path",
        type=str,
        required=True,
        help=" The OpenStudio model file path",
    )
    subparsers2.add_argument(
        "--weather_file_name",
        type=str,
        required=True,
        help="weather file name, the weather file must be placed in the weather directory",
    )
    subparsers2.add_argument(
        "--csv_file_path",
        type=str,
        required=True,
        help="Csv file path with filled in compliance parameter values",
    )
    subparsers2.add_argument(
        "--empty_comp_param_json_file_path",
        type=str,
        required=False,
        help="The path of the empty compliance parameter json (no updated values)",
    )
    subparsers2.add_argument(
        "--comp_param_json_file_path",
        type=str,
        required=False,
        help="The path of compliance parameter json with updated values",
    )

    # Create rmd
    args = parser.parse_args()

    openstudio_model_path = Path(args.openstudio_model_path)
    weather_file_name = args.weather_file_name

    script_dir_path = Path(__file__).resolve().parent

    weather_file_path = Path(
        os.path.join(script_dir_path, "weather", weather_file_name)
    )

    if not openstudio_model_path.exists():
        raise FileNotFoundError(
            f"The seed model file '{openstudio_model_path}' does not exist."
        )

    if not weather_file_path.exists():
        raise FileNotFoundError(
            f"The weather file '{weather_file_name}' does not exist in the weather directory. "
            "Please ensure that it is placed there."
        )

    analysis_path = script_dir_path / openstudio_model_path.stem
    analysis_path.mkdir(parents=True, exist_ok=True)

    empty_comp_param_json_file_path = empty_comp_param_json_path(openstudio_model_path)

    if args.command == "create_cp_csv":

        if not Path(args.convert_input_format_exe_path).exists():
            raise FileNotFoundError(
                f"Could not find executable for "
                f"EnergyPlus utility ConvertInputFormat.exe "
                f"at {args.convert_input_format_exe_path}"
            )

        simulate_model_with_outputs = (
            analysis_path / f"{openstudio_model_path.stem}_simulate_model.osw"
        )

        path_to_move_osm_to = analysis_path / openstudio_model_path.name

        shutil.copy(str(openstudio_model_path), path_to_move_osm_to)

        if is_osw_success(
            json.dumps(
                return_openstudio_workflow_simulate_model_and_add_analysis_outputs(
                    str(path_to_move_osm_to), weather_file_name
                ),
                indent=4,
            ),
            simulate_model_with_outputs.as_posix(),
        ):

            idf_file_path = idf_path(path_to_move_osm_to)

            if not idf_file_path.exists():
                raise FileNotFoundError(
                    f"Could not find the idf file at {idf_file_path}, did the simulation run correctly?"
                )

            if succcessfully_ran_convert_input_format(
                args.convert_input_format_exe_path, idf_file_path
            ):

                if create_empty_cp_json_file_success(
                    analysis_run_path(analysis_path).as_posix()
                ):

                    if is_osw_success(
                        json.dumps(
                            return_open_studio_workflow_create_cp_csv(
                                path_to_move_osm_to.as_posix(),
                                weather_file_name,
                                empty_comp_param_json_path(
                                    path_to_move_osm_to
                                ).as_posix(),
                                construct_csv_file_path(path_to_move_osm_to).as_posix(),
                            ),
                            indent=4,
                        ),
                        (
                            analysis_path
                            / f"{openstudio_model_path.stem}_create_cp_csv.osw"
                        ).as_posix(),
                        measures_only=False,
                        reporting_measures_only=True,
                    ):
                        print(
                            f"""\n\n\033[92mSuccessfully created the CSV file with compliance parameters for the model {openstudio_model_path.name} 
                        and have updated the compliance parameter json file {empty_comp_param_json_file_path.name} with the values.\033[0m"""
                        )

                    else:
                        print(
                            f"""\n\n\033[91mFailed to create the CSV file with compliance parameters for the model 
                            {openstudio_model_path.name}, please ensure that the openstudio model simulated correctly.\033[0m"""
                        )

                else:
                    print(
                        f"""\n\n\033[91m Failed to run command createRulesetProjectDescription to create empty cp json file at path 
                    {analysis_run_path(analysis_path).as_posix()},
                    and try again.\n\n\033[0m"""
                    )

            else:
                print(
                    f"""\n\n\033[91m Failed to convert idf at #{idf_file_path} to .epJson using EnergyPlus
                utilty ConvertInputFormat.exe. Please ensure that the idf file and the path to the exe is correct
                and try again.\n\n\033[0m"""
                )

        else:
            print(
                f"""\n\n\033[91mFailed to create the CSV file with compliance parameters for the model 
            {openstudio_model_path.name}, "
                  "please ensure that the openstudio model simulated correctly.\n\n\033[0m"""
            )

    elif args.command == "create_rpd":

        osw_path = analysis_path / f"{openstudio_model_path.stem}_create_rpd.osw"

        path_to_move_osm_to = analysis_path / openstudio_model_path.name

        shutil.copy(str(openstudio_model_path), path_to_move_osm_to)

        csv_file_path = args.csv_file_path

        if not Path(args.csv_file_path).exists():
            raise FileNotFoundError(f"Could not find csv file at {args.csv_file_path}")

        empty_comp_param_json_file_path = get_resource_path(
            args.empty_comp_param_json_file_path,
            default_path=f"{analysis_run_path(analysis_path)}/in.comp-param-empty.json",
        )

        if args.comp_param_json_file_path is None:
            # Create a default path
            comp_param_json_file_path = Path(
                f"{analysis_run_path(analysis_path)}/in.comp-param.json"
            )
        else:
            comp_param_json_file_path = Path(args.comp_param_json_file_path)

        if is_osw_success(
            json.dumps(
                return_open_studio_workflow_read_cp_csv(
                    path_to_move_osm_to.as_posix(),
                    weather_file_name,
                    empty_comp_param_json_file_path.as_posix(),
                    comp_param_json_file_path.as_posix(),
                    csv_file_path,
                ),
                indent=4,
            ),
            osw_path.as_posix(),
            measures_only=False,
            reporting_measures_only=True,
        ):

            print(
                f"""\n\n\033[92mSuccessfully read the CSV file with compliance parameters values for the model 
            {openstudio_model_path.name} 
            and have updated the compliance parameter json file {comp_param_json_file_path}
            with the values. 
            Attempting to validate with rpd validator
            """
            )
            remove_output_object(comp_param_json_file_path.as_posix())
            # in.comp-param.json

            if not comp_param_json_file_path.exists():
                raise FileNotFoundError(f"Could not find in.comp-param.json at {comp_param_json_file_path.as_posix()}")

            result = schema_validate(json.load(open(comp_param_json_file_path.as_posix(), 'r')))

            if result['passed']:

                print(
                    f"""\033[92mThe compliance parameter json file {comp_param_json_file_path.name} 
                for the model {openstudio_model_path.name} has passed validation with details {result}.\033[0m"""
                )

                if create_add_cp_json_file_success(analysis_run_path(analysis_path).as_posix()):
                    print(
                            f"""\033[92m Successfully generated rpd.json at {analysis_run_path(analysis_path).as_posix()}
                             \033[0m"""
                        )
                else:
                    print(
                            """\033[91m Failed to generate rpd.json!\033[0m"""
                        )
            else:

                print(
                    f"""\033[91mThe compliance parameter json file {comp_param_json_file_path.name} 
                for the model {openstudio_model_path.name} 
                at path {analysis_run_path(analysis_path).as_posix()} 
                has failed validation with {len(result['errors'])} please see below \n\n.\033[0m"""
                )

                for index, error in enumerate(result['errors']):
                    print(f"\033[91m-{index+1}. {error}\033[0m""\n")

        else:
            print(
                f"""\033[91mFailed to read the CSV file with compliance parameters
             values for the model {openstudio_model_path.name}, .\033[0m"""
            )


if __name__ == "__main__":
    main()
