import zipfile
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

	zfile = zipfile.ZipFile("unzipme.zip") #specify the zipfile
	passFile = open("dictionary.txt","r") #open dictionary file

	for line in passFile.readlines():
		password = line.strip('\n')
		t = Thread(target=extractFile, args=(zfile, password))
		t.start()	
		
	passFile.close()

if __name__ == '__main__':
	main()
