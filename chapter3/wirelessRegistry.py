import mechanize
import urllib
import re
import urlparse
import os
import optparse
from _winreg import *

#access the wigle database to determine the geolocation of mac address
def wiglePrint(username, password, netid):
	browser = mechanize.Browser() #start the mechanize browser to interact with wigle
	browser.open('http://wigle.net')
	reqData = urllib.urlencode({'credential_0': username, 'credential_1': password}) #set login credentials
	browser.open('https://wigle.net/gps/gps/main/login', reqData) #send credentials to the website
	params = {}
	params['netid'] = netid
	reqParams = urllib.urlencode(params) #url encode mac address
	respURL = 'http://wigle.net/gps/gps/main/confirmquery/'
	resp = browser.open(respURL, reqParams).read() #send mac address to wigle.net, read results
	mapLat = 'N/A'
	mapLon = 'N/A'
	rLat = re.findall(r'maplat=.*\&', resp)
	if rLat:
		mapLat = rLat[0].split('&')[0].split('=')[1]
	rLon = re.findall(r'maplon=.*\&', resp)
	if rLon:
		mapLon = rLon[0].split
	
	print '[-] Lat: ' +mapLat+ ', Lon: ' + mapLon

#function converts the hex bytes for the mac address to human readable format
def val2addr(val):
	addr = ""
	for ch in val:
		addr += '%02x '% ord(ch)
		
	addr = addr.strip(' ').replace(' ', ':')[0:17]
	return addr

def printNets(username, password):
	#setting the registry key to be used
	net = "SOFTWARE\Microsoft\Windows NT\CurrentVersion\NetworkList\Signatures\Unmanaged"
	key = OpenKey(HKEY_LOCAL_MACHINE, net, 0, KEY_READ | KEY_WOW64_64KEY) #open the registry key
	print QueryInfoKey(key)
	print '\n[*] Networks you have joined.'	
	
	for i in range(10):
		try:
			guid = EnumKey(key, i)
			netKey = OpenKey(key, str(guid))
			(n, addr, t) = EnumValue(netKey, 5)
			(n, name, t) = EnumValue(netKey, 4)	
			macAddr = val2addr(addr)
			netName = str(name)
			print "[+] " + netName + " " + macAddr
			wiglePrint(username, password, macAddr)
			CloseKey(netKey)
		except Exception, e:
			print e
			
			
def main():
	parser = optparse.OptionParser("usage%prog -u <wigle username> -p <wigle password>")
	parser.add_option('-u', dest='username', type = 'string', help = 'enter the wigle username')
	parser.add_option('-p', dest='password', type = 'string', help = 'enter the wigle password')

	(options, args) = parser.parse_args()
	username = options.username
	password = options.password
	
	if (username == None) | (password == None):
		print parser.usage
		exit(0)
	else:
		printNets(username, password)
	

if __name__ == "__main__":
	main()