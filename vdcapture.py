#!/usr/bin/python

import sys
import os
import datetime
import urllib
from xml.dom import minidom
import re
import subprocess
import argparse
import urlparse

__version__ = "0.1"

options = {}

def init():
	global options

	cmdparser = argparse.ArgumentParser(prog=__file__)

	cmdparser.add_argument("-U", "--single-url",
						help="The path to the latest screens")

	cmdparser.add_argument("-O", "--output-path",
						default="./VisualDiff/capture/Screens",
						help="Save files to Screens folder, defaults to ./VisualDiff/capture/Screens")
	cmdparser.add_argument("-P", "--sub-path",
						help="Save files to Screens folder, defaults to ./VisualDiff/capture/Screens")	
	cmdparser.add_argument("-S", "--sitemap",
						help="Crawl Google sitemap, <url><loc>http://</loc></url>")
	cmdparser.add_argument("-J", "--js",
						default=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'init.js'),
						help=argparse.SUPPRESS)	
	cmdparser.add_argument("-L", "--levels",
						type=int,
						default=5,
						help="How many url path levels to go down (/en/company/ is on level 2), defaults to 2")
	cmdparser.add_argument("-W", "--width",
						type=int,
						default=1280,
						help="Width of the browser screen, defaults to 1280")
	
	options = cmdparser.parse_args()

	if options.single_url:
		_url = urlparse.urlparse(options.single_url)
		if not _url.netloc or not _url.scheme:
			argparse.print_help()
			sys.exit(0)
			

	if options.js:
		with open (options.js, "r") as _file:
			options.js = re.sub(r"([\n\t]+|\s{2,})", '', _file.read())

	# If both or none are set, we throw an error
	if bool(options.sitemap) == bool(options.single_url):
		print("Must specify a URL OR sitemap.")
		cmdparser.print_usage() 
		sys.exit(0)


def webkit2png(url, options):
	parameters = [	"webkit2png",
						"--dir=%s" % (options.output_path),
						"-F",
						"--filename=%s" % (options.filename),
						"-W " + str(options.width),
						"--js='%s'" % (options.js),
						url
					]
	subprocess.call(parameters)
	
def makeFilepath(url, options):
	""" returns an array ([path], [filename]) """
	_url = urlparse.urlparse(url)
	pathparts = []
	pathparts.append(options.output_path)
	pathparts.append(_url.netloc)
	pathparts.append(str(datetime.date.today()))

	return (os.path.join(*pathparts), re.sub('\W', '', _url.path or 'index'))

def main():
	global options
	init()

	base_output_path = options.output_path

	if(options.single_url):
		# duplicate code below
		(options.filename, subdir) = makeFilename(options.single_url)
		options.output_path = '%s/%s/%s' % (base_output_path, subdir, datetime.date.today())
		# webkit2png will create the path if it does not exist
		webkit2png(options.single_url, options)
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
		# only capture pages options.levels down (no subpages)
		# de/ products/ komplete/ effects/ vintage-compressors/ = 5
		# won't find pages below this level
		reg = r"\.[a-z]{2,3}/([^/]+/){,%d}$" % options.levels
		if re.search(reg, url):
	 		urls.append(url)
	print "Capturing %d of %d urls from sitemap" % (len(urls), len(locations))

	for url in urls:
		(options.output_path, options.filename) = makeFilepath(url, options)
		webkit2png(url, options)
		


if __name__ == '__main__':
	main()
