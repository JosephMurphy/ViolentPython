import nmap
import optparse

def nmapScan(tgtHost, tgtPort): #function to run a nmap scan
	nmScan = nmap.PortScanner() #create port scanner object
	nmScan.scan(tgtHost, tgtPort)
	state = nmScan[tgtHost]['tcp'][int(tgtPort)]['state']
	print " [*] " + tgtHost + " tcp " + tgtPort + " " + state

def main():

	parser = optparse.OptionParser('usage %prog -H <target host> -p <target port>')
	parser.add_option('-H', dest='tgtHost', type = "string", help = "Specify Target Host") #setting -H option to the target host
	parser.add_option("-p", dest="tgtPort", type = "string", help="Specify the target port") #setting -p option to the target port
	(options, args) = parser.parse_args()
	
	tgtHost = options.tgtHost #assigning option to a variable
	tgtPorts = str(options.tgtPort).split(",") #assigning option to a variable

	if (tgtHost == None) | (tgtPorts[0] == None): #if user doesn't enter 	options, prompt with instructions
		print parser.usage
		exit(0)
	
	for tgtPort in tgtPorts:
		nmapScan(tgtHost,tgtPort)


if __name__ == '__main__':
	main()
