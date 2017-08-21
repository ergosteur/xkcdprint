# xkcdprint
print xkcd comics using Epson thermal printer

Usage: xkcdprint.py [-n <number of comics to print>] [-r | --random] [-i <comicid>]
Defaults to printing latest comic.

Work in progress.

Requires the following python modules:

  * python-escpos
  * xkcd

If on macOS, you must install libusb as a PyUSB backend. See https://github.com/pklaus/brother_ql/issues/3
