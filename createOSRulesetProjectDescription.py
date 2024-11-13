import subprocess
import argparse

def run_openstudio_command(command_args):
    try:
        run_osw = ['openstudio', 'run','-w']
        # Run the command
        subprocess.run(run_osw.extend(command_args), check=True)
        print(f"Successfully ran command: {run_osw.join(command_args)}")
    except subprocess.CalledProcessError as e:
        print(f"Error running the command: {e}")

def main():
    parser = argparse.ArgumentParser(description="Run OpenStudio workflow commands.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--create_cp_csv', metavar='filename.osm', help="Run with --create_cp_csv")
    group.add_argument('--create_rmd', nargs=2, metavar=('filename.osm', 'filename_cp-complete.csv'), help="Run with --create_rmd")

    args = parser.parse_args()

    if args.create_cp_csv:

        ## User will call 
        ## createOSRulesetProjectDescription --create_cp_csv filename.osm 
        run_openstudio_command(["create_cp_csv.osw", "--create_cp_csv", args.create_cp_csv])

    elif args.create_rmd:
        ### TODO need to check that input csv file exists and all rows are populated
        ### csv file name must be named -- filename_cp-complete.csv”
        
        ### User will call - createOSRulesetProjectDescription --create_rmd filename.osm filename_cp-complete.csv 
        run_openstudio_command(["create_rmd.osw", "--create_rmd", *args.create_rmd])

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