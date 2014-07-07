#!/usr/bin/python

from os import path
import urllib
from xml.dom import minidom
import re
import subprocess
import optparse

__version__ = "0.1"

options = {}
args = []

def init():
	global options, args
	usage = """%prog [options] [http://example.net/ ...]

	Examples:
	%prog http://www.ni.de/            	# screengrab the live site (not supported yet)
	%prog -S --site-map		# Crawl Google sitemap, <url><loc>http://</loc></url>
	%prog -O --output-path	# Save files to Screens folder, defaults to ~/
	%prog -W --width		# width of the browser screen, defaults to 1280
	%prog -L --levels		# How many url path levels to go down (/en/company/ is on level 2), defaults to 2"""

	cmdparser = optparse.OptionParser(usage, version=("capture " + __version__))

	cmdparser.add_option("-O", "--output-path",
						type="string",
						default=path.expanduser("~"),
						help=optparse.SUPPRESS_HELP)
	cmdparser.add_option("-S", "--sitemap",
						type="string",
						help=optparse.SUPPRESS_HELP)
	cmdparser.add_option("-L", "--levels", type="int",
						default=5,
						help=optparse.SUPPRESS_HELP)
	cmdparser.add_option("-W", "--width",
						type="int",
						default=1280,
						help=optparse.SUPPRESS_HELP)

	(options, args) = cmdparser.parse_args()
	# if len(args) == 0:
	# 	cmdparser.print_usage()
	# 	raise RuntimeError("Must specify a URL to capture screens from")

def main():
	global options, args
	init()
	dom = minidom.parse(urllib.urlopen(options.sitemap))
	locations = dom.getElementsByTagName('loc')
	urls = []

	for node in locations:
		url = node.childNodes[0].nodeValue
		# only capture pages 5 levels down (no subpages)
		# de/ products/ komplete/ effects/ vintage-compressors/ = 5
		# won't find pages
		reg = r"\.[a-z]{2,3}/([^/]+/){,%d}$" % options.levels
		if re.search(reg, url):
	 		urls.append(url)
	print "Capturing %d urls" % len(urls)

	##urls = ['http://www.integration.native-instruments.de/de/products/komplete/effects/premium-tube-series/']

	for url in urls:
		subprocess.call([	"webkit2png",
							"--dir=%s" % (options.output_path),
							"-F",
							"-W " + str(options.width),
							"--js='var i=0; function scroll(){ i += 600; if (i > document.height) { window.scrollTo(0,0);webkit2png.start() } else { window.scrollTo(0, i); window.setTimeout(scroll, 500)}}; webkit2png.stop(); scroll();'",
							url
						])


if __name__ == '__main__':
	main()
	