#this script will read a skype sqlite3 database and print the contents

import sqlite3

#Connect to the Calls and Conversations tables to create a call log
def printCallLog(skypeDB):
	#connect to the sqlite3 db
	conn = sqlite3.connect(skypeDB)
	c = conn.cursor()
	
	#create a SQL query that pulls from both the Calls and Conversations tables joined by a conversation.id
	c.execute("SELECT datetime(begin_timestamp, 'unixepoch,), identity FROM calls, conversations WHERE calls.conv_dbid = conversations.id;")
	
	#print the results for the call log
	print '[*] -- Calls Found --'
	for row in c:
		print '[+] Time: ' + str(row[0]) + ' | Partner: ' + str(row[1])
		

#connect to the contacts table and print out contact information
def printContacts(skypeDB):
	#connect to the sqlite3 db
	conn = sqlite3.connect(skypeDB)
	c = conn.cursor()
	
	#pass the SQL query to the database to pull contact information
	c.execute("SELECT displayname, skypename, city, country, phone_mobile, birthday FROM Contacts;")
	
	#print out the results of the query. Use if statements to ignore blank fields
	for row in c:
		print "[*] -- Found Contact --"
		print '[+] User: ' + str(row[0])
		print '[+] Skype Username: ' + str(row[1])
		if str(row[2]) != '' and str(row[2]) != 'None':
			print '[+] Location: ' + str(row[2]) + ', ' + str(row[3])
		if str(row[4]) != 'None':
			print '[+] Mobile Number: ' + str(row[4])
		if str(row[5]) != 'None':
			print '[+] Birthday: ' + str(row[5])

#connect to the user accounts table, print out account information
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