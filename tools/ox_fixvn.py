# -*- coding: utf-8 -*-
import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_PROJ = _os.path.dirname(_HERE)
"""Sua nghia tieng Viet SAI/THIEU trong data-vocab-oxford.js.

   Ban PDF Oxford 3000 cho nhieu nghia CO hoac nghia phu, sai han voi cach dung
   hang ngay (staff = "gay", receipt = "cong thuc; don thuoc", adapt = "lap vao").
   Dot nay chi sua nhung tu thuoc viec hang ngay cua nguoi dung (F&B / ban hang).
   Con lai ca kho van CAN RA SOAT — xem HANDOFF muc "Uu tien cao" so 2.

   Chay: python ox_fixvn.py
"""
import io, re, sys

SRC = _PROJ + r"\data-vocab-oxford.js"

# tu -> nghia moi (nghia dung nhieu nhat dat TRUOC)
FIX = {
    "adapt":    "thích nghi, điều chỉnh cho phù hợp",
    "staff":    "nhân viên, đội ngũ nhân sự",
    "receipt":  "hoá đơn, biên lai; sự nhận hàng",
    "order":    "đơn hàng, gọi món; ra lệnh; thứ tự",
    "branch":   "chi nhánh, điểm bán; nhánh cây",
    "deal":     "thoả thuận, hợp đồng mua bán; deal with = giải quyết",
    "quote":    "báo giá; trích dẫn",
    "stock":    "hàng tồn kho, hàng dự trữ; cổ phiếu",
    "shift":    "ca làm việc; chuyển, dời",
    "outlet":   "cửa hàng, điểm bán; lối thoát",
    "charge":   "tính tiền, thu phí; phụ trách",
    "bill":     "hoá đơn, giấy tính tiền",
    "serve":    "phục vụ, dọn món",
    "book":     "đặt chỗ, đặt bàn; quyển sách",
    "menu":     "thực đơn, menu",
}

src = io.open(SRC, encoding="utf-8").read()

def esc(s):
    return s.replace("\\", "\\\\").replace('"', '\\"')

done, missing, same = [], [], []
for w, vn in FIX.items():
    # bat dung ban ghi cua TU DO: {t:"w",...,vn:"..."}
    pat = re.compile(r'(\{t:"' + re.escape(w) + r'"(?:,[a-z0-9]+:"(?:[^"\\]|\\.)*")*?,vn:")((?:[^"\\]|\\.)*)(")')
    m = pat.search(src)
    if not m:
        missing.append(w); continue
    if m.group(2) == esc(vn):
        same.append(w); continue
    src = src[:m.start()] + m.group(1) + esc(vn) + m.group(3) + src[m.end():]
    done.append((w, m.group(2), vn))

io.open(SRC, "w", encoding="utf-8").write(src)

print("Da sua:", len(done))
for w, old, new in done:
    print("  %-9s %s  ->  %s" % (w,
          old.encode("ascii", "replace").decode("ascii"),
          new.encode("ascii", "replace").decode("ascii")))
if same:    print("Da dung san, bo qua:", same)
if missing: print("Khong co trong kho Oxford (bo qua):", missing)
