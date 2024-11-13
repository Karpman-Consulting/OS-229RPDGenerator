
User Steps:

1. Run command  createOSRulesetProjectDescription --create_cp_csv filename.osm

where  filename.osm is osm to process, this command will generate a csv 
filename_cp-empty.csv

2. Open filename_cp-empty.csv, be sure to provide data for ALL ROWS in the csv
then save it as filename_cp-complete.csv”


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

