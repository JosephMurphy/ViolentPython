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

	f = open("vuln_banners.txt", "r") #open text file in read only
	for line in f.readlines(): #read each line in the text file to get the banner
		if line.strip('\n') in banner:
			print "[+] Server is vulnerable: " +banner.strip('\n')

	f.close()
	return

def main():

	portList = [21,22,25,80,110,443] #ports to check connection too

	for x in range(107, 110): #iterate through IP address
		ip = '192.168.0.' + str(x)
		
		for port in portList: #iterate through the port list
			banner = retBanner(ip, port)
			if banner:
				print "[+] " + ip + ":" + str(port) +": "+ banner.strip('\n')
				checkVulns(banner)


if __name__ == '__main__':
	main()
