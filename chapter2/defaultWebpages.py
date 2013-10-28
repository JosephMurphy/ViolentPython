import ftplib

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

host = '192.168.0.108'
username = 'anonymous'
password = 'asdasdasd'
ftp = ftplib.FTP(host) #set ftp connection
ftp.login(username, password) #login to the ftp server
returnDefault(ftp) #pass ftp connection to the returnDefault function
