# -*- coding: utf-8 -*-
import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_PROJ = _os.path.dirname(_HERE)
"""Trich 2712 tu Oxford CHUA co trong web: word, POS, nghia VN (tu PDF),
   giu thu tu alphabet. Xuat words_ox.txt (de tra IPA) + ox_meta.json (POS+vn)."""
import json, io, re

BASE = _HERE + _os.sep
ox = json.load(io.open(BASE + "ox3000_raw.json", encoding="utf-8"))
base = io.open(_PROJ + r"\data-vocab.js", encoding="utf-8").read()
plus = io.open(_PROJ + r"\data-vocab-plus.js", encoding="utf-8").read()
have = set(m.lower() for m in re.findall(r'\{t:"([^"]+)"', base + plus))

def cleanword(w):
    # bo phan ngoac "(bike)", "(abbr Apr)"; giu tu chinh
    return re.sub(r"\s*\(.*?\)", "", w).strip().strip(",").strip()

# map POS PDF -> ma dung trong web (lay token dau)
POSMAP = {
    "v": "v", "n": "n", "adj": "adj", "adv": "adv", "prep": "prep",
    "det": "det", "pron": "pron", "conj": "conj", "exclam": "exclam",
    "number": "num", "modal v": "modalv", "auxiliary v": "v",
    "art": "art", "indefinite article": "art", "definite article": "art",
    "abbr": "abbr", "infinitive marker": "part", "exclamation": "exclam",
}
def mappos(t):
    if not t: return ""
    first = t.split(",")[0].strip().lower()
    return POSMAP.get(first, "")

seen = set()
meta = {}   # word -> {p, vn}
words = []  # giu thu tu alphabet
for o in ox:
    w = cleanword(o["w"])
    wl = w.lower()
    if not w or wl in have or wl in seen: continue
    if not re.match(r"^[a-zA-Z][a-zA-Z '\-]*$", w): continue   # bo entry la
    seen.add(wl)
    meta[w] = {"p": mappos(o.get("t", "")), "vn": (o.get("vn") or "").strip()}
    words.append(w)

io.open(BASE + "words_ox.txt", "w", encoding="utf-8").write("\n".join(words))
json.dump(meta, io.open(BASE + "ox_meta.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print("Tu moi can nhap:", len(words))
print("Co POS:", sum(1 for w in words if meta[w]["p"]), "| co nghia:", sum(1 for w in words if meta[w]["vn"]))
from collections import Counter
print("Phan bo POS:", dict(Counter(meta[w]["p"] for w in words).most_common()))
print("Mau:", ", ".join(words[:12]))
