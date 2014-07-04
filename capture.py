#!/usr/bin/python

import urllib
from xml.dom import minidom
import re
import subprocess

sitemap = 'http://native:native@www.integration.native-instruments.de/en/sitemap'
#sitemap = './sitemap.xml'

dom = minidom.parse(urllib.urlopen(sitemap))
#dom = minidom.parse(open(sitemap))

output_path = '/Users/thomasbrandl/Google Drive/Screens'

locations = dom.getElementsByTagName('loc')
urls = []
for node in locations:
	url = node.childNodes[0].nodeValue
	# only capture pages 5 levels down (no subpages)
	# de/ products/ komplete/ effects/ vintage-compressors/ = 5
	# won't find pages
	if re.search(r"\.de/([^/]+/){,5}$", url):
 		urls.append(url)
print len(urls)

##urls = ['http://www.integration.native-instruments.de/de/products/komplete/effects/premium-tube-series/']

for url in urls:
	subprocess.call([	"webkit2png",
						"--dir=%s" % (output_path),
						"-F",
						"-W 1600",
						"--js='var i=0; function scroll(){ i += 600; if (i > document.height) { window.scrollTo(0,0);webkit2png.start() } else { window.scrollTo(0, i); window.setTimeout(scroll, 500)}}; webkit2png.stop(); scroll();'",
						url
					])



