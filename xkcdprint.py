#!/usr/bin/python
import escpos
import escpos.printer
import xkcd
import textwrap
from random import randint
from PIL import Image

nComicsToPrint = 1
nComicsPrinted = 0
comicRandom = False
maxPixelWidth = 512

p = escpos.printer.Usb(0x04b8,0x0e15)
nLatestComic = xkcd.getLatestComic().number 

while nComicsPrinted < nComicsToPrint:
    comic = xkcd.getComic(nLatestComic - nComicsPrinted)
    comicImg = comic.download()
    comicAltText = textwrap.wrap(comic.getAsciiAltText(),40)
    img = Image.open(comicImg.encode('utf-8'))
    imgWidth, imgHeight = img.size
    if (imgWidth > imgHeight):
        img = img.rotate(270, expand=True)
        imgWidth, imgHeight = img.size
    scalingFactor = (maxPixelWidth / min(imgWidth, imgHeight))
    resizedImg = img.resize(int(scalingFactor * imgWidth), int(scalingFactor * imgHeight))
    p.block_text(comic.number + comic.getTitle())
    p.text(comic.link)
    p.image(resizedImg)
    p.text('\n')
    for line in comicAltText:
        p.text('\n' + line)
    p.cut()
    nComicsPrinted = nComicsPrinted + 1
