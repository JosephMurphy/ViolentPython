import crypt

def testPass(cryptpass): #Function to test dictionary against pw hash
	salt = cryptpass[0:2] #salt is first two characters
	
	dictFile = open('dictionary.txt','r') #opening dictionary file
	for word in dictFile.readlines(): #iterating through file
		word = word.strip('\n')
		cryptWord = crypt.crypt(word,salt)
		if (cryptWord == cryptpass): #compare dict to pw hash
			print "[+] Found password: " + word
			return
	dictFile.close()	
	print "[-] Could not find password"
	return

def main():
	passFile = open('passwords.txt','r') #open file with passwords
	for line in passFile.readlines(): #iterate through file
		if ":" in line:
			user = line.split(":")[0]
			cryptpass = line.split(":")[1].strip("\n")
			print "[*] Cracking password for " + user
			testPass(cryptpass)

if __name__ == "__main__":
	main()
