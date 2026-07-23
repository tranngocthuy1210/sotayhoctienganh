# -*- coding: utf-8 -*-
import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_PROJ = _os.path.dirname(_HERE)
"""Dung lai data-vocab-oxford.js: nhom theo CHU DE (ox_topics.py) thay vi A-Z.

   Doc thang tu file .js hien co nen GIU NGUYEN t/ipa/p/vn da ra soat,
   khong dung lai tu ox_meta/ox_ipa (tranh mat cac sua tay truoc do).
   Trong moi chu de, tu duoc xep A-Z.

   Bao loi:
     - tu trong file NHUNG chua gan chu de   -> phai gan them
     - tu da gan NHUNG khong co trong file   -> go bo / sua chinh ta
     - ma chu de la (khong co trong TOPICS)  -> sua
"""
import io, re, sys
from ox_topics import TOPICS, MAP

SRC = _PROJ + r"\data-vocab-oxford.js"
OUT = SRC

src = io.open(SRC, encoding="utf-8").read()

# Moi tu la mot object {t:"..",ipa:"..",p:"..",vn:".."} — ipa/p/vn co the vang
ROW = re.compile(
    r'\{t:"((?:[^"\\]|\\.)*)"'
    r'(?:,ipa:"((?:[^"\\]|\\.)*)")?'
    r'(?:,p:"([^"]*)")?'
    r'(?:,vn:"((?:[^"\\]|\\.)*)")?\}'
)
rows = ROW.findall(src)
if not rows:
    print("KHONG boc duoc tu nao — kiem lai regex/dinh dang file.")
    sys.exit(1)

order = [c for c, _t, _i, _cl in TOPICS]
titles = {c: (t, i, cl) for c, t, i, cl in TOPICS}

seen, dup = set(), []
buckets = {c: [] for c in order}
unassigned, badcode = [], []

for t, ipa, p, vn in rows:
    if t in seen:
        dup.append(t); continue
    seen.add(t)
    code = MAP.get(t)
    if code is None:
        unassigned.append(t); continue
    if code not in buckets:
        badcode.append((t, code)); continue
    buckets[code].append({"t": t, "ipa": ipa, "p": p, "vn": vn})

ghost = sorted(w for w in MAP if w not in seen)

print("Tong tu trong file :", len(rows))
print("Tu khac nhau       :", len(seen))
if dup:        print("!! TU TRUNG (%d):" % len(dup), dup[:20])
if badcode:    print("!! MA CHU DE LA (%d):" % len(badcode), badcode[:20])
if ghost:      print("!! GAN NHUNG KHONG CO TRONG FILE (%d):" % len(ghost), ghost[:40])
if unassigned:
    print("!! CHUA GAN CHU DE (%d):" % len(unassigned))
    for i in range(0, min(len(unassigned), 400), 20):
        print("   " + " ".join(unassigned[i:i + 20]))

if unassigned or badcode or ghost or dup:
    print("\n==> CHUA GHI FILE. Sua ox_topics.py roi chay lai.")
    sys.exit(1)

def esc(s):
    return str(s).replace("\\", "\\\\").replace('"', '\\"')

lines = [
    "/* KHO OXFORD 3000 THEO CHU DE (tra cuu) — tu Oxford 3000, IPA giong MY tu",
    "   Oxford Learner's Dictionaries (chuan hoa əʊ->oʊ). Nghia + loai tu tu ban PDF Oxford 3000.",
    "   Chia theo chu de de hoc, khong con A-Z; muon tra 1 tu thi dung o TIM KIEM tren dau tab.",
    "   Cac tu nay CHUA co cau vi du (bo sung dan). Cung dinh dang: t/ipa/p/vn. */",
    "window.VOCAB_OXFORD=[",
]
for c in order:
    ws = sorted(buckets[c], key=lambda x: x["t"].lower())
    if not ws:
        print("!! Chu de rong:", c); continue
    title, icon, col = titles[c]
    lines.append(' {id:"ox-%s",title:"%s",icon:"%s",c:"%s",words:[' % (c, esc(title), icon, col))
    for x in ws:
        parts = ['t:"%s"' % esc(x["t"])]
        if x["ipa"]: parts.append('ipa:"%s"' % esc(x["ipa"]))
        if x["p"]:   parts.append('p:"%s"' % esc(x["p"]))
        if x["vn"]:  parts.append('vn:"%s"' % esc(x["vn"]))
        lines.append("  {" + ",".join(parts) + "},")
    lines.append(" ]},")
lines.append("];")

io.open(OUT, "w", encoding="utf-8").write("\n".join(lines) + "\n")

print("\nDa ghi:", OUT)
print("So chu de:", sum(1 for c in order if buckets[c]))
for c in order:
    # console Windows la cp1252 -> in tieu de dang ASCII cho khoi vo
    safe = titles[c][0].encode("ascii", "replace").decode("ascii")
    print("  %-8s %4d  %s" % (c, len(buckets[c]), safe))
