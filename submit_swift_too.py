from swifttools.swift_too import Swift_TOO
import astropy.units as u
from astropy.table import Table

#Documentation Links
#https://docs.google.com/document/d/198HZHG70qLPNYletOZiW9s0wKscQU4wFw8dMynvk0Lc/edit?usp=sharing

# Username and secret key
#username = "oconnorb10"
#shared_secret = "ydSnTWIvJX1kg4Hqxjhmm"

#How to run from command line
# python3 submit_swift_too.py example_Swift_ToO.dat oconnorb10 ydSnTWIvJX1kg4Hqxjhmm GW190425 1000 1 3 2 0x30d5


def submit_swift_too(username, shared_secret, GW_event, exp_time, visitfreq, visitnumber, urgency, uvot_filter, src_name, ra, dec, mag, Filter, debug):


	# Initiate the Swift_TOO class
	too = Swift_TOO()

	#For the list of possible entries see here https://www.swift.psu.edu/too_api/index.php?md=TOO%20parameters.md

	#This is not an approved GI program. 
	too.proposal = False

	if debug == True:
		#Enabling debug mode, so it will NOT send an actual request. This is a test. Remove this line if you intend to submit.
		too.debug = True
		print("Enabling debug mode, so it will NOT send an actual request. This is a test. Re-run with debug = False in order to send a real ToO.")

	# Username and secret key
	too.username = username
	too.shared_secret = shared_secret

	# The relevant details of the object to observe
	too.source_name = src_name # Typical name of source, if it resolves in Simbad, all the better
	too.ra = ra         # Right ascension in decimal degrees
	too.dec = dec     # Declination in decimal degrees
	too.source_type = "EM-GW Counterpart"  # Short description of source class
	too.poserr = 0.008 #Source localization error in arcminutes. 0.008 arcmin = 0.5". A typical optical localization.

	too.opt_mag = mag
	too.opt_filt = Filter

	# This is saying the primary instrument behind our ToO is UVOT. 
	#If instead you prefer to say XRT is the dominant instrument put "XRT"
	too.instrument = "UVOT"

	#Select the UVOT filter you would like.
	too.uvot_mode = 0x01AB 
	#0x01AB = uvm2
	#0x015a = u
	#see https://www.swift.psu.edu/operations/mode_lookup.php for others.

	too.uvot_just = ("We request UV coverage of this kilonova candidate. Swift is the only instrument capable of providing this rapid UV coverage.")

	# Estimate of how bright it is
	too.xrt_countrate = 0.005         # XRT counts/s
	too.xrt_mode = "PC"
	too.obs_type = too.obs_types[1] # This is "Light Curve" - the options are:["Spectroscopy","Light Curve","Position","Timing"]

	# Immediate Objective of these observations
	too.immediate_objective = ("UVOT/XRT coverage of a candidate kilonova discovered through EM tiling observations of a LVK O4 GW event.")


	# Science Justification - one to three paragraphs to explain why this TOO request should be accepted
	too.science_just = ("In monitoring the GW localization of "+str(GW_event)+" we discovered this rapidly fading optical transient. "
                    "The source is blue in color, and the rapid decay resembles that of AT2017gfo. "
                    "No source is known at this location and it is not a minor planet. "
                    "We request Swift XRT and UVOT coverage of this source to aid in classification. UV coverage is critical to understanding, and later modeling, this source as a kilonova. ")

	# Exposure description
	too.exp_time_per_visit = exp_time  # Must be in seconds
	too.monitoring_freq =  visitfreq * u.day # visitfreq = 1 would be one visit every day
	too.num_of_visits = visitnumber         # visitnumber = would monitor the source for 3 days.

	# Exposure time justification - Explain why 3ks is needed per observation.
	too.exp_time_just = ("The requested "+str(too.exp_time_per_visit)+" s observation will allow us to achieve our science goals and provide the required UVOT sensitivity. " 
                     "The monitoring of this source every "+str(too.monitoring_freq)+" for "+str(too.num_of_visits)+" is required to aid in classification "
                     " and provide pivotol UV coverage not possible rapidly by any other telescopes. "
                    "Kilonova fade rapidly and the "+str(too.monitoring_freq)+" cadence is required.")

	# Urgency
	too.urgency = urgency  # urgency = 2; Observations needed within 24 hours 
	#Changing this to 1 would request observations within 4 hours. 
	#This is a special case and should be reserved for if spectroscopic confirmation is already available. I would think...

	print(too)

	if too.validate():
    		print("TOO is good to go!")
	else:
    		print("Uh-oh!")

	if too.submit():
   			print("TOO submitted succesfully")
   			#print(f"Submitted TOO ID = {too.status.too_id}")
	else:
    		print("Sorry there was a problem with the submission")

	#print(too.complete)

	#


#######################################################

if __name__ == '__main__':



	print("\n\nTakes a file with the ordering: #srcname ra dec mag filter")

	#############################
	## Parsing input arguments ##
	#############################

	import argparse

	parser = argparse.ArgumentParser(description="Wrapper to submit pointings to treasuremap.")
	parser.add_argument("file", help="Pointings file with columns",type=str)
	parser.add_argument("username", help="your Swift ToO username",type=str)
	parser.add_argument("shared_secret", help="your Swift ToO shared secret",type=str)
	parser.add_argument("GW_event", help="Name of GW Event e.g. GW170818",type=str)
	parser.add_argument("exp_time", help="Requested exposure time per visit in seconds",type=float)
	parser.add_argument("visit_frequency", help="Requested frequency of visits in days",type=float)
	parser.add_argument("visit_number", help="Requested number of visits",type=float)
	parser.add_argument("urgency", help="ToO Urgency: 1=within 4 hours; 2= within 24 hrs, etc...",type=float)
	parser.add_argument("uvot_filter", help="Requested UVOT Filter String e.g. 0x30d5",type=str)
	args = parser.parse_args()

	pointingslist = Table.read(args.file, format='ascii')
	ralist = pointingslist.columns[1].data
	declist = pointingslist.columns[2].data
	srcnamelist = pointingslist.columns[0]
	maglist = pointingslist.columns[3]
	filterlist = pointingslist.columns[4]

	#username = "oconnorb10"
	#shared_secret = "ydSnTWIvJX1kg4Hqxjhmm"

	#The information on your target
	#GW_Event = 'GW170817' #Name of the GW event you are observing
	#src_name = "SSS17a" #Name of the source you discovered
	#RA = 13.023439 #RA
	#DEC = -72.434508 #DEC
	#Mag = 17 #Discovery magnitude
	#Filter = 'r' #Optical Filter of Discovery

	print("\nCurrent setting is debug mode, which means that no actual ToO will be submitted. Change debug = False in order to submit a real ToO.\n\n")
	debug = True

	for i in range(len(ralist)):
		print("ToO #"+str(i)+": "+str(srcnamelist[i]))
		#submit_swift_too(username, shared_secret, GW_event, exp_time, visitfreq, visitnumber, urgency, uvot_filter, src_name, ra, dec, mag, Filter, debug)	
		submit_swift_too(args.username, args.shared_secret, args.GW_event, args.exp_time, args.visit_frequency, args.visit_number, args.urgency, args.uvot_filter, srcnamelist[i], ralist[i], declist[i], maglist[i], filterlist[i], debug)

		#

	print("\n\nAll ToOs Submitted.\n\n")



