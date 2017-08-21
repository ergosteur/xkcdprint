#!/usr/bin/python
# for testing code without printer connected
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
    if opt == '-h':
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