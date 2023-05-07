# O4-Tools
Useful python tools for LVK O4 

Python wrappers for Treasuremap, Swift ToOs, and converting gwemopt output to DECam JSON files.

# Treasuremap wrapper:

python3.10 submit_treasuremap.py file graceid status instrumend_id api_token

python3.10 submit_treasuremap.py example_SWOPE_Schedule_20230504.dat MS230507o completed 68 your_api_token_goes_here

**OR**

For gwemopt output file you can run: 

python3.10 submit_treasuremap_gwemopt.py schedule_DECam.dat MS230507o completed 38 your_api_token_goes_here
