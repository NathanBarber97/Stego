#!/usr/bin/python
import io
import sys
from PIL import Image

def getImage(filename):
	try:
	    image = Image.open(filename)
	except IOError:
	    pass
	else:
	    return image

def toBytes(filedata):
	byteArr = io.BytesIO()
	image.save(byteArr,format=image.format)
	return byteArr.getvalue()
	
def saveImage(filename,filedata):
	try:
	    image = Image.frombytes("RGB",(3,3),filedata,"raw")#Image.fromarray(filedata,"RGB")
		#Image.frombytes("RGB",(30,30),filedata)?
	except IOError:
	    pass
	else:
	    image.save(filename)


#Testing
#if len(sys.argv) == 2:
	filename = sys.argv[1]

#print('Filename ',filename)
#image = getImage(filename)
#print('Image Data: ',image)
#print('Image as Bytes', image.tobytes())
#byteArr = io.BytesIO()
#image.save(byteArr,format=image.format)
#print('Image as array', byteArr.getvalue())
#saveImage('Pillow_bytes.bmp',image.tobytes())
#saveImage('IO_bytes.bmp',byteArr.getvalue())
