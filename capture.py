#!/usr/bin/python

import sys
from os import path
import urllib
from xml.dom import minidom
import re
import subprocess
import optparse
import urlparse as url

__version__ = "0.1"

options = {}
args = []

def init():
	global options, args
	usage = "%prog [options] [http://example.net/ ...]"

	cmdparser = optparse.OptionParser(usage, version=("capture " + __version__))

	cmdparser.add_option("-O", "--output-path",
						type="string",
						default="./VisualDiff/capture/Screens",
						help="Save files to Screens folder, defaults to ./VisualDiff/capture/Screens")
	cmdparser.add_option("-S", "--sitemap",
						type="string",
						help="Crawl Google sitemap, <url><loc>http://</loc></url>")
	cmdparser.add_option("-U", "--url",
						type="string",
						help=optparse.SUPPRESS_HELP)
	cmdparser.add_option("-L", "--levels", type="int",
						default=5,
						help="How many url path levels to go down (/en/company/ is on level 2), defaults to 2")
	cmdparser.add_option("-W", "--width",
						type="int",
						default=1280,
						help="Width of the browser screen, defaults to 1280")
	
	(options, args) = cmdparser.parse_args()
	
	if not options.output_path:
		cmdparser.print_usage()

	if len(args) > 0:
		_url = url.urlparse(args[0])
		if _url.netloc and __url.scheme:
			options.url = args[0]

	# If both or none are set, we throw an error
	if bool(options.sitemap) == bool(options.url):
		print("Must specify a URL OR sitemap.")
		cmdparser.print_usage() 
		sys.exit(0)
		
	# if len(args) == 0:
	# 	cmdparser.print_usage()
	# 	raise RuntimeError("Must specify a URL to capture screens from")

def webkit2png(url):
	global options, args
	subprocess.call([	"webkit2png",
						"--dir=%s" % (options.output_path),
						"-F",
						"-W " + str(options.width),
						"--js='var i=0; function scroll(){ i += 600; if (i > document.height) { window.scrollTo(0,0);webkit2png.start() } else { window.scrollTo(0, i); window.setTimeout(scroll, 500)}}; webkit2png.stop(); scroll();'",
						url
					])
	
def main():
	global options, args
	init()

	if(options.url):
		webkit2png(options.url)
		return
	try:
		dom = minidom.parse(urllib.urlopen(options.sitemap))
		locations = dom.getElementsByTagName('loc')
	except Exception:
		print("Sitemap could not be parsed. Check https://support.google.com/webmasters/answer/183668")
		sys.exit(0)


	urls = []

	for node in locations:
		url = node.childNodes[0].nodeValue
		# only capture pages 5 levels down (no subpages)
		# de/ products/ komplete/ effects/ vintage-compressors/ = 5
		# won't find pages
		reg = r"\.[a-z]{2,3}/([^/]+/){,%d}$" % options.levels
		if re.search(reg, url):
	 		urls.append(url)
	print "Capturing %d urls form sitemap" % len(urls)

	##urls = ['http://www.integration.native-instruments.de/de/products/komplete/effects/premium-tube-series/']

	for url in urls:
		webkit2png(url)


if __name__ == '__main__':
	main()
