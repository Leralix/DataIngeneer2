#import sys
#sys.executable
#print(sys.executable)


#import xmltodict
#import urllib2
import feedparser


url = "https://www.senat.fr/rss/rapports.rss"
RSSparser = feedparser.parse(url)

#print(RSSparser.feed)
#print(RSSparser["entries"][0])

