import xmltodict
import urllib2
url = "https://www.senat.fr/rss/rapports.rss"

file = urllib2.urlopen(url)
data = file.read()
file.close()

