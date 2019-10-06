#!/usr/bin/python3
#
#----------------------------------------------------------------------------------------------------------------------
# Source File: dcimage.py
# Program Usage: ./dcimage.py
#
# Date: October 06, 2019
# Designers: Matthew Baldock
# Programmers: Matthew Baldock 
#
# Notes:Contains function calls for Image Handling, opening and saving
#----------------------------------------------------------------------------------------------------------------------
import io
import sys
from PIL import Image
#----------------------------------------------------------------------------------------------------------------------
#getImage
#Takes filename parameter and tries to open an image file
#If successful returns PIL Image object
#----------------------------------------------------------------------------------------------------------------------
def getImage(filename):
	try:
	    image = Image.open(filename)
	except IOError:
	    pass
	else:
	    print("Got Image")
	    return image

#----------------------------------------------------------------------------------------------------------------------
#saveImage
#Takes filename, filedata and size parameters
#Attempts to create Image from bytes with specified name, data and size
#If successful saves image to disk	
#----------------------------------------------------------------------------------------------------------------------
def saveImage(filename,filedata,size):
	try:
	    print("Image Size: ",size)
	    print("File data ",len(filedata))
	    image = Image.frombytes("RGB",size,filedata,"raw")
	except IOError:
	    pass
	else:
	    image.save(filename)

