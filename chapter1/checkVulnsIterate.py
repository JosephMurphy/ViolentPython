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

	portList = [21,22,25,80,110,443]

	for x in range(107, 110): #iterate through IP address
		ip = '192.168.0.' + str(x)
		
		for port in portList: #iterate through the port list
			banner = retBanner(ip, port)
			if banner:
				print "[+] " + ip + ":" + str(port) +": "+ banner.strip('\n')
				checkVulns(banner)


if __name__ == '__main__':
	main()
