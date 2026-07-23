# -*- coding: utf-8 -*-
import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_PROJ = _os.path.dirname(_HERE)
"""Bóc 3000 từ Oxford 3000 từ PDF english4u -> JSON thô.
Cách tách: nối toàn bộ text thành 1 chuỗi rồi dò lần lượt số thứ tự 1..3000
(không phụ thuộc xuống dòng, vì PDF hay gộp dòng)."""
import re, json, io
from pypdf import PdfReader

SRC = r"C:\Users\Thuy.tran\.claude\projects\D--AI-Challenge-so-tay-web\bdc786b3-9b44-4cc8-82fa-cb4a187537b0\tool-results\webfetch-1784619113553-uip8np.pdf"
BASE = _HERE

r = PdfReader(SRC)
chunks = []
for pg in r.pages:
    t = pg.extract_text() or ""
    for ln in t.split("\n"):
        s = ln.replace("\xa0", " ").strip()
        if not s or s.startswith("`"): continue
        if "Oxford 3000" in s or "TỪ VỰNG TIẾNG ANH" in s: continue
        if "effortlessenglishclub" in s or s.startswith("No. Word"): continue
        if re.match(r"^Trang \d+$", s): continue
        chunks.append(s)
full = re.sub(r"\s+", " ", " ".join(chunks)).strip()

# Dò số thứ tự tăng dần
pos, spans = 0, []
for n in range(1, 3401):
    m = re.compile(r"(?<![\w])" + str(n) + r"(?![\w])").search(full, pos)
    if not m:
        spans.append((n, None, None)); continue
    spans.append((n, m.end(), None)); pos = m.end()
recs = []
for i, (n, st, _) in enumerate(spans):
    if st is None: continue
    en = None
    for j in range(i + 1, len(spans)):
        if spans[j][1] is not None:
            en = spans[j][1] - len(str(spans[j][0])); break
    body = full[st:(en if en else len(full))].strip()
    recs.append({"no": n, "raw": body})

print("Bat duoc:", len(recs), "/ 3000")

TYPES = ("modal v","auxiliary v","indefinite article","definite article","infinitive marker",
         "number","det","pron","prep","conj","exclam","adv","adj","abbr","art","n","v")
T = "|".join(TYPES)
TYPE_RE = re.compile(r"^((?:%s)(?:\s*,\s*(?:%s))*)(?![a-z])\s*(.*)$" % (T, T))

VIET = "àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ"
def has_viet(s): return any(ch in VIET for ch in s.lower())
IPA_ONLY = set("æɑɐɒəɚɛɜɝɪɨʊʌʒʃθðŋɳɔːˈˌ´ʤʧʔ")
def looks_ipa(tok):
    t = tok.strip().strip(",.;")
    if not t or has_viet(t): return False
    if any(ch in IPA_ONLY for ch in t): return True
    # token toàn chữ latin thường + dấu : ' - cũng có thể là IPA đơn giản (vd "luk", "æd")
    return bool(re.match(r"^[a-z:'´,\-\(\)/]+$", t))

out = []
for rc in recs:
    raw = rc["raw"]
    word, typ, rest = None, "", raw
    toks = raw.split(" ")
    for k in range(1, min(5, len(toks)) + 1):
        m = TYPE_RE.match(" ".join(toks[k:]))
        if m:
            word, typ, rest = " ".join(toks[:k]), m.group(1), m.group(2); break
    if word is None:
        word, typ, rest = toks[0], "", " ".join(toks[1:])
    rtoks = rest.split(" ")
    i = 0
    while i < len(rtoks) and i < 5 and looks_ipa(rtoks[i]) and not has_viet(rtoks[i]):
        i += 1
    ipa = " ".join(rtoks[:i]).strip() if i else ""
    vn = " ".join(rtoks[i:]).strip()
    out.append({"no": rc["no"], "w": word.strip().strip(",").strip(), "t": typ, "ipa": ipa, "vn": vn})

json.dump(out, io.open(BASE + r"\ox3000_raw.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)

bad_w = [o for o in out if not re.match(r"^[a-zA-Z][a-zA-Z '\-,\.]*$", o["w"] or "")]
print("Thieu IPA:", sum(1 for o in out if not o["ipa"]))
print("Thieu nghia:", sum(1 for o in out if not o["vn"]))
print("Tu nghi ngo (parse loi):", len(bad_w))
for o in bad_w[:15]: print("   ?", o["no"], "|", repr(o["w"]), "|", o["t"], "|", o["vn"][:40])
print("\n--- mau rai rac ---")
for k in (0, 500, 1200, 1900, 2500, 2999):
    if k < len(out):
        o = out[k]; print(o["no"], "|", o["w"], "|", o["t"], "|", o["ipa"], "|", o["vn"][:45])
