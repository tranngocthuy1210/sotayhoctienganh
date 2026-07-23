# -*- coding: utf-8 -*-
import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_PROJ = _os.path.dirname(_HERE)
"""Loc cau Tatoeba co audio giay phep MO (CC BY 4.0 / CC0), ghep voi chu,
   chon cau hop trinh do nguoi mat goc. Xuat JSON tho de kiem truoc."""
import tarfile, bz2, io, json, re

BASE = _HERE + _os.sep
OKLIC = {"CC BY 4.0", "CC0 1.0"}

# 1) sentence_id -> (license, username, attr)
tar = tarfile.open(BASE + "sentences_with_audio.tar.bz2", "r:bz2")
f = tar.extractfile("sentences_with_audio.csv").read().decode("utf-8", "replace")
aud = {}
for l in f.splitlines():
    p = l.split("\t")
    if len(p) < 5: continue
    sid, aid, user, lic, attr = p[0], p[1], p[2], p[3], p[4]
    if lic in OKLIC:
        aud[sid] = (lic, user, attr)
print("Cau co audio giay phep mo:", len(aud))

# 2) ghep chu
txt = {}
with bz2.open(BASE + "eng_sentences.tsv.bz2", "rt", encoding="utf-8") as fh:
    for line in fh:
        p = line.rstrip("\n").split("\t")
        if len(p) < 3: continue
        if p[0] in aud:
            txt[p[0]] = p[2]
print("Ghep duoc chu:", len(txt))

# 3) loc cau hop trinh do
def wc(s): return len(s.split())
def clean(s):
    if not (4 <= wc(s) <= 12): return False          # ngan, de chep
    if not re.match(r"^[A-Z]", s): return False       # bat dau hoa chuan
    if not re.search(r"[.?!]$", s): return False      # ket cau tron
    if re.search(r"[^A-Za-z0-9 ,.?!'\"-]", s): return False  # bo cau co ky tu la / tieng khac
    if sum(c.isupper() for c in s) > 3: return False  # bo cau nhieu ten rieng
    if '"' in s: return False                          # bo cau trich dan long dong
    letters = re.sub(r"[^a-z]", "", s.lower())
    if len(set(letters)) < 5: return False
    return True

cand = []
for sid, s in txt.items():
    if clean(s):
        lic, user, attr = aud[sid]
        cand.append({"id": sid, "t": s, "lic": lic, "by": user})
cand.sort(key=lambda x: (wc(x["t"]), x["t"]))
print("Sau khi loc:", len(cand))
print("\n--- 30 cau mau (ngan nhat) ---")
for c in cand[:30]:
    print("  [%s] %s  (%s)" % (c["id"], c["t"], c["by"]))

json.dump(cand, io.open(BASE + "tatoeba_cand.json", "w", encoding="utf-8"), ensure_ascii=False)
print("\nDa ghi tatoeba_cand.json:", len(cand), "cau")
