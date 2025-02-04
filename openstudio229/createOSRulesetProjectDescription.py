import os
import shutil
import subprocess
import argparse
import json
import logging
from pathlib import Path, WindowsPath
from rpdvalidator.validate import schema_validate

from transfer_csv_to_json import transfer_csv_to_rpd

# ANSI color codes
RED = "\033[31m"
GREEN = "\033[32m"
GRAY = "\033[37m"
RESET = "\033[0m"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format=f'{GRAY}%(asctime)s [%(levelname)s] %(message)s{RESET}',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


def return_openstudio_workflow_simulate_model_and_add_analysis_outputs(
    seed_model_path: Path,
    weather_file_path: Path
) -> dict:
    root_path = Path(__file__).parent.parent.resolve()
    run_directory = seed_model_path.parent / "run"
    return {
        "seed_file": seed_model_path.as_posix(),
        "weather_file": weather_file_path.as_posix(),
        "root": root_path.as_posix(),
        "measure_paths": ["."],
        "run_directory": run_directory.as_posix(),
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

# REPLACED BY transfer_csv_to_json
# --------------------------------
# def return_open_studio_workflow_read_cp_csv(
#     seed_model_path: Path,
#     weather_file_path: Path,
#     empty_comp_param_json_file_path: Path,
#     updated_comp_param_json_file_path: Path,
#     csv_file_path: Path
# ) -> dict:
#     root_path = Path(__file__).parent.parent.resolve()
#     run_directory = seed_model_path.parent / seed_model_path.stem / "run"
#     return {
#         "seed_file": seed_model_path.as_posix(),
#         "weather_file": weather_file_path.as_posix(),
#         "root": current_file_path.as_posix(),
#         "measure_paths": ["."],
#         "run_directory": run_directory.as_posix(),
#         "steps": [
#             {
#                 "measure_dir_name": "read_cp_csv",
#                 "name": "ReadComplianceParameterCsvFromOsm",
#                 "arguments": {
#                     "empty_comp_param_json_file_path": empty_comp_param_json_file_path.as_posix(),
#                     "updated_comp_param_json_file_path": updated_comp_param_json_file_path.as_posix(),
#                     "csv_file_path": csv_file_path.as_posix(),
#                 },
#             }
#         ],
#     }


def return_open_studio_workflow_create_cp_csv(
    seed_model_path: Path,
    weather_file_name: Path,
    empty_comp_param_json_file_path: Path,
    output_csv_file_path: Path
) -> dict:
    root_path = Path(__file__).parent.parent.resolve()
    run_directory = seed_model_path.parent / "run"
    return {
        "seed_file": seed_model_path.as_posix(),
        "weather_file": weather_file_name.as_posix(),
        "root": root_path.as_posix(),
        "measure_paths": ["."],
        "run_directory": run_directory.as_posix(),
        "steps": [
            {
                "measure_dir_name": "create_cp_csv",
                "name": "CreateComplianceParameterCsvFromOsm",
                "arguments": {
                    "empty_comp_param_json_file_path": empty_comp_param_json_file_path.as_posix(),
                    "output_csv_file_path": output_csv_file_path.as_posix(),
                },
            }
        ],
    }


def run_convert_input_format(
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
            [convert_input_format_exe_path, idf_file_path],
            env=os.environ,
        )
        return True

    except FileNotFoundError:
        logging.error(f"{RED}Executable not found: %s{RESET}", convert_input_format_exe_path)
    except PermissionError:
        logging.error(f"{RED}Permission denied: %s{RESET}", convert_input_format_exe_path)
    except subprocess.CalledProcessError as e:
        logging.error(
            f"{RED}Failed to execute '%s' on '%s'. Exit code: %d. Error: %s{RESET}",
            convert_input_format_exe_path,
            idf_file_path,
            e.returncode,
            e.output if e.output else "No output available"
        )
    except OSError as e:
        logging.error(
            f"{RED}OS error while executing '%s' on '%s': %s{RESET}",
            convert_input_format_exe_path,
            idf_file_path,
            str(e)
        )
    except Exception as e:
        logging.error(
            f"{RED}Unexpected error while running '%s' on '%s': %s{RESET}",
            convert_input_format_exe_path,
            idf_file_path,
            str(e)
        )
    return False


def run_create_empty_cp_json_file(analysis_run_path_str: str) -> bool:
    """
    Attempts to create an empty cp JSON file by running the 'energyplus_create_rpd' command.
    Returns True if successful, False otherwise.
    """
    try:
        subprocess.check_call(
            [
                "energyplus_create_rpd",
                "--create_empty_cp",
                "in.epJSON",
            ],
            cwd=analysis_run_path_str,
            env=os.environ,
        )
        return True
    except FileNotFoundError:
        logging.error(
            f"{RED}Command 'energyplus_create_rpd' not found. Ensure it is installed and in the system PATH.{RESET}"
        )
    except PermissionError:
        logging.error(
            f"{RED}Insufficient permissions to execute 'energyplus_create_rpd' in %s.{RESET}",
            analysis_run_path_str
        )
    except subprocess.TimeoutExpired:
        logging.error(
            f"{RED}Command 'energyplus_create_rpd' timed out in %s.{RESET}",
            analysis_run_path_str
        )
    except ValueError as e:
        logging.error(f"{RED}Invalid parameter provided: %s{RESET}", str(e))
    except OSError as e:
        logging.error(f"{RED}OS error occurred while running subprocess: %s{RESET}", str(e))
    except subprocess.CalledProcessError as e:
        logging.error(
            f"{RED}Failed to run 'energyplus_create_rpd --create_empty_cp' in %s. Error: %s{RESET}",
            analysis_run_path_str, str(e)
        )
    return False


def run_openstudio_workflow(
    osw_config: str,
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
        osw_config (str): The OSW JSON string to be written to a file.
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
        file.write(osw_config)

    try:
        run_osw = ["openstudio", "run", "-w"]

        if measures_only and reporting_measures_only:
            raise ValueError(
                "Only one of measures_only and reporting_measures_only can be True."
            )

        if measures_only:
            run_osw = [
                "openstudio",
                "run",
                "--measures_only",
                "-w",
            ]
        if reporting_measures_only:
            run_osw = [
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
        subprocess.check_call(full_command, env=os.environ)

        return True

    except subprocess.CalledProcessError:
        return False


def validate_paths(paths: [list, Path, str]):
    if isinstance(paths, list):
        for path in paths:
            validate_paths(path)
    elif isinstance(paths, Path):
        if not paths.exists():
            raise FileNotFoundError(f"The path '{paths}' does not exist.")
    elif isinstance(paths, str):
        if not Path(paths).exists():
            raise FileNotFoundError(f"The path '{paths}' does not exist.")
    else:
        raise ValueError(f"Invalid type '{type(paths)}' for 'paths'.")


def setup_analysis_directory(openstudio_model_path):
    analysis_path = openstudio_model_path.parent / openstudio_model_path.stem
    analysis_path.mkdir(parents=True, exist_ok=True)
    return analysis_path


def handle_simulation_workflow(analysis_path, openstudio_model_path, weather_file_path):
    validate_paths([openstudio_model_path, weather_file_path])

    target_osm_path = analysis_path / openstudio_model_path.name
    shutil.copy(str(openstudio_model_path), target_osm_path)

    # Simulate model
    osw_return_code = run_openstudio_workflow(
        json.dumps(
            return_openstudio_workflow_simulate_model_and_add_analysis_outputs(
                target_osm_path, weather_file_path
            ),
            indent=4,
        ),
        (analysis_path / f"{target_osm_path.stem}_simulate_model.osw").as_posix(),
    )
    if not osw_return_code:
        logger.error(f"{RED}Failed to simulate OpenStudio model. CSV creation aborted.{RESET}")
        return


def handle_convert_input_format(convert_input_format_exe_path, analysis_path):
    idf_file_path = analysis_path / "run" / "in.idf"
    validate_paths([convert_input_format_exe_path, idf_file_path])

    # Convert IDF to epJSON
    if not run_convert_input_format(convert_input_format_exe_path.as_posix(), idf_file_path.as_posix()):
        logger.error(f"{RED}Failed to convert IDF to epJSON.{RESET}")
        return


def handle_create_empty_comp_param_json(analysis_path):
    # Create empty compliance parameter JSON
    if not run_create_empty_cp_json_file((analysis_path / "run").as_posix()):
        logger.error(f"{RED}Failed to create empty CP JSON file.{RESET}")
        return


def handle_convert_json_to_csv(analysis_path, openstudio_model_path, weather_file_path):
    target_osm_path = analysis_path / openstudio_model_path.name
    comp_param_json_file_path = analysis_path / "run" / "in.comp-param-empty.json"
    empty_csv_file_path = analysis_path / "run" / f"{target_osm_path.stem}-empty.csv"

    # Create the CSV from JSON
    if not run_openstudio_workflow(
        json.dumps(
            return_open_studio_workflow_create_cp_csv(
                target_osm_path,
                weather_file_path,
                comp_param_json_file_path,
                empty_csv_file_path,
            ),
            indent=4,
        ),
        (analysis_path / f"{target_osm_path.stem}_create_cp_csv.osw").as_posix(),
        measures_only=False,
        reporting_measures_only=True,
    ):
        logger.error(f"{RED}Failed to create CSV file with compliance parameters.{RESET}")
        return

    logger.info(f"{GREEN}Successfully created compliance parameters CSV.{RESET}")


def handle_csv_data_transfer(analysis_path, csv_file_path):
    rpd_file_path = analysis_path / "run" / "in.rpd"
    validate_paths([csv_file_path, rpd_file_path])

    # Read CSV and update JSON
    if not transfer_csv_to_rpd(rpd_file_path, csv_file_path):
        logger.error(f"{RED}Failed to process CSV file.{RESET}")
        return

    logger.info(f"{GREEN}Successfully transferred CSV data to RPD.{RESET}")


def handle_rpd_validation(analysis_path):
    rpd_file_path = analysis_path / "run" / "in.rpd"
    logger.info(f"{GRAY}Validating '{rpd_file_path}'{RESET}")

    # Validate updated JSON
    with open(rpd_file_path.as_posix(), "r") as f:
        validation_result = schema_validate(json.load(f))
        if not validation_result["passed"]:
            logger.error(f"{RED}Validation FAILED with errors:{RESET}")
            for index, error in enumerate(validation_result["errors"]):
                logger.error(f"{RED}{index + 1}.) {error}{RESET}")
            return

    logger.info(f"{GREEN}Validation PASSED. Successfully generated '{rpd_file_path}'.{RESET}")


def handle_create_comp_param_csv(convert_input_format_exe_path, openstudio_model_path, weather_file_path, analysis_path):
    handle_simulation_workflow(analysis_path, openstudio_model_path, weather_file_path)
    handle_convert_input_format(convert_input_format_exe_path, analysis_path)
    handle_create_empty_comp_param_json(analysis_path)
    handle_convert_json_to_csv(analysis_path, openstudio_model_path, weather_file_path)


def handle_create_rpd(analysis_path, csv_file_path):
    handle_csv_data_transfer(analysis_path, csv_file_path)
    handle_rpd_validation(analysis_path)


def cli():
    parser = argparse.ArgumentParser(
        description="CLI tool for generating 229 Ruleset Project Description files from OpenStudio models",
    )
    subparsers = parser.add_subparsers(dest="command", required=True, help="Available subcommands")

    # create_cp_csv Subcommand
    cp_csv_parser = subparsers.add_parser("create_csv", help="Create a compliance parameters CSV file", description="Generates a CSV file with compliance parameters extracted from an OpenStudio model.")
    cp_csv_parser.add_argument("--openstudio_model", type=Path, required=True, help="Path to OpenStudio model - absolute or relative to base_dir")
    cp_csv_parser.add_argument("--weather_file", type=Path, required=True, help='Path to weather file - absolute or relative to a "weather" folder in base_dir')
    cp_csv_parser.add_argument("--base_dir", type=Path, default=Path.cwd(), help="(optional) Base directory for relative paths - default is current working directory")
    cp_csv_parser.add_argument("--convert_input_format_exe", type=Path, default=Path(r"C:\EnergyPlusV24-2-0\ConvertInputFormat.exe"), help=r"Absolute path to ConvertInputFormat.exe - default is C:\EnergyPlusV24-2-0\ConvertInputFormat.exe")

    # create_rpd Subcommand
    rpd_parser = subparsers.add_parser("create_rpd", help="Merge CSV data into RPD and validate", description="Merges compliance parameters from a CSV file into a Ruleset Project Description (RPD) and validates the file against the schema.")
    rpd_parser.add_argument("--openstudio_model", type=Path, required=True, help="Path to OpenStudio model - absolute or relative to base_dir")
    rpd_parser.add_argument("--csv_file", type=Path, required=True, help="Path to CSV file - absolute or relative to base_dir")
    rpd_parser.add_argument("--base_dir", type=Path, default=Path.cwd(), help="(optional) Base directory for relative paths - default is current working directory")

    args = parser.parse_args()
    base_dir = args.base_dir.resolve()
    validate_paths(base_dir)

    # Resolve openstudio_model_path
    openstudio_model_path = args.openstudio_model
    if not openstudio_model_path.is_absolute():
        openstudio_model_path = base_dir / openstudio_model_path

    analysis_path = setup_analysis_directory(openstudio_model_path)

    if args.command == "create_csv":
        convert_input_format_exe_path = args.convert_input_format_exe

        # Resolve weather_file_path
        weather_file_path = args.weather_file
        if not weather_file_path.is_absolute():
            weather_file_path = base_dir / "weather" / args.weather_file

        # Run create_comp_param_csv
        handle_create_comp_param_csv(convert_input_format_exe_path, openstudio_model_path, weather_file_path, analysis_path)

    elif args.command == "create_rpd":
        # Resolve csv_file_path
        csv_file_path = args.csv_file
        if not csv_file_path.is_absolute():
            csv_file_path = base_dir / csv_file_path

        # Run create_rpd
        handle_create_rpd(analysis_path, csv_file_path)


if __name__ == "__main__":
    cli()
