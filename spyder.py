import httplib2, urlparse, operator
from BeautifulSoup import BeautifulSoup, SoupStrainer
import urllib, urllib2
DEBUG = 0

def getUrls(url, roothost):
	try:
		http = httplib2.Http()
		status, response = http.request(url)
		listing = []
		for link in BeautifulSoup(response, parseOnlyThese=SoupStrainer('a')):
		    if link.has_key('href'):
		        lnk = link['href']
		        host = urlparse.urlparse(lnk).hostname
		        if not host:
		        	lnk = "http://" + (roothost + "/" + lnk).replace("//","/")
		        	host = urlparse.urlparse(lnk).hostname
		       	if host == roothost:
		       		if DEBUG == 2:
		       			print "New SubLink " + lnk
		        	listing.append(lnk)
		        else:
		        	if DEBUG == 2:
		        		print "Skipping " + lnk
		return listing
	except:
		return []

def readURL(url):
	try:
		rep = urllib2.urlopen(url)
		return rep.read()
	except:
		return ""
def maxValue(dict):
	if len(dict) < 1:
		return ""
	return max(dict.iteritems(), key=operator.itemgetter(1))[0]

def rootURL(url):
	return urlparse.urlparse(url).hostname

def spyder(rooturl, maxiters=None):
	nrooturl = urlparse.urlparse(rooturl).hostname
	if not nrooturl == None:
		rooturl = "http://" + nrooturl + "/"
		roothost = urlparse.urlparse(rooturl).hostname
	else:
		roothost = rooturl
		rooturl = "http://" + rooturl + "/"
	checkedURL = []
	lengths = {}
	URLs = getUrls(rooturl,roothost)
	nURLS = []
	iters = 0
	while len(URLs) > 0:
		iters = iters + 1
		if maxiters:
			if iters > maxiters:
				break
		nURLS = []
		for url in URLs:
			if not url in checkedURL:
				if DEBUG >= 1:
					print "Checking URL " + url
				ln = len(readURL(url))
				lengths[url] = ln
				stubs = getUrls(url, roothost)
				for stub in stubs:
					if DEBUG == 2:
						print "Checking stub " + stub
					if not stub in checkedURL:
						nURLS.append(stub)
				checkedURL.append(url)
		URLs = nURLS
	if iters == 1:
		print "Unable to find."
		return ""

	maxURL = maxValue(lengths)
	if DEBUG >= 1:
		if maxURL == "":
			print "error!"
			return ""
		print "Iters: " + str(iters)
		print "Size: " + str(lengths[maxURL] * 16 / 1024)
	return maxURL

if __name__ == "__main__":	
	from optparse import OptionParser
	import sys
	parser = OptionParser()
	parser.add_option("-w","--website", dest="website", help="Website to crawl")
	parser.add_option("-l","--limit", dest="limit", help="Repetition limit")
	(options,args) = parser.parse_args()
	if options.website is None:
		print "You are required to input a website."
		parser.print_help()
		sys.exit(0)
	website = options.website
	limit = options.limit
	if limit is None:
		print spyder(website)
	else:
		try:
			limit = int(limit)
		except:
			limit = 50
		print spyder(website, limit)