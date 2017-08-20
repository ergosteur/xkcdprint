#!/usr/bin/python
import escpos
import escpos.printer
import PythonMagick
import xkcd
import textwrap

nComicsToPrint = 2
nComicsPrinted = 0

p = escpos.printer.Usb(0x04b8,0x0e15)
nLatestComic = xkcd.getLatestComic().number 

while nComicsPrinted < nComicsToPrint:
    comic = xkcd.getComic(nLatestComic - nComicsPrinted)
    comicImg = comic.download()
    comicAltText = textwrap.wrap(comic.getAsciiAltText(),40)
    img = PythonMagick.Image(comicImg.encode('utf-8'))
    if (img.size().width() > img.size().height()):
        img.rotate(90)
        img.resize('512x')
    else:
        img.resize('512x')
    img.magick('PNG')
    img.write('outputImage.png')
    p.image('outputImage.png')
    p.text('\n')
    for line in comicAltText:
        p.text('\n' + line)
    p.cut()
    nComicsPrinted = nComicsPrinted + 1
