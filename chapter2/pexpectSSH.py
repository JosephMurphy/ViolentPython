import pexpect

PROMPT = ['# ', '>>> ',' \$ ']
def send_command(child,cmd):
	child.sendline(cmd)
	child.expect(PROMPT)
	print child.before

def connect(user,host,password): #attempts to connect to host over ssh with provided username, hostname, and password
	ssh_newkey = 'Are you sure you want to continue connecting' #string contains the prompt if it is a new ssh key
	connStr = 'ssh ' + user + '@' + host #command to start ssh connection
	child = pexpect.spawn(connStr)
	ret = child.expect([pexpect.TIMEOUT, ssh_newkey, '[P|p]assword:']) #sets expect response from server: timeout, newkey prompt, or password prompt
	if ret == 0: #no response from server/unexpected response
		print '[-] Error Connecting'
		return
	if ret == 1: #if prompted for new key
		child.sendline('yes') #send yes to command line
		ret = child.expect([pexpect.TIMEOUT, '[P|p]assword:'])
		if ret == 0:
			print '[-] Error Connecting'
			return

	child.sendline(password) #send the password to the command line
	child.expect(PROMPT)
	return child

def main():
	host = 'localhost'
	user = 'root'
	password = 'toor'
	child = connect(user,host,password)
	send_command(child, 'cat /etc/shadow | grep root') #searches for the root entry in the shadow file if the ssh connection is successful.

if __name__ == '__main__':
	main()
