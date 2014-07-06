#!/usr/bin/python

import os, glob
from time import sleep
from SimpleCV import *

base_images_path = os.path.expanduser('~')
current_images_path = base_images_path + '/Google Drive/Screens'
previous_images_path = base_images_path + '/Google Drive/Screens pre migration'
mismatch_images_path = current_images_path + '/Mismatches'

scale_factor = .75
border_width = int(5 ** scale_factor)

mismatch = []


def mask(imgA, imgB):
	tmp = (imgB - imgA)
	return tmp

def openImage(img):
	try:
		_img = Image(img).scale(scale_factor)
		return _img
	except cv2.error as e:
		print "Error opening image: %s" % cv2.error

def markBlobs(img, color=Color.RED):
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

for current_image_path in glob.glob('%s/*.png' % current_images_path):
	current_image_name = os.path.basename(current_image_path)
	previous_image_path = '%s/%s' % (previous_images_path, current_image_name)

	if (os.path.isfile(previous_image_path)):
		print "opening current  %s..." % previous_image_path
		imgA = openImage(current_image_path).scale(scale_factor)
		print "opening previous ..."
		imgB = openImage(previous_image_path).scale(scale_factor)
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
				imgA = imgA.embiggen((imgA.width, imgB.height), Color.BLACK, (0,0))
			elif diff_height > 0:
				imgB = imgB.embiggen((imgA.width, imgA.height), Color.BLACK, (0,0))
			# now try again to find the differences
			imgD = mask(imgB, imgA)

		# Substract A from B, then B from A and add them. This way, we can also see black areas
		# that were added/removed
		imgD = markBlobs(imgD, Color.RED)
		imgE = markBlobs((imgA.invert() - imgB.invert()), Color.GREEN)
		imgX = imgD + imgE

		matrix = imgD.getNumpy()
		mean = matrix.mean()

		if mean > 0.0:
			mismatch.append(current_image_name)
			imgB.sideBySide(imgA) \
			.sideBySide(imgX) \
			.save('%s/%s.%s' % (mismatch_images_path, current_image_name[:-4], 'jpg'))
		print mean

print mismatch

