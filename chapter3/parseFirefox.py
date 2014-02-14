#Application will parse through local FireFox databases to pull data from
import sqlite3
import re
import os
import optparse

#parse through the Downloads database and print results
def printDownloads(downloadDB):
	#connect to the database
	conn = sqlite3.connect(downloadDB)
	c = conn.cursor()
	#sql query to pull data from the downloads database. Time is stored in unix*1,000,000, which is why it is divided
	c.execute("SELECT name, source, datetime(endTime/1000000, 'unixepoch') FROM moz_downloads;")
	
	print "\n[*] -- Files Downloaded --"
	#iterate through all of the pulled data
	for row in c:
		print '[+] File: ' + str(row[0]) + ' from source: ' + str(row[1]) + ' at: ' + str(row[2])

#parse through the cookies database and print results
def printCookies(cookiesDB):
	#the cookies database is encrypted, exception to handle any errors
	try:
		#connect to the database
		conn = sqlite3.connect(cookiesDB)
		c = conn.cursor()
		#query to pull back data from the cookies database
		c.execute("SELECT host,name,value FROM moz_cookies;")
		#iterate through all of the pulled data
		for row in c:
			print "\n[*] -- Cookies Found --"
			print "[+] Host: " + str(row[0]) + ", Cookie: " + str(row[1]) + ", Value: " + str(row[2])
	except Exception, e:
		if 'encrypted' in str(e):
			print "\n[*] Error reading your cookies database."
			print "[*] Upgrade your Python-sqlite3 library"

#parse through the Places and History Vists database to pull back web history
def printHistory(placesDB):
	#the cookies database is encrypted, exception to handle any errors
	try:
		#connect to the database
		conn = sqlite3.connect(placesDB)
		c = conn.cursor()
		#query to pull back data from the history databases
		c.execute("SELECT url, datetime(visitdate/1000000, 'unixepoch') FROM moz_places, moz_historyvisits WHERE vist_count > 0 and moz_places.id == moz_historyvisits.place_id;")
		print "\n[*] -- Found History --"
		#iterate through the results
		for row in c:
			print "[+] " + str(row[1]) + " - Visited: " + str(row[0])
	except Exception, e:
		if 'encrypted' in str(e):
			print "\n[*] Error reading your places database."
			print "[*] Upgrade your Python-sqlite3 library"
			
#parse through the places database for Google searches. Extract the search terms from the url, replacing the HTML codes with whitespace
def printGoogle(placesDB):
	try:
		#connect to the database
		conn = sqlite3.connect(placesDB)
		c = conn.cursor()
		#query to pull back data from the history databases
		c.execute("SELECT url, datetime(visitdate/1000000, 'unixepoch') FROM moz_places, moz_historyvisits WHERE vist_count > 0 and moz_places.id == moz_historyvisits.place_id;")
	
		print "\n[*] -- Found Google --"
		for row in c:
			url = str(row[0])
			date = str(row[1])
		
			#check the url to see if it is from Google
			if 'google' in url.lower():
				#look in the url for 'q=&' to determine if it is a google search or not
				r = re.findall(r'q=.*\&', url)
				if r:
					search = r[0].split('&')[0]
					#remove the 'q=' and replace '+' with spaces
					search = search.replace('q=', '').replace('+', ' ')
					print '[+] ' + date + ' - Searched for: ' + search
	except Exception, e:
		if 'encrypted' in str(e):
			print "\n[*] Error reading your places database."
			print "[*] Upgrade your Python-sqlite3 library"

def main():
	parser = optparse.OptionParser("usage%prog -p <firefox profile path>")
	parser.add_option('-p', dest='pathName', type='string', help='specify firefox profile path')
	(options,args) = parser.parse_args()
	pathName = options.pathName
	
	if pathName == 'None':
		print parser.usage
		exit(0)
	#check to see that the path directory exists
	elif os.path.isdir(pathName) == False:
		print ' [!] Path does not exist: ' + pathName
		exit(0)
	else:
		downloadDB = os.path.join(pathName, 'downloads.sqlite')
		#check to see if the database exists
		if os.path.isfile(downloadDB):
			printDownloads(downloadDB)
		else:
			print '[!] Downloads DB does not exist: ' + downloadDB
		
		cookiesDB = os.path.join(pathName, 'cookies.sqlite')
		#check to see if the database exists
		if os.path.isfile(cookiesDB):
			printCookies(cookiesDB)
		else:
			print '[!] Cookies DB does not exist: ' + cookiesDB
		
		placesDB = os.path.join(pathName, 'places.sqlite')
		#check to see if the database exists
		if os.path.isfile(placesDB):
			printHistory(placesDB)
			printGoogle(placesDB)
		else:
			print '[!] Places DB does not exist: ' + placesDB
if __name__ == '__main__':
	main()
	