import sys
import os

if len(sys.argv) == 2:
	filename = sys.argv[1]
	if not os.path.isfile(filename): #check to see if file exists
		print '[-] ' + filename + " does not exist"
		exit(0)
	if not os.access(filename, os.R_OK): #check to see if you have read access
		print "[-] " + filename + " access denied"	
		exit(0)
	print "Reading vulnerabilities from " + filename
