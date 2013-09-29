import socket
def retBanner(ip, port):
	try:
		socket.setdefaulttimeout(2)
		s = socket.socket()
		s.connect((ip, port)) #connect to provided IP addresa
		banner = s.recv(1024) #get banner from IP address
		return banner
	except Exception, e:
		return str(e)

def checkVulns(banner):
	if ('FreeFloat Ftp Server (Version 1.00)' in banner):
		print '[+] Server is vulnerable'
	elif ('vsFTPd 2.3.5' in banner):
		print '[+] Server is vulnerable'
	else:
		print '[-] Server is not vulnerable'
	return

def main():
	ip1 = '192.168.0.110' #bad ip
	ip2 = '192.168.0.108' #ip of virtual machine with FTP running
	port = 21

	banner1 = retBanner(ip1, port)
	if banner1:
		print '[+] ' +ip1 + ': ' + banner1.strip('\n')
		checkVulns(banner1)

	banner2 = retBanner(ip2, port)
	if banner2:
		print '[+] ' +ip2 + ': ' + banner2.strip('\n')
		checkVulns(banner2)

if __name__ == '__main__':
	main()
