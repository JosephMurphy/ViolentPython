#Application will parse through local FireFox databases to pull data from
import sqlite3

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

		
if __name__ == '__main__':
	main()
	