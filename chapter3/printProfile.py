#this script will read a skype sqlite3 database and print the contents

import sqlite3

def printProfile(skypeDB):
	#connect to the sqlite3 db
	conn = sqlite3.connect(skypeDB)
	c = conn.cursor()

	#pass the SQL query to the database.  It will pull information from the accounts table
	c.execute("SELECT fullname,skypename,city,country, datetime(profile_timestamp, 'unixepoch') FROM Accounts;")
	
	#iterate through the info pulled from the query, printing each row
	for row in c:
		print '[*] -- Found Account -- '
		print '[+] User: ' + str(row[0])
		print '[+] Skype Username: ' + str(row[1])
		print '[+] Location: ' + str(row[2]) + ', ' + str(row[3])
		print '[+] Profile Date: ' + str(row[4])
		
def main():
	skypeDB = 'main.db'
	printPRofile(skypeDB)

if __name__ == '__main__':
	main()