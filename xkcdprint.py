#!/usr/bin/python
import escpos
import escpos.printer
import xkcd
import textwrap
import sys
import getopt
from random import randint
from PIL import Image

usageText = 'xkcdprint.py [-n <number of comics to print>] [-r] [-i <comicid>]\nDefaults to printing latest comic.\n'
nComicsToPrint = 1
nComicsPrinted = 0
comicRandom = False
maxPixelWidth = 512
nStartComic = xkcd.getLatestComic().number

try:
    opts, args = getopt.getopt(sys.argv,"hn:ri:",["help","to-print=","random","comicid="])
except getopt.GetoptError:
    print(usageText)
    sys.exit(2)

for opt, arg in opts:
    if opt == '-h':
        print(usageText)
        sys.exit()
    elif opt in ("-r", "--random"):
        nStartComic = randint(1, xkcd.getLatestComicNum())
    elif opt in ("-i", "--comicid"):
        if 0 <= arg <= xkcd.getLatestComicNum():
            nStartComic = arg
        else:
            sys.exit(1)
    elif opt in ("-n", "--to-print"):
        nComicsToPrint = arg

# Initialize Epson thermal printer using usb-id (here using TM-T20II)
p = escpos.printer.Usb(0x04b8, 0x0e15)

while nComicsPrinted < nComicsToPrint:
    comic = xkcd.getComic(nStartComic - nComicsPrinted)
    comicImg = comic.download()
    comicAltText = textwrap.wrap(comic.getAsciiAltText(),40)
    img = Image.open(comicImg.encode('utf-8'))
    imgWidth, imgHeight = img.size
    if (imgWidth > imgHeight):
        img = img.rotate(270, expand=True)
        imgWidth, imgHeight = img.size
    scalingFactor = (maxPixelWidth / min(imgWidth, imgHeight))
    resizedImg = img.resize((int(scalingFactor * imgWidth), int(scalingFactor * imgHeight)))
    resizedImg.save('resizedImg.png')
    p.text('\n' + comic.getAsciiTitle())
    p.text('\n' + comic.link + '\n\n')
    p.image('resizedImg.png')
    p.text('\n')
    for line in comicAltText:
        p.text('\n' + line)
    p.cut()
    nComicsPrinted = nComicsPrinted + 1
