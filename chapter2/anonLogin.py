import ftplib

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

host = '192.168.0.108'
anonLogin(host)
