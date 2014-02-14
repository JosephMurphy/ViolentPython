#Application will search through a iPhone backup to find phone message information
import os
import sqlite3
import optparse

"""
#Open the database and print all of the table names by pulling from the sqlite_master table
def printTables(iphoneDB):
	try:
		#connect to the database
		conn = sqlite3.connect(iphoneDB)
		c = conn.cursor()
		#SQL query to list all of the table names
		c.execute("SELECT tbl_name FROM sqlite_master WHERE type == \"table\";")
		
		print "\n[*] Database: " + iphoneDB
		#iterate through the results and print
		for row in c:
			print "[-] Table: " + str(row[0])
	except:
		pass
	
	#close the connect
	conn.close()
	
	
def main():
	dirList = os.listdir(os.getcwd())
	for filename in dirList:
		printTables(filename)
"""

#search through the tables in the database files, return true if the file contains the table "messages"
def isMessageTable(iphoneDB):
	try:
		#connect to the database
		conn = sqlite3.connect(iphoneDB)
		c = conn.cursor()
		#SQL query to select all the table names from the database
		c.execute("SELECT tbl_name FROM sqlite_master WHERE type == \"table\";")
		#iterate through all the results
		for row in c:
			#check to see if the "message" table is in the database
			if 'message' in str(row):
				return True
	except:
		return False

#Query the message table to pull back and print message information
def printMessage(msgDB):
	try:
		#connect to the database
		conn = sqlite3.connect(msgDB)
		c = conn.cursor()
		#SQL query to pull back the message information
		c.execute("SELECT datetime(date, 'unixepoch'), address, text FROM message WHERE address > 0;")
		#iterage through the results
		for row in c:
			date = str(row[0])
			addr = str(row[1])
			text = row[2]
			print "\n[+] Date: " + date + ", Address: " + addr + ", Message: " + text
	except:
		pass
		
def main():
	parser = optparse.OptionsParser("usage%prog -p <iPhone Backup Directory>")
	parser.add_option('-p', dest='pathName', type='string', help='specify the iphone backup directory path')
	(options, args) = parser.parse_args()
	pathName = options.pathName
	
	if pathName == 'None':
		print parser.usage
		exit(0)
	else:
		#Get a list of the files in the provided directory
		dirList = os.listdir(pathName)
		#iterate through each file, looking for the one with the "message" table
		for filename in dirList:
			iphoneDB = os.path.join(pathName, filename)
			#use the isMessageTable function to search for the message table in the database file. Only call the function if isMessageTable returns true
			if isMessageTable(iphoneDB):
				try:
					print '\n[*] -- Found Messages -- '
					printMessage(iphoneDB)
				except:
					pass

if __name__ == '__main__':
	main()