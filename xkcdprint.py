#!/usr/bin/env python
"""This script fetches comic(s) from xkcd.com (using xkcd python module) and outputs them to an Epson thermal
printer using the python-escpos module"""
import escpos
import escpos.printer
import xkcd
import textwrap
import sys
import getopt
from random import randint
from PIL import Image

usageText = 'Usage: xkcdprint.py [-n <number of comics to print>] [-r] [-i <comicid>]\nDefaults to printing latest comic.'
nComicsToPrint = 1
nComicsPrinted = 0
comicRandom = False
maxPixelWidth = 512
nStartComic = xkcd.getLatestComic().number

try:
    opts, args = getopt.getopt(sys.argv[1:], "hn:ri:", ["help", "to-print=", "random", "comicid="])
except getopt.GetoptError:
    print(usageText)
    sys.exit(2)

for opt, arg in opts:
    if opt in ("-h", "--help"):
        print(usageText)
        sys.exit()
    elif opt in ("-r", "--random"):
        nStartComic = randint(1, xkcd.getLatestComicNum())
    elif opt in ("-i", "--comicid"):
        if 0 < int(arg) <= xkcd.getLatestComicNum():
            nStartComic = int(arg)
        else:
            print("Error: Comic ID specified is out of valid range. Please specify a comic ID between 1 and " + str(xkcd.getLatestComicNum()))
            sys.exit(1)
    elif opt in ("-n", "--to-print"):
        nComicsToPrint = int(arg)
        print("Printing " + str(nComicsToPrint) + " comics.")

if nComicsToPrint > 1:
    print("Comic # " + str(nStartComic) + " and " + str(nComicsToPrint - 1) + " previous comics will be printed.")
else:
    print("Comic # " + str(nStartComic) + " selected for printing.")

# Initialize Epson thermal printer using usb-id (here using TM-T20II)
p = escpos.printer.Usb(0x04b8, 0x0e15)

while nComicsPrinted < nComicsToPrint:
    comic = xkcd.getComic(nStartComic - nComicsPrinted)
    comicImg = comic.download()
    comicAltText = textwrap.wrap(comic.getAsciiAltText().decode('utf-8'), 40)
    img = Image.open(comicImg.encode('utf-8'))
    imgWidth, imgHeight = img.size
    
    if imgWidth > imgHeight and (imgWidth / imgHeight) > 1.4: #handle square-ish images
        img = img.rotate(270, expand=True)
        imgWidth, imgHeight = img.size
        scalingFactor = (maxPixelWidth / min(imgWidth, imgHeight))
    elif imgWidth > imgHeight and (imgWidth / imgHeight) <= 1.4:
        scalingFactor = (maxPixelWidth / max(imgWidth, imgHeight))
    else:
        scalingFactor = (maxPixelWidth / min(imgWidth, imgHeight))
    resizedImg = img.resize((int(scalingFactor * imgWidth), int(scalingFactor * imgHeight)))
    p.text('\n' + comic.getAsciiTitle().decode('utf-8'))
    p.text('\n' + comic.link + '\n\n')
    p.image(resizedImg)
    p.text('\n')
    for line in comicAltText:
        p.text('\n' + line)
    p.cut()
    nComicsPrinted = nComicsPrinted + 1
