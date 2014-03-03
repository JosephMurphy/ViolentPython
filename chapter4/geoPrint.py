import dpkt
import socket
import pygeoip
import optparse

#global variable for the GeoIP database
gi = pygeoip.GeoIP('/opt/GeoIP/Geo.dat')

#look up the geolocation of provided IP addresses
def retGeoStr(ip):
	try:
		rec = gi.record_by_name(ip)
		city = rec['city']
		country = rec['country_code3']
		#check to see if there is a city record for the IP
		if city != '':
			geoLoc = city + ', ' + country
		else:
			geoLoc = country

		return geoLoc
	except Exception, e:
		return 'Unregistered IP Address'

#takes a pcap file, iterates through the file information to print the IP data for each packet.  Skips over none IP packets
def printPcap(pcap):
	for (ts, buf) in pcap:
		try:
			eth = dpkt.ethernet.Ethernet(buf)
			ip = eth.data
			src = socket.inet_ntoa(ip.src)
			dst = socket.inet_ntoa(ip.dst)
			print '[+] Source: ' + src + ' --> Destination: ' + dst
			#get the geolocation of source and Destrination IP's, print
			print '[+] Source: ' + retGeoStr(src) + ' --> ' + retGeoStr(dst)
		except:
			pass

def main():
	parser = optparse.OptionParser('usage%prog -p <pcap file>')
	parser.add_option('-p', dest='pcapFile', type='string', help='specify the pcap file location')
	(options, args) = parser.parse_args()
	#check to make sure the pcap file was provided
	if options.pcapFile == None:
		print parser.usage
		exit(0)

	pcapFile = options.pcapFile
	#open the pcap
	f = open(pcapFile)
	pcap = dpkt.pcap.Reader(f)
	printPcap(pcap)

if __name__ == '__main__':
	main()


