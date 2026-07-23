# -*- coding: utf-8 -*-
import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_PROJ = _os.path.dirname(_HERE)
"""Kiểm tra data-vocab-plus.js: cú pháp JS, trùng từ, thiếu trường,
   và đối chiếu với danh sách Oxford 3000 đã bóc từ PDF."""
import re, io, json, esprima, sys

PLUS = _PROJ + r"\data-vocab-plus.js"
BASE = _PROJ + r"\data-vocab.js"
OX   = r"ox3000_raw.json"

ok = True
src = io.open(PLUS, encoding="utf-8").read()
try:
    esprima.parseScript(src); print("Cu phap JS: OK")
except Exception as e:
    ok = False; print("Cu phap JS LOI:", e)

groups = re.findall(r'\{id:"(.*?)",title:"(.*?)",icon:"(.*?)",c:"(.*?)",words:\[', src)
print("So chu de moi:", len(groups))

entries = re.findall(r'\{t:"((?:[^"\\]|\\.)*)"(.*?)\}(?=,\n|\n\]|\s*\n\])', src)
words = re.findall(r'\{t:"((?:[^"\\]|\\.)*)",ipa:"((?:[^"\\]|\\.)*)",p:"(\w+)",vn:"((?:[^"\\]|\\.)*)",ex:"((?:[^"\\]|\\.)*)"', src)
print("So tu bat duoc (du 5 truong t/ipa/p/vn/ex):", len(words))

# tong so ban ghi {t:"..."} de doi chieu
alt = re.findall(r'\{t:"', src)
print("Tong ban ghi {t:...}:", len(alt))
if len(words) != len(alt):
    ok = False
    print("  !! Co ban ghi THIEU truong bat buoc (ipa/p/vn/ex)")

# trung nhau trong file moi
seen, dup = set(), []
for w in words:
    k = w[0].lower()
    if k in seen: dup.append(w[0])
    seen.add(k)
print("Trung trong file moi:", len(dup), dup[:10])
if dup: ok = False

# trung voi bo 600 cu
base = io.open(BASE, encoding="utf-8").read()
old = set(m.lower() for m in re.findall(r'\{t:"((?:[^"\\]|\\.)*)"', base))
clash = sorted(k for k in seen if k in old)
print("Trung voi bo 600 cu:", len(clash), clash[:10])
if clash: ok = False

# IPA: phai co dau trong am voi tu >=2 am tiet (heuristic: do dai >4)
noStress = [w[0] for w in words if len(w[1]) > 4 and "ˈ" not in w[1] and "ˌ" not in w[1]]
print("IPA dai ma thieu dau trong am:", len(noStress), noStress[:12])

# ky tu IPA la
BAD = set("´ʤʧɳ:'")
badIpa = [(w[0], w[1]) for w in words if any(c in BAD for c in w[1])]
print("IPA dung ky hieu cu/sai:", len(badIpa), badIpa[:8])
if badIpa: ok = False

# vi du phai chua tu do (hoac bien the)
noEx = []
for t, ipa, p, vn, ex in words:
    stem = t.lower().split()[0][:4]
    if stem and stem not in ex.lower():
        noEx.append((t, ex))
print("Vi du KHONG chua tu (can xem lai):", len(noEx))
for t, ex in noEx[:12]: print("   -", t, "->", ex)


# ex2: phai co du, phai KHAC ex
e2 = re.findall(r'ex:"((?:[^"\\]|\\.)*)",ex2:"((?:[^"\\]|\\.)*)"', src)
print("So tu co ex2:", len(e2))
if len(e2) != len(alt):
    ok = False; print("  !! Co tu THIEU ex2:", len(alt)-len(e2))
dupex = [a for a,b in e2 if a.strip().lower()==b.strip().lower()]
print("ex2 TRUNG y het ex:", len(dupex), dupex[:5])
if dupex: ok = False

# doi chieu Oxford
ox = json.load(io.open(OX, encoding="utf-8"))
oxset = set()
for o in ox:
    w = re.sub(r"\s*\(.*?\)", "", o["w"]).strip().strip(",").lower()
    if w: oxset.add(w)
notOx = sorted(k for k in seen if k not in oxset)
print("\nTu KHONG co trong danh sach Oxford:", len(notOx))
print("  ", ", ".join(notOx[:20]))

print("\n==> " + ("OK" if ok else "CO VAN DE"))
sys.exit(0 if ok else 1)
