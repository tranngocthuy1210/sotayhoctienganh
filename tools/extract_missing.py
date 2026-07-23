# -*- coding: utf-8 -*-
import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_PROJ = _os.path.dirname(_HERE)
"""Trich moi cau trong kho chep chinh ta CHUA co ban dich VN."""
import re, io
from html.parser import HTMLParser
from vn_core import VN as HAVE0

have = dict(HAVE0)
D = _PROJ + "/"

def wc(s): return len(s.strip().split())

# 1) plus vocab: ex + ex2
plus = io.open(D + "data-vocab-plus.js", encoding="utf-8").read()
plus_sents = []
for m in re.finditer(r'ex2?:"((?:[^"\\]|\\.)*)"', plus):
    t = m.group(1)
    if 4 <= wc(t) <= 16: plus_sents.append(t)

# 2) tatoeba
tat = io.open(D + "data-dictation-tatoeba.js", encoding="utf-8").read()
tat_sents = [m.group(1) for m in re.finditer(r't:"((?:[^"\\]|\\.)*)"', tat)]

# 3) script lines tu index.html
html = io.open(D + "index.html", encoding="utf-8").read()
class P(HTMLParser):
    def __init__(s):
        super().__init__(convert_charrefs=True); s.d=0; s.buf=""; s.out=[]
    def handle_starttag(s, tag, attrs):
        a=dict(attrs); cls=a.get("class","")
        if s.d: s.d+=1; return
        if "sl" in cls.split() or "txt" in cls.split(): s.d=1; s.buf=""
    def handle_endtag(s, tag):
        if s.d:
            s.d-=1
            if s.d==0:
                t=re.sub(r"\s+"," ",s.buf).strip()
                if t: s.out.append(t)
    def handle_data(s, d):
        if s.d: s.buf+=d
p=P(); p.feed(html)
scr_sents=[t for t in p.out if 4<=wc(t)<=16 and re.search(r"[a-zA-Z]",t)]

def dump(name, sents):
    uniq=[]
    seen=set()
    for t in sents:
        if t in seen: continue
        seen.add(t); uniq.append(t)
    missing=[t for t in uniq if t not in have]
    io.open(name, "w", encoding="utf-8").write("\n".join(missing))
    print("%-10s tong duy nhat %3d | chua dich %3d -> %s" % (name, len(uniq), len(missing), name))
    return missing

dump("miss_plus.txt", plus_sents)
dump("miss_tat.txt", tat_sents)
dump("miss_scr.txt", scr_sents)
