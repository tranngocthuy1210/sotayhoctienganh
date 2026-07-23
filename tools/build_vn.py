# -*- coding: utf-8 -*-
import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_PROJ = _os.path.dirname(_HERE)
"""Dung data-sentence-vn.js tu tat ca batch ban dich. Kiem phu du cau."""
import io, re
from vn_core import VN as V0
from vn_plus1 import VN as V1
from vn_plus2 import VN as V2
from vn_scr import VN as V3
from vn_tat import VN as V4

BASE = _HERE + _os.sep
OUT = _PROJ + r"\data-sentence-vn.js"

ALL = {}
for d in (V0, V1, V2, V3, V4): ALL.update(d)

# kiem phu tung nguon
def check(name, path):
    sents = [l.strip() for l in io.open(BASE + path, encoding="utf-8") if l.strip()]
    miss = [s for s in sents if s not in ALL]
    print("%-14s %3d cau | THIEU %d" % (name, len(sents), len(miss)))
    for s in miss[:12]: print("     -", s)
    return len(miss)

BASE2 = BASE
tot_miss = 0
tot_miss += check("core", "core_ex.txt")
tot_miss += check("plus", "miss_plus.txt")
tot_miss += check("script", "miss_scr.txt")
tot_miss += check("tatoeba", "tat_kept.txt")

# canh bao value rong / con tieng Anh
empty = [k for k, v in ALL.items() if not v.strip()]
suspicious = [k for k, v in ALL.items()
              if re.search(r"[a-zA-Z]", v)
              and not re.search(r"[àáảãạăâđêôơưèéẻẽẹìíỉĩịòóỏõọùúủũụ]", v.lower())
              and len(v.split()) > 2]
print("Value rong:", len(empty), "| nghi con tieng Anh:", len(suspicious), suspicious[:5])

# xuat JS
def esc(s): return s.replace("\\", "\\\\").replace('"', '\\"')
lines = ["/* Ban dich tieng Viet cho cau chep chinh ta (dich tay, bo sung dan).",
         "   Key = cau tieng Anh y het. Dung trong tab Chep chinh ta. */",
         "window.SENTENCE_VN={"]
for k in sorted(ALL.keys()):
    lines.append('"%s":"%s",' % (esc(k), esc(ALL[k])))
lines.append("};")
io.open(OUT, "w", encoding="utf-8").write("\n".join(lines) + "\n")
print("Da ghi:", OUT, "|", len(ALL), "cau |", "TONG THIEU:", tot_miss)
