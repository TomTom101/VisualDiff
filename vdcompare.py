#!/usr/bin/python

import sys, os, glob
from time import sleep
import argparse
from SimpleCV import *

__version__ = "0.1"

options = {}
args = []

mismatch = []

def init():
	global options

	cmdparser = argparse.ArgumentParser(prog=__file__)

	cmdparser.add_argument("current_image_path",
						help="Specify the folder with the latest screens")
	cmdparser.add_argument("previous_image_path",
						help="Specify the folder to compare the current ones to")
	cmdparser.add_argument("-O", "--output-path",
						default="./VisualDiff/compare/mismatches",
						help="Specify a folder to save the difference images. Will be put in a subfolder automatically, '.' is fine")
	cmdparser.add_argument("-S", "--scale",
						type=float,
						default=0.75,
						help=argparse.SUPPRESS)

	options = cmdparser.parse_args()

	if options.output_path[0] == '~':
		options.output_path = os.path.expanduser(options.output_path)

	# create a subfolder stating what we compared
	options.output_path = os.path.join(	options.output_path,
										"%s-vs-%s" % (	os.path.basename(os.path.normpath(options.current_image_path)),
														os.path.basename(os.path.normpath(options.previous_image_path))
													)
									)

	if not os.path.exists(options.output_path):
		os.makedirs(options.output_path)
		if not os.access(options.output_path, os.W_OK):
			print('Cannot write to output-path "%s"' % options.output_path)
			sys.exit(0)

def mask(imgA, imgB):
	tmp = (imgB - imgA)
	return tmp

def openImage(img):
	try:
		_img = Image(img)
		return _img
	except cv2.error as e:
		print "Error opening image: %s" % cv2.error

def markBlobs(img, border_width, color=Color.RED):
	# thresh 5 filters tiny changes we don't care about
	# max and minsize is by trial
	blobs = img.binarize(thresh=5).invert().findBlobs(
				maxsize=((img.width*img.height)/2),
				minsize=1000)
	if blobs:
		blobs.image = img
		for b in blobs:
			b.drawRect(color=color, width=border_width)
	# merge the drawing layer on the image. Otherwise drawings get lost when changing the source image in any way
	return img.applyLayers()

def main():
	global options
	init()
	border_width = int(5 ** options.scale)

	for current_image_path in glob.glob('%s/*.png' % options.current_image_path):
		current_image_name = os.path.basename(current_image_path)
		previous_image_path = '%s/%s' % (options.previous_image_path, current_image_name)

		if (os.path.isfile(previous_image_path)):
			print "opening %s" % current_image_name
			imgA = openImage(current_image_path).scale(options.scale)
			print "opening previous ..."
			imgB = openImage(previous_image_path).scale(options.scale)
			if imgA.width != imgB.width:
				# Not sure why this happened, screenshots are taken at a defined width of 1600px
				print "Width does not match! Continuing ..."
				continue
			print "comparing ..."

			if (imgA.height - imgB.height) != 0:
				# when the images are not the same size, image arithmetric (adding, subtracting) does not work
				# before we can compare them, they need the same image dimensions.
				diff_height = imgA.height - imgB.height
				if diff_height < 0:
					imgA = imgA.embiggen((imgA.width, imgB.height), Color.BLACK, (0,0))
				elif diff_height > 0:
					imgB = imgB.embiggen((imgA.width, imgA.height), Color.BLACK, (0,0))
				# now try again to find the differences
			imgD = mask(imgB, imgA)

			# Substract A from B, then B from A and add them. This way, we can also see black areas
			# that were added/removed
			imgD = markBlobs(imgD, border_width, Color.RED)
			imgE = markBlobs((imgA.invert() - imgB.invert()), border_width, Color.GREEN)
			imgX = imgD + imgE

			mean = imgD.getNumpy().mean()

			if mean > 0.0:
				mismatch.append(current_image_name)
				imgA.sideBySide(imgB) \
				.sideBySide(imgX) \
				.getPIL().save('%s/%s.%s' % (options.output_path, current_image_name[:-4], 'jpg'),
					quality=85, optimize=True, progressive=True)
			print mean

	print mismatch

if __name__ == '__main__':
	main()
