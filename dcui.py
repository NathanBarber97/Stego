#!/usr/bin/env python3

from tkinter import filedialog
from tkinter import *
import dcimage
import dcstego
destimage = ''
srcimage = ''
secretFileName = ''
stegoFileName = ''
stegoimage =''
def destImage():
	filename = filedialog.askopenfilename(initialdir = "",title = "Select destination image")
	global destimage
	print("Filename:",filename)
	if filename != () and filename != '':
		destimage = dcimage.getImage(filename)
	print("Image:",destimage)

def srcImage():
	global secretFileName 
	secretFileName = filedialog.askopenfilename(initialdir = "",title = "Select source image")
	global srcimage
	if secretFileName != () and secretFileName != '':
		srcimage = dcimage.getImage(secretFileName)


def encrypt():
	global passEntry1	
	header = secretFileName+"@width"+str(srcimage.width)+"@height"+str(srcimage.height)
	dcimage.saveImage("secretimage.bmp",dcstego.hidemsg(destimage.tobytes(),srcimage.tobytes(),header.encode(),passEntry1.get()),destimage.size)


def stegoImage():
	global stegoFileName 
	stegoFileName = filedialog.askopenfilename(initialdir = "",title = "Select stego'd image")
	global stegoimage
	if stegoFileName != () and stegoFileName != '':
		stegoimage = dcimage.getImage(stegoFileName)
def decrypt():
	global passEntry2
	secretFileName,secretImage = dcstego.extractmsg(stegoimage.tobytes(),passEntry2.get())
	widthIndex = secretFileName.find("@width")
	heightIndex = secretFileName.find("@height")
	print("Secret ",secretFileName[:widthIndex], secretFileName[widthIndex+6:heightIndex],secretFileName[heightIndex+7:])
	dcimage.saveImage(secretFileName[:widthIndex],secretImage,(int(secretFileName[widthIndex+6:heightIndex]),int(secretFileName[heightIndex+7:])))

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
