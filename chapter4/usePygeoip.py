import pygeoip
gi = pygeoip.GeoIP('/opt/GeoIP/Geo.dat') #location of the GeoIP database from MaxMind

def printRecord(tgt):
	#look up the provided target IP address in the GeoIP database
	rec = gi.record_by_name(tgt)
	#print rec
	#data was stored in the 'rec' list. Pull back data from the list
	city = rec['city']
	region = rec['region_code']
	country = rec['country_name']
	longitude = rec['longitude']
	lat = rec['latitude']

	print '[*] Target: '+ tgt + ' Geo-located.'
	print '[+] ' + str(city) + ', ' + str(region) + ', ' + str(country)
	print '[+] Latitude: ' + str(lat) + ', Longitude: ' + str(longitude)

#hardcoded target information.
tgt = '173.255.226.98'
printRecord(tgt)
