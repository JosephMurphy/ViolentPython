#this script will read a skype sqlite3 database and print the contents
import sqlite3
import optparse
import os

#Connect to the Messages db to query and print the body of all messages
def printMessages(skypeDB):
	#connect to the sqlite3 db
	conn = sqlite3.connect(skypeDB)
	c = conn.cursor()
	
	#SQL query to pull the messages
	c.execute("SELECT datetime(timestamp, 'unixepoch'), dialog_partner, author, body_xml FROM Messages;")
	
	#print the results
	print '\n[*] -- Found Messages --'
	for row in c:
		try:
			if 'partlist' not in str(row[3]):
				#Check to see if the dialog_partner is different than the author. If this is the case, the DB owner initiated the conversation
				if str(row[1]) != str(row[2]):
					msgDirection = 'To ' + str(row[1]) + ': ' #message initiated by owner of DB
				else:
					msgDirection = 'To ' + str(row[2]) + ': ' #message initiated by the dialog partner
				print 'Time: ' + str(row[0]) + ' ' + msgDirection + str(row[3])
		except:
			pass

#Connect to the Calls and Conversations tables to create a call log
def printCallLog(skypeDB):
	#connect to the sqlite3 db
	conn = sqlite3.connect(skypeDB)
	c = conn.cursor()
	
	#create a SQL query that pulls from both the Calls and Conversations tables joined by a conversation.id
	c.execute("SELECT datetime(begin_timestamp, 'unixepoch,), identity FROM calls, conversations WHERE calls.conv_dbid = conversations.id;")
	
	#print the results for the call log
	print '\n[*] -- Calls Found --'
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
		print "\n[*] -- Found Contact --"
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
		print '\n[*] -- Found Account -- '
		print '[+] User: ' + str(row[0])
		print '[+] Skype Username: ' + str(row[1])
		print '[+] Location: ' + str(row[2]) + ', ' + str(row[3])
		print '[+] Profile Date: ' + str(row[4])
		
def main():
	#have the user set the path for the skype profile using the '-p' option
	parser = optparse.OptionParser("usage%prog -p <skype profile path> ")
	parser.add_option('-p', dest='pathName', type='string', help='specify skype profile path')
	(options,args) = parser.parse_args()
	
	pathName = options.pathName
	
	#check to make sure the path name isn't blank and that it exists
	if pathName == 'None':
		print parser.usage
		exit(0)
	elif os.path.isdir(pathName) == False:
		print '[!] Path does not exist: ' + pathName
		exit(0)
	else:
		skypeDB = os.path.join(pathName, 'main.db')
		#check to make sure the file exists
		if os.path.isfile(skypeDB):
			printProfile(skypeDB)
			printContacts(skypeDB)
			printCallLog(skypeDB)
			printMessages(skypeDB)
		else:
			print '[!] Skype database does not exist: ' + skypeDB

	
	
	"""
	skypeDB = 'main.db'
	printPRofile(skypeDB)
	"""
	
if __name__ == '__main__':
	main()