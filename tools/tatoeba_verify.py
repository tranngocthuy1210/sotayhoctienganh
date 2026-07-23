# -*- coding: utf-8 -*-
import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_PROJ = _os.path.dirname(_HERE)
"""Xac minh URL audio that su phat duoc, chot ~120 cau, xuat file JS."""
import json, io, re, time, sys
import requests

BASE = _HERE + _os.sep
OUT = _PROJ + r"\data-dictation-tatoeba.js"
good = json.load(io.open(BASE + "tatoeba_good.json", encoding="utf-8"))
TARGET = 120
HDR = {"User-Agent": "Mozilla/5.0"}

def audio_ok(sid):
    url = "https://audio.tatoeba.org/sentences/eng/%s.mp3" % sid
    try:
        r = requests.head(url, headers=HDR, timeout=15, allow_redirects=True)
        return r.status_code == 200 and "audio" in r.headers.get("Content-Type", "")
    except Exception:
        return False

kept, checked = [], 0
for c in good:
    if len(kept) >= TARGET: break
    checked += 1
    if audio_ok(c["id"]):
        kept.append(c)
    time.sleep(0.15)
    if checked % 25 == 0:
        print("  ...da kiem %d, giu %d" % (checked, len(kept)), flush=True)

print("XONG. Kiem %d cau, audio phat duoc %d." % (checked, len(kept)))

# Xuat file JS
def esc(s): return s.replace("\\", "\\\\").replace('"', '\\"')
lines = []
lines.append("/* Cau chep chinh ta co GIONG NGUOI THAT tu du an Tatoeba (tatoeba.org).")
lines.append("   Chi lay audio giay phep MO: CC BY 4.0 va CC0 1.0. Da xac minh tung URL phat duoc.")
lines.append("   Moi cau ghi cong nguoi thu (by) + ma cau (id) de dan link ghi cong theo CC-BY.")
lines.append("   Audio phat truc tiep tu audio.tatoeba.org (hotlink), loi thi tu lui ve giong may. */")
lines.append("window.DICT_TATOEBA=[")
for c in kept:
    lines.append(' {id:"%s",t:"%s",by:"%s",lic:"%s"},' % (
        c["id"], esc(c["t"]), esc(c["by"]), esc(c["lic"])))
lines.append("];")
io.open(OUT, "w", encoding="utf-8").write("\n".join(lines) + "\n")
print("Da ghi:", OUT)

# thong ke license
from collections import Counter
print("Giay phep:", dict(Counter(c["lic"] for c in kept)))
