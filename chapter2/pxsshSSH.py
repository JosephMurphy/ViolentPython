import pxssh

def send_command(s, cmd): #send ssh commands
	s.sendline(cmd)
	s.prompt()
	print s.before

def connect(host, user, password):
	try:
		s = pxssh.pxssh() #creating pxssh object
		s.login(host,user,password) #attempt to login to ssh server
		return s
	except:
		print '[-] Error Connecting'
		exit(0)

def main():
	s = connect('localhost', 'root', 'toor')
	send_command(s, 'cat /etc/shadow | grep root')

if __name__ == '__main__':
	main()
