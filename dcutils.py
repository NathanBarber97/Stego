#!/usr/bin/env python3
#----------------------------------------------------------------------------------------------------------------------
# 
# Source File: dcutils.py
# Program Usage: ./dcutils.py
#
# Date: October 06, 2019
# Designers: Matthew Baldock
# Programmers: Matthew Baldock 
#
# Notes: Runs a Stegonography UI Application
# Takes a Cover image and an image to hide, encrypts the hidden image then encodes
# the bits into the cover image and saves as a new stego'd image
#----------------------------------------------------------------------------------------------------------------------

#imports and global variable calls
from tkinter import filedialog
from tkinter import *
import dcimage
import dcstego
destimage = ''
srcimage = ''
secretFileName = ''
stegoFileName = ''
stegoimage =''
#----------------------------------------------------------------------------------------------------------------------
#destImage
#Opens dialogue window to choose Destination/Cover image
#Sets object to "destimage"
#----------------------------------------------------------------------------------------------------------------------
def destImage():
	filename = filedialog.askopenfilename(initialdir = "",title = "Select destination image")
	global destimage
	print("Filename:",filename)
	if filename != () and filename != '':
		destimage = dcimage.getImage(filename)
#srcImage
#Opens dialogue window to choose Hidden/Source image
#Calls getImage from dcimage to return PIL Image object
#Sets object to "srcimage"
#Sets name of file to "secretFileName"
#
def srcImage():
	global secretFileName 
	secretFileName = filedialog.askopenfilename(initialdir = "",title = "Select source image")
	print("Filename:",secretFileName)
	global srcimage
	if secretFileName != () and secretFileName != '':
		srcimage = dcimage.getImage(secretFileName)

#----------------------------------------------------------------------------------------------------------------------
#encrypt
#If Cover image is more than 8 times bigger than the hidden image, encode name/size header and begin encryption
#Passes image objects, Cover image size and new file name to saveImage in dcimage
#Calls hidemsg in dcstego to get encrypted and encoded image bytes 
#Saves stego'd image
#----------------------------------------------------------------------------------------------------------------------
def encrypt():
	global passEntry1	
	if len(destimage.tobytes())/len(srcimage.tobytes()) > 8:
		header = secretFileName+"@width"+str(srcimage.width)+"@height"+str(srcimage.height)
		dcimage.saveImage("secretimage.bmp",dcstego.hidemsg(destimage.tobytes(),srcimage.tobytes(),header.encode(),passEntry1.get()),destimage.size)
	else:
	    print("File size to big to stego")

#----------------------------------------------------------------------------------------------------------------------
#stegoImage
#Opens dialogue window to choose Stego'd image
#Calls getImage from dcimage to return PIL Image object
#Sets object to "stegoimage"
#Sets name of file to "stegoFileName"
#----------------------------------------------------------------------------------------------------------------------
def stegoImage():
	global stegoFileName 
	stegoFileName = filedialog.askopenfilename(initialdir = "",title = "Select stego'd image")
	global stegoimage
	if stegoFileName != () and stegoFileName != '':
		stegoimage = dcimage.getImage(stegoFileName)
#----------------------------------------------------------------------------------------------------------------------
#decrypt
#Calls extractmsg from dcstego to retrieve decoded and decrypted bytes from stego'd image
#Passes in selected stedo image and password
#Retrieves filename and bytes of image, decodes size of file from "secretFileName"
#Calls saveImage from dcimage and saves hidden image as the original 
#----------------------------------------------------------------------------------------------------------------------
def decrypt():
	global passEntry2
	secretFileName,secretImage = dcstego.extractmsg(stegoimage.tobytes(),passEntry2.get())
	widthIndex = secretFileName.find("@width")
	heightIndex = secretFileName.find("@height")
	print("Secret ",secretFileName[:widthIndex], secretFileName[widthIndex+6:heightIndex],secretFileName[heightIndex+7:])
	dcimage.saveImage(secretFileName[:widthIndex],secretImage,(int(secretFileName[widthIndex+6:heightIndex]),int(secretFileName[heightIndex+7:])))


#----------------------------------------------------------------------------------------------------------------------
# UI Window objects and their labels
#----------------------------------------------------------------------------------------------------------------------
root = Tk()
root.title("Stegostaurus")
topFrame = Frame(root)
topFrame.pack()
blankFrame = Frame(root)
blankFrame.pack()
bottomFrame = Frame(root)
bottomFrame.pack(side=BOTTOM)
passEntry1 = Entry(topFrame)
passLabel1 = Label(topFrame,text="Password:")
passEntry2 = Entry(bottomFrame)
passLabel2 = Label(bottomFrame,text="Password:")
hiddenLabel = Label(blankFrame,text="\n\n")
hiddenLabel.pack()
hideLabel = Label(topFrame, text="Hiding",fg="brown")
revealLabel = Label(bottomFrame,text="Revealing",fg="brown")
hideLabel.pack(side=TOP)
revealLabel.pack(side=TOP)
#Hiding Image Buttons
encryptButton = Button(topFrame,text="Encrypt",command=encrypt)

getDestButton = Button(topFrame,text="Get Target Image",command=destImage)

getSourceButton = Button(topFrame,text="Get Image to Hide",command=srcImage)
#Revealing Image Buttons
getSecretButton = Button(bottomFrame,text="Get Secret Image",command=stegoImage)
decryptButton = Button(bottomFrame,text="Decrypt",command=decrypt)


#Packing Buttons
encryptButton.pack(side=BOTTOM)
passEntry1.pack(side=BOTTOM)
passLabel1.pack(side=BOTTOM)


getDestButton.pack(side=LEFT)
getSourceButton.pack(side=LEFT)

getSecretButton.pack(side=TOP)
decryptButton.pack(side=BOTTOM)
passEntry2.pack(side=BOTTOM)
passLabel2.pack(side=BOTTOM)



root.mainloop()
