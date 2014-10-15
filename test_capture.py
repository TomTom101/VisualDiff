#!/usr/bin/python

import sys
import vdcapture
import datetime


def test_makeFilenameWithDate():
	sys.argv = ['vdcapture', '-U', 'http://www.google.com']
	vdcapture.init()

	filename = vdcapture.makeFilepath('http://www.ni.de/en/page/', vdcapture.options)
	assert filename == ("./VisualDiff/capture/Screens/www.ni.de/%s" % datetime.date.today(), "enpage")


def test_makeFilenameWithSubpath():
	sys.argv = ['vdcapture', '-U', 'http://www.google.com', '-P', 'version0']
	vdcapture.init()

	filename = vdcapture.makeFilepath('http://www.ni.de/en/page/', vdcapture.options)
	assert filename == ("./VisualDiff/capture/Screens/www.ni.de/version0", "enpage")	