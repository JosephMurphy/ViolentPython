import socket
import os
import sys

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

	if len(sys.argv) == 2: #checking if filename was provided as argument
		filename = sys.argv[1]
		if not os.path.isfile(filename): #check to see if file exists
			print '[-] ' + filename + " does not exist"
			exit(0)
		if not os.access(filename, os.R_OK): #check to see if you have read access
			print "[-] " + filename + " access denied"	
			exit(0)
		print "Reading vulnerabilities from " + filename

	
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
