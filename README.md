# O4-Tools
Useful python tools for LVK O4 

Python wrappers for Treasuremap, Swift ToOs, and converting gwemopt output to DECam JSON files.

# Treasure Map wrapper:

This code takes an input file (e.g. example_SWOPE_Schedule_20230504.dat) with columns # name ra dec filter exptime start_time_utc m3sigma where state_time_utc is in the format 2023-05-04T23:24:18 and ra/dec are in the format 05:23:56.980 -13:06:15.690. The ra/dec are converted to degrees.

To run the code in terminal use:

python3.10 submit_treasuremap.py file graceid status instrumend_id api_token

python3.10 submit_treasuremap.py example_SWOPE_Schedule_20230504.dat MS230507o completed 68 your_api_token_goes_here

**OR**

The gwemopt output file (e.g. schedule_DECam.dat) already has ra/dec in degrees, but the time is in MJD and gets converted to UTC time. 

To run the code in terminal use:

python3.10 submit_treasuremap_gwemopt.py schedule_DECam.dat MS230507o completed 38 your_api_token_goes_here

# Swift ToO wrapper:

The file Swift_ToO_API_Submission_Notebook.ipynb allows for submitting a ToO in a Jupyter Notebook format - **this is the preferred method and is easiest to verify** - automic submission as below could be tricky.

To submit multiple Swift ToOs from a text file with columns of: #srcname ra dec mag filter

To run the code in terminal use:

python3 submit_swift_too.py example_Swift_ToO.dat "your_username "your_shared_secret" GW_event exp_time visit_frequency visit_number urgency uvot_filter_string

# gwemopt DECam Wrapper:

gwemopt_to_json_DECam.py converts the gwemopt output file into the format of a DECam pointings json file. 

To run the code in terminal use:

python gwemopt_to_json_DECam.py schedule_DECam.dat DECam_program_ID GW_event

