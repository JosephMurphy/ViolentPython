import os
import optparse
from _winreg import *

#checks to see which recycle bin directory is being used by Windows
def returnDir():
	dirs = ['C:\\Recycler\\' , 'C:\\Recycled\\', 'C:\\$Recycle.Bin\\'] #array of possible recycle bin directories in Windows
	for recycleDir in dirs:
		if os.path.isdir(recycleDir): #check if the directory exists
			return recycleDir
		
	return None
	
#translate the sid to a readable user id	
def sid2user(sid):
	try:
		key = OpenKey(HKEY_LOCAL_MACHINE, "SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList" + '\\' + sid, 0, KEY_READ | KEY_WOW64_64KEY) 
		(value, type) = QueryValueEx(key, 'ProfileImagePath')
		print value
		user = value.split('\\')[-1]
		return user
	except Exception, e:
		print e
		return sid

def findRecycled(recycleDir):
	dirList = os.listdir(recycleDir)
	for sid in dirList:
		files = os.listdir(recycleDir + sid)
		user = sid2user(sid)
		print '\n[*] Listing Files for User: ' +str(user)
		
		for file in files:
			print '[+] found File: ' + str(file)

def main():
	recycledDir = returnDir()
	findRecycled(recycledDir)
	
if __name__ == '__main__':
	main()
	
