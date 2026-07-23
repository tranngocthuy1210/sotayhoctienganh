# -*- coding: utf-8 -*-
import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_PROJ = _os.path.dirname(_HERE)
"""Dung data-vocab-oxford.js: nhom A-Z, moi tu {t,ipa,p,vn}.
   IPA tu Oxford (chuan hoa əʊ->oʊ, chan ky hieu giong Anh sot lai).
   Chay SAU khi oxipa.py xong (co ox_ipa.json)."""
import json, io, os, re

BASE = _HERE + _os.sep
OUT = _PROJ + r"\data-vocab-oxford.js"

words = [l.strip() for l in io.open(BASE + "words_ox.txt", encoding="utf-8") if l.strip()]
meta = json.load(io.open(BASE + "ox_meta.json", encoding="utf-8"))
ipa = json.load(io.open(BASE + "ox_ipa.json", encoding="utf-8"))

BRIT_ONLY = ["ɒ", "ɪə", "eə", "ʊə", "əʊ", "ɛə"]
def fix_ipa(s):
    if not s: return ""
    s = s.replace("əʊ", "oʊ")
    # Cac chuoi HOP LE trong giong My nhung chua chuoi con ɪə/ʊə (fire, hour, player,
    # mayor, poem, employer...) -> bo truoc khi kiem tra, tranh chan nham
    t = s
    for combo in ("aɪə", "aʊə", "eɪə", "oʊə", "ɔɪə"):
        t = t.replace(combo, "")
    if any(b in t for b in BRIT_ONLY): return "__BRIT__"
    return s

# Entry rac tu loi boc PDF (tu bi dinh nhan loai tu / ghi chu)
ARTIFACT = {
    "any detpron", "can modal", "could modal", "might modal", "do vauxiliary",
    "have vauxiliary", "seem linking", "used to modal", "have to modal",
    "number no", "per cent usn", "TV television", "OK exclamation", "no exclamation",
    "hello exclamation", "goodbye exclamation", "please exclamation",
    "thank you exclamation", "thanks exclamation", "swollen swell", "suf",
}

def esc(s): return str(s).replace("\\", "\\\\").replace('"', '\\"')

groups = {}
noipa, briterr = [], []
for w in words:
    if w in ARTIFACT: continue
    letter = w[0].upper()
    if not letter.isalpha(): letter = "#"
    ip = fix_ipa(ipa.get(w, ""))
    if ip == "__BRIT__": briterr.append(w); ip = ""
    if not ip: noipa.append(w)
    m = meta.get(w, {})
    groups.setdefault(letter, []).append({
        "t": w, "ipa": ip, "p": m.get("p", ""), "vn": m.get("vn", "")
    })

letters = sorted(groups.keys())
lines = []
lines.append("/* KHO OXFORD 3000 A-Z (tra cuu) — tu Oxford 3000, IPA giong MY tu")
lines.append("   Oxford Learner's Dictionaries (chuan hoa əʊ->oʊ). Nghia + loai tu tu ban PDF Oxford 3000.")
lines.append("   Cac tu nay CHUA co cau vi du (bo sung dan). Cung dinh dang: t/ipa/p/vn. */")
lines.append("window.VOCAB_OXFORD=[")
for L in letters:
    ws = groups[L]
    lines.append(' {id:"ox-%s",title:"Oxford 3000 · %s",icon:"i-book",c:"tonghop",words:[' % (L.lower(), L))
    for x in ws:
        parts = ['t:"%s"' % esc(x["t"])]
        if x["ipa"]: parts.append('ipa:"%s"' % esc(x["ipa"]))
        if x["p"]:   parts.append('p:"%s"' % esc(x["p"]))
        if x["vn"]:  parts.append('vn:"%s"' % esc(x["vn"]))
        lines.append("  {" + ",".join(parts) + "},")
    lines.append(" ]},")
lines.append("];")
io.open(OUT, "w", encoding="utf-8").write("\n".join(lines) + "\n")

total = sum(len(v) for v in groups.values())
print("Da ghi:", OUT)
print("Tong tu:", total, "| nhom A-Z:", len(letters))
print("Co IPA:", total - len(noipa), "| KHONG co IPA:", len(noipa))
print("IPA con ky hieu giong Anh (da bo, can dò lai):", len(briterr), briterr[:8])
print("Vai tu khong IPA:", noipa[:12])
