import gwtm_api
import datetime
from astropy.coordinates import SkyCoord 
from astropy.table import Table
import astropy.units as u

def submit_treasuremap(graceid, api_token, status, ralist, declist, times, depths, bands, instrumentid):
	#Bulk submission of treasure map pointings for e.g. Swope in the format e.g. # name ra dec filter exptime start_time_utc m3sigma 
    #Assumes we are using the AB magnitude system and are not savages. 
    
    batch = []

    for i in range(len(ralist)):
        
        c = SkyCoord(ralist[i], declist[i], frame='fk5', unit=(u.hourangle, u.deg))
        
        p = gwtm_api.Pointing(
        ra=c.ra.deg,
        dec=c.dec.deg,
        instrumentid = instrumentid,
        time = times[i],
        status = status,
        depth = depths[i],
        depth_unit = 'ab_mag', 
        pos_angle=0, #Not sure if we plan to change position angles?
        band = bands[i]
        )
    
        batch.append(p)
        
       
    gwtm_api.Pointing.batch_post(pointings=batch, graceid=graceid, api_token=api_token)
    
    print(len(batch))
    print(len(ralist))


#pointingslist = '/Users/brendan/Documents/research/DECam/SWOPE_Schedule_20230504.dat'

#pointingslist = Table.read(pointingslist, format='ascii')
#ralist = pointingslist.columns[1].data
#declist = pointingslist.columns[2].data
#bands = pointingslist.columns[3].data
#times = pointingslist.columns[5].data
#depths = pointingslist.columns[6].data

#api_token = "your_token"
#graceid = 'MS230507r' #Test for a mock event. #http://treasuremap.space/alert_select?role=test&observing_run=O4
#status = 'planned'
#instrumentid = 68 #38 = DECam; 68 = Swope


#######################################################

if __name__ == '__main__':

	#############################
	## Parsing input arguments ##
	#############################

	import argparse

	parser = argparse.ArgumentParser(description="Wrapper to submit pointings to treasuremap.")
	parser.add_argument("file", help="Pointings file with columns # name ra dec filter exptime start_time_utc m3sigma ",type=str)
	parser.add_argument("graceid", help="graceid of event to submit pointings for",type=str)
	parser.add_argument("status", help="planned vs completed",type=str)
	parser.add_argument("instrumentid", help="Treasuremap instrument ID, e.g., Swope = 68",type=int)
	parser.add_argument("api_token", help="Your treasuremap api_token ",type=str)
	args = parser.parse_args()

	pointingslist = Table.read(args.file, format='ascii')
	ralist = pointingslist.columns[1].data
	declist = pointingslist.columns[2].data
	bands = pointingslist.columns[3].data
	times = pointingslist.columns[5].data
	depths = pointingslist.columns[6].data

	# Submit to treasuremap
	submit_treasuremap(args.graceid, args.api_token, args.status, ralist, declist, times, depths, bands, args.instrumentid)

    #How to run from command line
    # python3.10 submit_treasuremap.py /Users/brendan/Documents/research/DECam/example_SWOPE_Schedule_20230504.dat MS230507o completed 68 your_api_token_goes_here






#