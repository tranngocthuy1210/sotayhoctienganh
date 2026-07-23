# -*- coding: utf-8 -*-
import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_PROJ = _os.path.dirname(_HERE)
"""Dung data-topics.js — bang chu de DUNG CHUNG cho ca 3 kho tu.

   Truoc day: 15 nhom "co san vi du" + 26 nhom Oxford = 41 nhom rieng biet.
   Nay gop lam MOT: 26 chu de, moi chu de chua ca tu co vi du lan tu Oxford.
   File .js goc (data-vocab.js / -plus / -oxford) GIU NGUYEN, khong dung toi —
   index.html doc bang nay roi tu xep lai lop nhom khi chay.

   Xuat:
     window.TOPIC_DEF = [{id,title,icon,c}, ...]   thu tu hien thi
     window.TOPIC_OF  = {tu: "ma chu de", ...}     3443 tu

   Bao loi va KHONG ghi file neu con tu chua gan / gan thua / trung.
"""
import io, re, sys
from ox_topics import TOPICS, MAP

SRCS = [_PROJ + r"\data-vocab.js",
        _PROJ + r"\data-vocab-plus.js",
        _PROJ + r"\data-vocab-oxford.js"]
OUT = _PROJ + r"\data-topics.js"

WORD = re.compile(r'\{t:"((?:[^"\\]|\\.)*)"')

words, dup = [], []
seen = set()
for p in SRCS:
    s = io.open(p, encoding="utf-8").read()
    got = WORD.findall(s)
    print("%-26s %4d tu" % (_os.path.basename(p), len(got)))
    for w in got:
        w = w.replace('\\"', '"').replace("\\\\", "\\")
        if w in seen: dup.append(w); continue
        seen.add(w); words.append(w)

codes = set(c for c, _t, _i, _cl in TOPICS)
unassigned = [w for w in words if w not in MAP]
badcode = [(w, MAP[w]) for w in words if w in MAP and MAP[w] not in codes]
ghost = sorted(w for w in MAP if w not in seen)

print("\nTong tu khac nhau:", len(words))
if dup:        print("!! TU TRUNG (%d):" % len(dup), dup[:20])
if badcode:    print("!! MA CHU DE LA (%d):" % len(badcode), badcode[:20])
if ghost:      print("!! GAN NHUNG KHONG CO TRONG KHO (%d):" % len(ghost), ghost[:40])
if unassigned:
    print("!! CHUA GAN CHU DE (%d):" % len(unassigned))
    for i in range(0, min(len(unassigned), 400), 15):
        print("   " + " | ".join(unassigned[i:i + 15]))

if dup or badcode or ghost or unassigned:
    print("\n==> CHUA GHI FILE. Sua ox_topics.py roi chay lai.")
    sys.exit(1)

def esc(s):
    return str(s).replace("\\", "\\\\").replace('"', '\\"')

n = {}
for w in words: n[MAP[w]] = n.get(MAP[w], 0) + 1

lines = [
    "/* BANG CHU DE DUNG CHUNG — sinh boi tools/build_topics.py, DUNG SUA TAY.",
    "   Gop 794 tu co vi du + 2649 tu Oxford thanh 26 chu de chung.",
    "   index.html doc file nay roi xep lai lop nhom khi chay; 3 file du lieu goc",
    "   (data-vocab.js / -plus / -oxford) giu nguyen, van la noi chua t/ipa/p/vn/ex. */",
    "window.TOPIC_DEF=[",
]
for c, t, ic, cl in TOPICS:
    if not n.get(c): print("!! Chu de rong:", c); continue
    lines.append(' {id:"ox-%s",title:"%s",icon:"%s",c:"%s"},' % (c, esc(t), ic, cl))
lines.append("];")
lines.append("window.TOPIC_OF={")
buf = []
for w in sorted(words, key=lambda x: x.lower()):
    buf.append('"%s":"%s"' % (esc(w), MAP[w]))
    if len(buf) == 6:
        lines.append(" " + ",".join(buf) + ","); buf = []
if buf: lines.append(" " + ",".join(buf) + ",")
lines.append("};")

io.open(OUT, "w", encoding="utf-8").write("\n".join(lines) + "\n")

print("\nDa ghi:", OUT)
print("So chu de:", sum(1 for c in codes if n.get(c)))
for c, t, ic, cl in TOPICS:
    safe = t.encode("ascii", "replace").decode("ascii")
    print("  %-8s %4d  %s" % (c, n.get(c, 0), safe))
