#!/usr/bin/env python
#
#  t a b l e . p y
#
#  Build html table to display full byte chars
#
html = """
<html><body>
<font size="24">
<table border="4" cellpadding="3">
%s
</table>
</body></html>
"""

t = ""
for r in range(0,256,16) :
    t = t+"<tr>"
    for c in range(r,r+16) :
        t = t+"<td> %02x %s </td>" % (c,chr(c))
    t = t+"</tr>\n"

print html % t

