import dpkt
import socket

#takes a pcap file, iterates through the file information to print the IP data for each packet.  Skips over none IP packets
def printPcap(pcap):
	for (ts, buf) in pcap:
		try:
			eth = dpkt.ethernet.Ethernet(buf)
			ip = eth.data
			src = socket.inet_ntoa(ip.src)
			dst = socket.inet_ntoa(ip.dst)
			print '[+] Source: ' + src + ' --> Destination: ' + dst
		except:
			pass

def main():
	#open the pcap file to look at
	f = open('capture')
	pcap = dpkt.pcap.Reader(f)
	printPcap(pcap)

if __name__ == '__main__':
	main()


