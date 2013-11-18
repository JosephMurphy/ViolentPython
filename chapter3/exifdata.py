import urllib2
import optparse
from urlparse import urlsplit
from os.path import basename
from bs4 import BeautifulSoup
from PIL import Image
from PIL.ExifTags import TAGS

#use beautiful soup to find image tags
def findImages(url):
	print '[+] Finding images on ' + url
	urlContent = urllib2.urlopen(url).read() #open the url
	soup = BeautifulSoup(urlContent) #create a beautifulsoup object
	imgTags = soup.findAll('img') #find all image tags on the provided url and place in array
	return imgTags

#download image file from the source address in tag, write the binary contents of image to a file
def downloadImage(imgTag):
	try:
		print '[+] Downloading image...'
		imgSrc = imgTag['src']
		imgContent = urllib2.urlopen(imgSrc).read() #read the source address of the image
		imgFileName = basename(urlsplit(imgSrc)[2])
		imgFile = open(imgFileName, 'wb') #open file in write binary mode
		imgFile.write(imgContent) #write the content of the image to the file
		imgFile.close()
		return imgFileName
	except:
		return ''

#open file with PIL, check to see if exif data exists
def testForExif(imgFileName):
	try:
		exifData = {}
		imgFile = Image.open(imgFileName) #open the image file as PIL Image
		info = imgFile._getexif() #get exif data from image

		if info:
			for (tag, value) in info.items():
				decoded = TAGS.get(tag,tag)
				exifData[decoded] = value
			exifGPS = exifData['GPSInfo']

			if exifGPS:
				print '[*] ' + imgFileName + ' contains GPS MetaData'

	except:
		pass

def main():
	parser = optparse.OptionParser('usage%prog -u <target url>')
	parser.add_option('-u', dest='url', type = 'string', help = 'specify the url to download the image from')
	(options, args) = parser.parse_args()
	url = options.url

	if url == None:
		print parser.usage
		exit(0)
	else:
		imgTags = findImages(url)
		for imgTag in imgTags:
			imgFileName = downloadImage(imgTag)
			testForExif(imgFileName)

if __name__ == '__main__':
	main()
