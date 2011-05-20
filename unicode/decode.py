#!/usr/local/bin/python
#
#  Decode bytes out of 32-126 range to <nn> (decimal)
#
import sys
while 1 :
    lin = sys.stdin.readline()
    if not lin : break
    out = ""
    for c in lin[:-1] :
        n = ord(c)
        if   n == 0  : out += '.'
        elif n > 126 : out += "-%x-" % n
        else         : out += c
    print out

