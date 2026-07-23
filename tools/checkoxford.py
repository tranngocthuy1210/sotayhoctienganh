# -*- coding: utf-8 -*-
import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_PROJ = _os.path.dirname(_HERE)
"""Kiem data-vocab-oxford.js sau khi chia lai theo chu de:
   cu phap JS, so tu, tu trung, id chu de trung, so tu doi chieu ban .bak."""
import io, re, sys, json

SRC = _PROJ + r"\data-vocab-oxford.js"
BAK = SRC + ".bak"
ok = True

src = io.open(SRC, encoding="utf-8").read()

import esprima
try:
    esprima.parseScript(src)
    print("Cu phap JS: OK")
except Exception as e:
    ok = False
    print("Cu phap JS LOI:", e)

ids = re.findall(r'\{id:"([^"]+)"', src)
print("So chu de:", len(ids))
if len(set(ids)) != len(ids):
    ok = False
    print("!! ID CHU DE TRUNG:", [i for i in ids if ids.count(i) > 1])

words = re.findall(r'\{t:"((?:[^"\\]|\\.)*)"', src)
print("Tong tu:", len(words), "| khac nhau:", len(set(words)))
if len(set(words)) != len(words):
    ok = False
    seen, dup = set(), []
    for w in words:
        if w in seen: dup.append(w)
        seen.add(w)
    print("!! TU TRUNG:", dup[:20])

# doi chieu ban truoc khi chia lai: phai GIU DU tung tu, tung IPA, tung nghia
if _os.path.exists(BAK):
    bak = io.open(BAK, encoding="utf-8").read()
    ROW = re.compile(r'\{t:"((?:[^"\\]|\\.)*)"'
                     r'(?:,ipa:"((?:[^"\\]|\\.)*)")?'
                     r'(?:,p:"([^"]*)")?'
                     r'(?:,vn:"((?:[^"\\]|\\.)*)")?\}')
    old = {r[0]: r[1:] for r in ROW.findall(bak)}
    new = {r[0]: r[1:] for r in ROW.findall(SRC and src)}
    print("Ban .bak:", len(old), "tu | ban moi:", len(new), "tu")
    miss = sorted(set(old) - set(new))
    extra = sorted(set(new) - set(old))
    changed = [w for w in old if w in new and old[w] != new[w]]
    if miss:    ok = False; print("!! MAT TU (%d):" % len(miss), miss[:20])
    if extra:   ok = False; print("!! TU LA (%d):" % len(extra), extra[:20])
    if changed: ok = False; print("!! DOI IPA/NGHIA (%d):" % len(changed), changed[:20])
    if not (miss or extra or changed):
        print("Doi chieu .bak: GIU NGUYEN du lieu tung tu (chi doi cach nhom)")
else:
    print("(khong co file .bak de doi chieu)")

print("\n==> " + ("TAT CA OK" if ok else "CO LOI"))
sys.exit(0 if ok else 1)
