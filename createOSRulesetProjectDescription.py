import sys
import subprocess
import argparse
import json
from pathlib import Path, WindowsPath
import os
import shutil
from rpdvalidator.validate import schema_validate


def return_openstudio_workflow_simulate_model_and_add_analysis_outputs(
    seed_model_path: str,
    weather_file_name: str
) -> dict:
    return {
        "seed_file": seed_model_path,
        "weather_file": weather_file_name,
        "measure_paths": ["..", "../measures/", "../..", "../../.."],
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
    seed_model_path: str,
    weather_file_name: str,
    empty_comp_param_json_file_path: str,
    updated_comp_param_json_file_path: str,
    csv_file_path: str
) -> dict:
    return {
        "seed_file": seed_model_path,
        "weather_file": weather_file_name,
        "measure_paths": ["..", "../measures/", "../..", "../../.."],
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
    seed_model_path: str,
    weather_file_name: str,
    empty_comp_param_json_file_path: str,
    output_csv_file_path: str
) -> dict:
    return {
        "seed_file": seed_model_path,
        "weather_file": weather_file_name,
        "measure_paths": ["..", "../measures/", "../..", "../../.."],
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


def analysis_run_path(analysis_path: Path) -> Path:
    return analysis_path / "run"


def in_epjson_path(openstudio_model_path: Path) -> Path:
    return openstudio_model_path.parent / "run" / "in.epJSON"


def idf_path(openstudio_model_path: Path) -> Path:
    return openstudio_model_path.parent / "run" / "in.idf"


def empty_comp_param_json_path(openstudio_model_path: Path) -> Path:
    return openstudio_model_path.parent / "run" / "in.comp-param-empty.json"


def construct_csv_file_path(openstudio_model_path: Path) -> Path:
    return openstudio_model_path.parent / "run" / f"{openstudio_model_path.stem}-empty.csv"


def succcessfully_ran_convert_input_format(
    convert_input_format_exe_path: str,
    idf_file_path: Path
) -> bool:
    """
    Runs the ConvertInputFormat executable on the specified IDF file to produce in.epJSON
    and checks if it ran successfully.
    Returns True if successful, False otherwise.
    """
    try:
        subprocess.check_call(
            [sys.executable, "-m", convert_input_format_exe_path, idf_file_path],
            env=os.environ
        )
        return True
    except subprocess.CalledProcessError:
        print(
            f"Failed to run the command {convert_input_format_exe_path} on {idf_file_path}"
        )
        return False


def create_empty_cp_json_file_success(analysis_run_path_str: str) -> bool:
    """
    Attempts to create an empty cp JSON file by running the 'createRulesetProjectDescription' command.
    Returns True if successful, False otherwise.
    """
    try:
        subprocess.check_call(
            [
                sys.executable,
                "-m",
                "createRulesetProjectDescription",
                "--create_empty_cp",
                "in.epJSON",
            ],
            cwd=analysis_run_path_str,
            env=os.environ
        )
        return True
    except subprocess.CalledProcessError:
        print(
            f"Failed to run the command createRulesetProjectDescription --create_empty_cp in {analysis_run_path}"
        )
        return False


def create_add_cp_json_file_success(analysis_run_path_str: str) -> bool:
    try:
        subprocess.check_call(
            [
                sys.executable,
                "-m",
                "createRulesetProjectDescription",
                "--add_cp",
                "in.epJSON",
            ],
            cwd=analysis_run_path_str,
            env=os.environ
        )
        return True
    except subprocess.CalledProcessError:
        return False


def remove_output_object(json_file_path):
    # Read the JSON file
    with open(json_file_path, "r") as file:
        data = json.load(file)

    # Remove the 'output' object if it exists
    for description in data.get("ruleset_model_descriptions", []):
        if "output" in description:
            del description["output"]

    # Write the modified JSON data back to the file
    with open(json_file_path, "w") as file:
        json.dump(data, file, indent=4)


def is_osw_success(
    osw_content: str,
    path_to_osw: str,
    measures_only: bool = False,
    reporting_measures_only: bool = False
) -> bool:
    """
    Determines if an OpenStudio Workflow (OSW) run is successful.
    This function writes the OSW JSON string to a file, constructs the appropriate
    command to run the OSW using the OpenStudio CLI, and executes the command.
    It returns True if the OSW run is successful, and False otherwise.
    Args:
        osw_content (str): The OSW JSON string to be written to a file.
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
        file.write(osw_content)

    try:
        run_osw = ["openstudio", "run", "-w"]

        if measures_only and reporting_measures_only:
            raise ValueError(
                "Only one of measures_only and reporting_measures_only can be True."
            )

        if measures_only:
            run_osw = [
                sys.executable,
                "-m",
                "openstudio",
                "run",
                "--measures_only",
                "-w",
            ]
        if reporting_measures_only:
            run_osw = [
                sys.executable,
                "-m",
                "openstudio",
                "run",
                "--postprocess_only",
                "-w",
            ]

        command_args = path_to_osw
        # Run the command
        if isinstance(path_to_osw, str):
            command_args = [path_to_osw]
        full_command = run_osw + command_args
        subprocess.check_call(
            full_command,
            env=os.environ
        )
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
                f"but could not find the file {default_path}"
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
    subparsers = parser.add_subparsers(title="Commands", dest="command", required=True)

    # --------------------- create_cp_csv Subcommand --------------------- #
    create_cp_csv_parser = subparsers.add_parser(
        "create_cp_csv",
        help="Create CSV with compliance parameters"
    )
    create_cp_csv_parser.add_argument(
        "--convert_input_format_exe_path",
        type=str,
        required=True,
        help="Path to the EnergyPlus Convert Input Format executable"
    )
    create_cp_csv_parser.add_argument(
        "--openstudio_model_path",
        type=str,
        required=True,
        help="Path to the OpenStudio model file"
    )
    create_cp_csv_parser.add_argument(
        "--weather_file_name",
        type=str,
        required=True,
        help="Weather file name (must exist in the 'weather' directory)"
    )
    create_cp_csv_parser.add_argument(
        "--base_dir",
        default=os.getcwd(),
        help="Base directory for relative paths (defaults to current working directory)"
    )

    # --------------------- create_rpd Subcommand --------------------- #
    create_rpd_parser = subparsers.add_parser(
        "create_rpd",
        help="Read CSV with compliance parameters and validate"
    )
    create_rpd_parser.add_argument(
        "--openstudio_model_path",
        type=str,
        required=True,
        help="Path to the OpenStudio model file"
    )
    create_rpd_parser.add_argument(
        "--weather_file_name",
        type=str,
        required=True,
        help="Weather file name (must exist in the 'weather' directory)"
    )
    create_rpd_parser.add_argument(
        "--csv_file_path",
        type=str,
        required=True,
        help="Path to the CSV file containing compliance parameter values"
    )
    create_rpd_parser.add_argument(
        "--empty_comp_param_json_file_path",
        type=str,
        required=False,
        help="Path to the empty compliance parameter JSON (contains no updated values)"
    )
    create_rpd_parser.add_argument(
        "--comp_param_json_file_path",
        type=str,
        required=False,
        help="Path to the compliance parameter JSON with updated values"
    )
    create_rpd_parser.add_argument(
        "--base_dir",
        default=os.getcwd(),
        help="Base directory for relative paths (defaults to current working directory)"
    )

    # --------------------- Parse Arguments --------------------- #
    args = parser.parse_args()

    openstudio_model_path = Path(args.openstudio_model_path)
    weather_file_name = args.weather_file_name

    script_dir_path = Path(__file__).resolve().parent
    weather_file_path = script_dir_path / "weather" / weather_file_name
    base_dir = Path(args.base_dir)

    # Validate essential file/directory paths
    if not openstudio_model_path.exists():
        raise FileNotFoundError(
            f"The OpenStudio model file '{openstudio_model_path}' does not exist."
        )
    if not weather_file_path.exists():
        raise FileNotFoundError(
            f"The weather file '{weather_file_name}' does not exist in the 'weather' directory. "
            "Please ensure that it is placed there."
        )
    if not base_dir.exists():
        raise FileNotFoundError(
            f"The base directory '{base_dir}' does not exist. Please specify a valid directory."
        )

    # Create the analysis directory based on the model's stem
    analysis_path = base_dir / openstudio_model_path.stem
    analysis_path.mkdir(parents=True, exist_ok=True)

    empty_cp_json_default = empty_comp_param_json_path(openstudio_model_path)

    # --------------------- create_cp_csv Command --------------------- #
    if args.command == "create_cp_csv":
        convert_input_format_exe = Path(args.convert_input_format_exe_path)
        if not convert_input_format_exe.exists():
            raise FileNotFoundError(
                f"Could not find ConvertInputFormat.exe at '{convert_input_format_exe}'."
            )

        # Prepare paths
        simulate_model_with_outputs = analysis_path / f"{openstudio_model_path.stem}_simulate_model.osw"
        target_osm_path = analysis_path / openstudio_model_path.name

        # Copy the model into the analysis directory
        shutil.copy(str(openstudio_model_path), target_osm_path)

        # 1) Simulate model with analysis outputs
        if is_osw_success(
                json.dumps(
                    return_openstudio_workflow_simulate_model_and_add_analysis_outputs(
                        str(target_osm_path), weather_file_name
                    ),
                    indent=4,
                ),
                simulate_model_with_outputs.as_posix(),
        ):
            # 2) Convert IDF to epJSON
            idf_file_path = idf_path(target_osm_path)
            if not idf_file_path.exists():
                raise FileNotFoundError(
                    f"Could not find the IDF file at '{idf_file_path}'. "
                    "Did the simulation run correctly?"
                )

            if succcessfully_ran_convert_input_format(
                    convert_input_format_exe.as_posix(), idf_file_path
            ):
                # 3) Create an empty compliance parameter JSON
                if create_empty_cp_json_file_success(
                        analysis_run_path(analysis_path).as_posix()
                ):
                    # 4) Create the CSV from the compliance parameter JSON
                    create_cp_csv_osw_path = analysis_path / f"{openstudio_model_path.stem}_create_cp_csv.osw"
                    if is_osw_success(
                            json.dumps(
                                return_open_studio_workflow_create_cp_csv(
                                    target_osm_path.as_posix(),
                                    weather_file_name,
                                    empty_comp_param_json_path(target_osm_path).as_posix(),
                                    construct_csv_file_path(target_osm_path).as_posix(),
                                ),
                                indent=4,
                            ),
                            create_cp_csv_osw_path.as_posix(),
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

    # --------------------- create_rpd Command --------------------- #
    elif args.command == "create_rpd":
        osw_path = analysis_path / f"{openstudio_model_path.stem}_create_rpd.osw"
        target_osm_path = analysis_path / openstudio_model_path.name

        # Copy the model into the analysis directory
        shutil.copy(str(openstudio_model_path), target_osm_path)

        # Validate the CSV file
        csv_file_path = Path(args.csv_file_path)
        if not csv_file_path.exists():
            raise FileNotFoundError(
                f"Could not find the CSV file at '{csv_file_path}'."
            )

        # Determine the compliance parameter JSON path to update
        if args.comp_param_json_file_path is None:
            comp_param_json_file_path = Path(
                analysis_run_path(analysis_path)
            ) / "in.comp-param.json"
        else:
            comp_param_json_file_path = Path(args.comp_param_json_file_path)

        # 1) Read CP CSV and update JSON
        if is_osw_success(
                json.dumps(
                    return_open_studio_workflow_read_cp_csv(
                        target_osm_path.as_posix(),
                        weather_file_name,
                        empty_cp_json_default.as_posix(),
                        comp_param_json_file_path.as_posix(),
                        csv_file_path.as_posix(),
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

            # 2) Validate the updated JSON
            if not comp_param_json_file_path.exists():
                raise FileNotFoundError(
                    f"Could not find the file '{comp_param_json_file_path}'"
                )

            result = schema_validate(
                json.load(open(comp_param_json_file_path.as_posix(), "r"))
            )

            if result["passed"]:
                print(
                    f"""\033[92mThe compliance parameter json file {comp_param_json_file_path.name} 
                for the model {openstudio_model_path.name} has passed validation with details {result}.\033[0m"""
                )

                # 3) Attempt to generate rpd.json
                if create_add_cp_json_file_success(
                    analysis_run_path(analysis_path).as_posix()
                ):
                    print(
                        f"""\033[92m Successfully generated rpd.json at {analysis_run_path(analysis_path).as_posix()}
                             \033[0m"""
                    )
                else:
                    print(
                        f"""\033[91m Failed to generate rpd.json! 
                            at {analysis_run_path(analysis_path).as_posix()}\033[0m"""
                    )
            else:
                print(
                    f"""\033[91mThe compliance parameter json file {comp_param_json_file_path.name} 
                for the model {openstudio_model_path.name} 
                at path {analysis_run_path(analysis_path).as_posix()} 
                has failed validation with {len(result['errors'])} errors, please see below \n\n.\033[0m"""
                )

                for index, error in enumerate(result["errors"]):
                    print(f"\033[91m-{index+1}. {error}\033[0m" "\n")

        else:
            print(
                f"""\033[91mFailed to read the CSV file with compliance parameters
             values for the model {openstudio_model_path.name}, .\033[0m"""
            )


if __name__ == "__main__":
    main()
