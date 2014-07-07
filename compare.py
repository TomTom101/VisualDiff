#!/usr/bin/python

import os, glob
from time import sleep
import optparse
from SimpleCV import *

__version__ = "0.1"

options = {}
args = []

mismatch = []

def init():
	global options, args
	usage = """%prog [options] ~/Screens-A ~/Screens-B

	Examples:
	%prog ~/Screens-A/ ~/Screens-B/           	# compare folder Screens-A to Screens-B
	%prog -S --scale		# Crawl Google sitemap, <url><loc>http://</loc></url>
	%prog -O --output-path	# Save files to specified folder, defaults to ./VisualDiff/compare/mismatches"""

	cmdparser = optparse.OptionParser(usage, version=("capture " + __version__))

	cmdparser.add_option("-O", "--output-path",
						type="string",
						default="./VisualDiff/compare/mismatches",
						help=optparse.SUPPRESS_HELP)
	cmdparser.add_option("-S", "--scale",
						type="float",
						default=0.75,
						help=optparse.SUPPRESS_HELP)

	(options, args) = cmdparser.parse_args()

	if len(args) != 2:
	 	cmdparser.print_usage()
	 	raise RuntimeError("Must define 2 folders to compare!")

	if not os.path.exists(options.output_path):
		os.makedirs(options.output_path)
		if not os.access(options.output_path, os.W_OK):
			raise RuntimeError('Cannot write to output-path "%s"' % options.output_path)

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
	global options, args
	init()
	border_width = int(5 ** options.scale)

	for current_image_path in glob.glob('%s/*.png' % args[0]):
		current_image_name = os.path.basename(current_image_path)
		previous_image_path = '%s/%s' % (args[1], current_image_name)

		if (os.path.isfile(previous_image_path)):
			print "opening current  %s..." % current_image_name
			imgA = openImage(current_image_path).scale(options.scale)
			print "opening previous ..."
			imgB = openImage(previous_image_path).scale(options.scale)
			if imgA.width != imgB.width:
				# Not sure why this happened, screenshots are taken at a defined width of 1600px
				print "Width does not match! Continuing ..."
				continue
			print "comparing ..."
			try:
				imgD = mask(imgB, imgA)
			except cv2.error as e:
				print "Error comparing image: %s" % cv2.error
				mismatch.append(current_image_name)
			finally:
				# when the images are not the same size, image arithmetric (adding, subtracting) does not work
				# before we can compare them, they need the same image dimensions.
				diff_height = imgA.height - imgB.height
				if diff_height < 0:
					print imgA.width, imgB.height
					imgA = imgA.embiggen((imgA.width, imgB.height), Color.BLACK, (0,0))
				elif diff_height > 0:
					print imgA.width, imgA.height
					imgB = imgB.embiggen((imgA.width, imgA.height), Color.BLACK, (0,0))
				# now try again to find the differences
				imgD = mask(imgB, imgA)

			# Substract A from B, then B from A and add them. This way, we can also see black areas
			# that were added/removed
			imgD = markBlobs(imgD, border_width, Color.GREEN)
			imgE = markBlobs((imgA.invert() - imgB.invert()), border_width, Color.RED)
			imgX = imgD + imgE

			matrix = imgD.getNumpy()
			mean = matrix.mean()

			if mean > 0.0:
				mismatch.append(current_image_name)
				imgB.sideBySide(imgA) \
				.sideBySide(imgX) \
				.save('%s/%s.%s' % (options.output_path, current_image_name[:-4], 'jpg'))
			print mean

	print mismatch

if __name__ == '__main__':
	main()
