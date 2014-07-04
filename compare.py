#!/usr/bin/python

import os, glob
from time import sleep
from SimpleCV import *

current_images_path = './Screens'
current_images_path = '/Users/thomasbrandl/Google Drive/Screens'
previous_images_path = '/Users/thomasbrandl/Google Drive/Screens pre migration'
mismatch_images_path = current_images_path + '/Mismatches'

scale_factor = .5
border_width = int(10 ** scale_factor)

def openImage(img):
	try:
		_img = Image(img)
		return _img
	except cv2.error as e:
		print "Error opening image: %s" % cv2.error 

mismatch = []
for current_image_path in glob.glob('%s/*.png' % current_images_path):
	#img = Image(screen)
	current_image_name = os.path.basename(current_image_path)
	previous_image_path = '%s/%s' % (previous_images_path, current_image_name)

	if (os.path.isfile(previous_image_path)):
		print "opening current  %s..." % previous_image_path
		imgA = openImage(current_image_path).scale(scale_factor)
		print "opening previous ..."
		imgB = openImage(previous_image_path).scale(scale_factor)
		if imgA.width != imgB.width:
			print "Width does not match! Continuing ..."
			continue
		print "comparing ..."
		try:
			imgD = imgB - imgA
		except cv2.error as e:
			print "Error comparing image: %s" % cv2.error 
			mismatch.append(current_image_name)
		finally:
			# when the images are not the same size, image arithmetric (adding, subtracting) does not work
			# before we can compare them, the need the same image dimensions.
			diff_height = imgA.height - imgB.height
			if diff_height < 0:
				imgA = imgA.embiggen((imgA.width, imgB.height), Color.BLACK, (0,0))
			elif diff_height > 0:
				imgB = imgB.embiggen((imgA.width, imgA.height), Color.BLACK, (0,0))
			# now try again to find the differences	
			print imgA, imgB
			imgD = imgB - imgA

		blobs = imgD.binarize(thresh=0).erode().invert().findBlobs(maxsize=((imgD.width*imgD.height)/2), minsize=1000)
		# Dim previous version by 50% and add the difference to it
		imgX = imgB/2 + imgD
		if blobs:
			blobs.image = imgX
			#blobs.draw(color=Color.GREEN, width=5)
			for b in blobs:
				b.drawRect(color=Color.RED, width=border_width)

		matrix = imgD.getNumpy()
		mean = matrix.mean()
		if mean > 0.0:
			mismatch.append(current_image_name)
			imgX.save('%s/%s' % (mismatch_images_path, current_image_name))
		print mean

print mismatch



