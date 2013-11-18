import pyPdf
import optparse
from pyPdf import PdfFileReader

def printMeta(filename):
	pdfFile = PdfFileReader(file(filename, 'rb'))
	docInfo = pdfFile.getDocumentInfo() #gets the meta data of pdf file, stores in a tuple
	print '[*] PDF MetaDate For: ' + str(filename)
	for metaItem in docInfo:
		print '[+] ' + metaItem + ':' + docInfo[metaItem]
		
def main():
	parser = optparse.OptionParser('usage %prog -F <PDF File Name>')
	parser.add_option('-F', dest = 'fileName', type = 'string', help = 'specify the pdf file name')
	(options, args) = parser.parse_args()
	fileName = options.fileName
	
	if fileName == None:
		print parser.usage
		exit(0)
	else:
		printMeta(fileName)

if __name__ == '__main__':
	main()