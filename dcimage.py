from PIL import Image

	def getImage(filename):
	    try:
		image = Image.open(filename)
	    except IOError:
		pass
	    else:
		 return image
