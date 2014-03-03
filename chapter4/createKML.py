import dpkt
import socket
import pygeoip
import optparse

#global variable for the geolocation database
gi = pygeoip.GeoIP('/opt/GeoIP/Geo.dat')

#resolve an ip address to a specific geolocation, create a KML placemarker for Google Earth
def retKML(ip):
	#rec = gi.record_by_name(ip)
	try:	
		rec = gi.record_by_name(ip)
		longitude = rec['longitude']
		lat = rec['latitude']
		kml = ('<Placemark>\n<name>' + ip + '</name>\n<Point>\n<coordinates>' + longitude + ',' +lat+ '</coordinates>\n</Point>\n</Placemark>\n')
		return kml
	except Exception, e:
		return ''

#resolve IP address from the pcap file, send to retKML to create KML entries
def plotIPs(pcap):
	kmlPts = ''
	for (ts, buf) in pcap:
		try:
			eth = dpkt.ethernet.Ethernet(buf)
			ip = eth.data
			src = socket.inet_ntoa(ip.src)
			#send source IP to create KML entry
			srcKML = retKML(src)
			dst = socket.inet_ntoa(ip.dst)
			#send destination IP to create KML entry
			dstKML = retKML(dst)
			kmlPts = kmlPts + scrKML + dstKML
		except:
			pass
	return kmlPts

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

	#create the kml header
	kmlheader = '<?xml version="1.0" encoding="UTF-8"?>\n<kml xmlns="https:www.opengis.net/kml/2.2">\n<Document>\n'
	#create the kml footer
	kmlfooter = '</Document>\n</kml>\n'
	#create the kml document by combing header, pcap analysis results, and the footer
	kmldoc = kmlheader+plotIPs(pcap)+kmlfooter
	print kmldoc

if __name__ == '__main__':
	main()
