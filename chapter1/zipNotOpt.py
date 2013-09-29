import zipfile
import os
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

def doesExist(filename):
	if not os.path.isfile(filename):
		return False
	else:
		return True

def main():

	zname = raw_input("Enter the name of the zipfile: ") #prompt user for zipfile
	dname = raw_input("Enter the name of the dictionary file: ") #prompt user for name of dictionary file

	if doesExist(zname) & doesExist(dname): #check if the files exist
		zfile = zipfile.ZipFile(zname)
		passFile = open(dname)
		for line in passFile.readlines():
			password = line.strip('\n')
			t = Thread(target=extractFile, args=(zfile, password))
			t.start()	
			
		passFile.close()
	else:
		print "One of the files you entered does not exist"

if __name__ == '__main__':
	main()
