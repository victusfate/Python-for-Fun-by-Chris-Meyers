#!/usr/bin/env python
#
#  u t f 8 . p y
#
#
"""utf8.py stdin to stdout
convert string to utf-8 from latin alphabet equivalents
convert <german>...</german> to utf-8 standard german
convert <russian>...</russian> to utf-8 standard russian
"""
import sys, re

def main () :
    txt = sys.stdin.read()
    p = max(0,search(txt,"<html"))    # precede <html> tag with
    utf = '<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />'
    txt = txt[:p]+utf+txt[p:]

    for lang in ('unicode','german','russian') :
        ll = len(lang)
        while 1 :
            p = search(txt,"<%s>"%lang)
            q = search(txt,"</%s>"%lang)
            if p < 0 or q <= p : break
            src = txt[p+ll+2:q]
            rpl = encode(src,lang)
            txt = txt[:p]+"<strong>"+rpl+"</strong>"+txt[q+ll+3:]
    print txt,
                
def encode(s, Trans=None) :
    "encode s to utf-8. Trans is a module name or 'unicode'"
    if not Trans : return s
    if Trans == 'unicode' :
        return unichr(eval("0x"+s)).encode('utf-8')
    exec("from %s import trans, maxKeyLen" % Trans)
    u = u''
    ls = len(s)
    rng = range(maxKeyLen,0,-1)
    i = 0
    while i < ls :
        for j in rng :
            seq = s[i:i+j]
            uc = trans.get(seq)
            if uc :
                i += j
                break
        if not uc :
            uc = ord(s[i])
            i += 1
        u += unichr(uc)
    return u.encode('utf-8')

def search (a,b) :
    match = re.search(b,a)
    if not match : return -1
    else         : return match.start()

if __name__ == "__main__" : main()
