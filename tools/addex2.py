# -*- coding: utf-8 -*-
import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_PROJ = _os.path.dirname(_HERE)
"""Chen truong ex2 vao sau ex trong data-vocab-plus.js. Bao cao tu thieu/thua."""
import re, io, shutil, sys
from ex2_a import EX2 as A
from ex2_b import EX2 as B

SRC = _PROJ + r"\data-vocab-plus.js"
EX2 = {}
EX2.update(A); EX2.update(B)
print("Tong ex2 soan duoc:", len(EX2))

shutil.copy(SRC, SRC + ".bak")
s = io.open(SRC, encoding="utf-8").read()

words = re.findall(r'\{t:"([^"]*)"', s)
missing = [w for w in words if w not in EX2]
extra = [w for w in EX2 if w not in words]
already = s.count('ex2:"')

print("Tu trong file      :", len(words))
print("THIEU ex2          :", len(missing), missing)
print("THUA (khong co tu) :", len(extra), extra)
print("Da co ex2 tu truoc :", already)
if missing or extra:
    print("\n=> DUNG LAI, sua danh sach truoc.")
    sys.exit(1)

done = []
def repl(m):
    head, w, mid, ex, tail = m.group(1), m.group(2), m.group(3), m.group(4), m.group(5)
    if 'ex2:"' in m.group(0): return m.group(0)
    e2 = EX2[w].replace('"', "'")
    done.append(w)
    return head + w + mid + ex + '",ex2:"' + e2 + tail

out = re.sub(r'(\{t:")([^"]*)(",ipa:"[^"]*",p:"\w+",vn:"[^"]*",ex:")([^"]*)(")', repl, s)
io.open(SRC, "w", encoding="utf-8").write(out)
print("\nDa chen ex2 cho", len(done), "tu")
print("Kiem lai: so ex2 trong file =", out.count('ex2:"'))
