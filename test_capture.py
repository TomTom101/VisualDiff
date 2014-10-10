#!/usr/bin/python

import sys
import vdcapture


def test_makeFilenameWithDate():
	sys.argv = ['vdcapture', '-U', 'http://www.google.com']
	vdcapture.init()

	filename = vdcapture.makeFilepath('http://www.ni.de/en/page/', vdcapture.options)
	assert filename == ("./VisualDiff/capture/Screens/www.ni.de/2014-10-10", "enpage")


