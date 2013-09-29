import zipfile
import optparse
from threading import Thread

def extractFile(zfile, password):
	print "Guessing " +password
	try:
		zfile.extractall(pwd=password) #attempt to extract file with guess
		print "[+] The password is: " +password
		return password
	except:
		print "[-] " + password + " was incorrect"
		return

def main():

	parser = optparse.OptionParser("usage%prog " +"-f <zipfile> -d <dictionary>")
	parser.add_option("-f", dest="zname", type="string", help = "specify zip file")
	parser.add_option("-d", dest="dname", type="string", help = "specify dictionary file")
	(options, args) = parser.parse_args()

	if (options.zname == None) | (options.dname == None): #check if names were blank
		print parser.usage
		exit(0)
	else:
		zname = options.zname
		dname = options.dname

	zfile = zipfile.ZipFile(zname)
	passFile = open(dname)
	for line in passFile.readlines():
		password = line.strip('\n')
		t = Thread(target=extractFile, args=(zfile, password))
		t.start()	
		
	passFile.close()

if __name__ == '__main__':
	main()
