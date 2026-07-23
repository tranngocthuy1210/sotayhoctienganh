# -*- coding: utf-8 -*-
import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_PROJ = _os.path.dirname(_HERE)
"""Loc gat: chi giu cau doi thuong trung tinh, chan tu nhay cam.
   Nguon audio giay phep mo cua Tatoeba lech ve meme/chinh tri/ton giao,
   nen phai chan manh + uu tien cau dung tu thong dung."""
import json, io, re

BASE = _HERE + _os.sep
cand = json.load(io.open(BASE + "tatoeba_cand.json", encoding="utf-8"))

# Chan tu: chinh tri / ton giao / quoc gia-sac toc / bao luc / tinh duc / tuc / meme
BLOCK = set("""
god allah muslim muslims islam islamic christian christians christ jesus jew jews jewish
buddhist hindu church mosque temple pray prayer religion religious devout holy bible quran
gay lesbian trans queer sex sexual penis vagina ass asshole shit fuck damn hell bitch
drunk drug drugs cocaine weed alcohol kill killed kill killing murder gun guns shoot shot
war coup army soldier bomb terrorist attack blood dead death die dies dying died corpse
president trump biden putin obama communist nazi hitler racist slave slaves
alien aliens extraterrestrial ufo baddies anakin sand vader
iran iraq israel palestine russia ukraine china chinese america american africa
albanian albanians algiers baghdad bamako mali syria afghanistan
naked penis breast boobs whore slut virgin pregnant abortion
stupid idiot fool dumb ugly hate hatred disgusting
""".split())

# Tu thong dung -> uu tien cau chua nhieu tu nay (doi thuong, an toan)
COMMON = set("""
i you he she we they it the a an this that my your our is are was were be been am
have has had do does did will would can could go went come came get got make made
take took see saw know knew think want need like love work working home house room
today tomorrow yesterday morning night time day week month year now later soon
water food eat ate drink coffee tea book read write speak talk say said tell told
buy bought sell sold money price shop store market street city bus car train walk
friend family mother father child children people man woman name good bad big small
new old happy help please thank sorry yes no not very much many some all here there
school student teacher learn english question answer open close start stop wait
""".split())

def toks(s): return re.sub(r"[^a-z ]", " ", s.lower()).split()

good = []
for c in cand:
    ws = toks(c["t"])
    if any(w in BLOCK for w in ws): continue
    if len(ws) < 4: continue
    common_ratio = sum(1 for w in ws if w in COMMON) / len(ws)
    if common_ratio < 0.55: continue   # phan lon la tu thong dung -> cau doi thuong an toan
    c["cr"] = round(common_ratio, 2)
    good.append(c)

good.sort(key=lambda x: (-x["cr"], len(x["t"])))
print("Sau loc gat:", len(good), "/", len(cand))
print("\n--- 60 cau tot nhat ---")
for c in good[:60]:
    print("  %s" % c["t"])

json.dump(good, io.open(BASE + "tatoeba_good.json", "w", encoding="utf-8"), ensure_ascii=False)
print("\nDa ghi tatoeba_good.json:", len(good))
