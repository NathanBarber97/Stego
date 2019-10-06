#!/usr/bin/env python3

from tkinter import filedialog
from tkinter import *
import dcimage
destimage = ''
srcimage = ''
def destImage():
	filename = filedialog.askopenfilename(initialdir = "",title = "Select destination image")
	global destimage
	print("Filename:",filename)
	if filename != () and filename != '':
		destimage = dcimage.getImage(filename)
	print("Image:",destimage)

def srcImage():
	filename = filedialog.askopenfilename(initialdir = "",title = "Select source image")
	global srcimage
	print("Filename:",filename)
	if filename != () and filename != '':
		srcimage = dcimage.getImage(filename)
	print("Image:",srcimage)


def encrypt():
	global passEntry
	print("Entry Value:",passEntry.get())
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
getSecretButton = Button(bottomFrame,text="Get Secret Image")
decryptButton = Button(bottomFrame,text="Decrypt")


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
