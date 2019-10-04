#!/usr/bin/python
import sys
from PIL import Image

def getImage(filename):
	try:
	    image = Image.open(filename)
	except IOError:
	    pass
	else:
	    return image


def saveImage(filename,filedata):
	try:
	    image = Image.fromarray(filedata,"RGB")
		#Image.frombytes("RGB",(30,30),filedata)?
	except IOError:
	    pass
	else:
	    image.save(filename)


if len(sys.argv) == 2:
	filename = sys.argv[1]

print('Filename ',filename)
image = getImage(filename)
print('Image Data: ',image)
saveImage('New Image.bmp',[[233,101,101]])
