import optparse
import socket
from socket import *
from threading import *

screenlock = Semaphore(value=1)

def connScan(tgtHost, tgtPort): #Function will attempt to connect to target host on specified host
	try:
		connSkt = socket(AF_INET, SOCK_STREAM) #create a TCP socket for ipv4
		connSkt.connect((tgtHost, tgtPort)) #attempt to connect
		connSkt.send('Violent Python\r\n') #send string data to host
		results = connSkt.recv(100) #store results of response
		screenlock.acquire() #lock screen so only one thread can print at a time	
		print '[+]tcp open on port '+ str(tgtPort) #open port message
		print '[+] ' + str(results) #print response
		connSkt.close()
	except:
		screenlock.acquire()	
		print '[-]tcp closed on port '+ str(tgtPort)+'\n' #closed port message
	finally:
		screenlock.release()
		connSkt.close()

def portScan(tgtHost, tgtPorts): #function will scan through ports to see what is open
	try:
		tgtIP = gethostbyname(tgtHost) #attempt to resolve hn to ip
	except:
		print '[-] Cannot resolve: Unknown host ' +tgtHost #can not resolve the host name

	try:
		tgtName = gethostbyaddress(tgtIP)
		print '\n[+]Scan results for: ' + tgtName[0]
	except:
		print '\n[+]Scan results for: ' +tgtIP
	setdefaulttimeout(1)
	for tgtPort in tgtPorts:
		print 'Scanning port ' + tgtPort
		t = Thread(target = connScan, args=(tgtHost, int(tgtPort))) #connect to host on tgtPort
		t.start() #start thread

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
	
	portScan(tgtHost,tgtPorts)


if __name__ == '__main__':
	main()
