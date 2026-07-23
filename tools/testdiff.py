# -*- coding: utf-8 -*-
"""Port nguyen thuat toan cham chinh ta tu index.html sang Python de kiem logic."""
import re, sys

def norm(s):
    s = s.lower()
    s = re.sub(r"['’‘]", "", s)
    s = re.sub(r"[^a-z0-9 ]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()

def toks(s):
    n = norm(s)
    return n.split(" ") if n else []

def lev(a, b):
    if a == b: return 0
    m, n = len(a), len(b)
    prev = list(range(n + 1))
    for i in range(1, m + 1):
        cur = [i] + [0] * n
        for j in range(1, n + 1):
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1,
                         prev[j - 1] + (0 if a[i - 1] == b[j - 1] else 1))
        prev = cur
    return prev[n]

def nearly(a, b):
    if not a or not b: return False
    d = lev(a, b)
    lim = 1 if len(a) <= 6 else 2
    return 0 < d <= lim

def diff(A, B):
    m, n = len(A), len(B)
    L = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m - 1, -1, -1):
        for j in range(n - 1, -1, -1):
            L[i][j] = L[i + 1][j + 1] + 1 if A[i] == B[j] else max(L[i + 1][j], L[i][j + 1])
    ops = []
    i = j = 0
    while i < m and j < n:
        if A[i] == B[j]: ops.append(("ok", A[i], None)); i += 1; j += 1
        elif L[i + 1][j] >= L[i][j + 1]: ops.append(("miss", A[i], None)); i += 1
        else: ops.append(("extra", None, B[j])); j += 1
    while i < m: ops.append(("miss", A[i], None)); i += 1
    while j < n: ops.append(("extra", None, B[j])); j += 1
    out = []
    q = 0
    while q < len(ops):
        o = ops[q]; p = ops[q + 1] if q + 1 < len(ops) else None
        if o[0] == "miss" and p and p[0] == "extra" and nearly(o[1], p[2]):
            out.append(("sp", o[1], p[2])); q += 2
        elif o[0] == "extra" and p and p[0] == "miss" and nearly(p[1], o[2]):
            out.append(("sp", p[1], o[2])); q += 2
        else:
            out.append(o); q += 1
    return out

def score(correct, typed):
    A, B = toks(correct), toks(typed)
    ops = diff(A, B)
    ok = sum(1 for o in ops if o[0] == "ok")
    ex = sum(1 for o in ops if o[0] == "extra")
    pct = round(ok / (len(A) + ex) * 100) if A else 0
    return pct, ops

def show(ops):
    parts = []
    for k, a, b in ops:
        if k == "ok": parts.append(a)
        elif k == "sp": parts.append("~%s(go:%s)" % (a, b))
        elif k == "miss": parts.append("[-%s]" % a)
        else: parts.append("[+%s]" % b)
    return " ".join(parts)

CASES = [
    # (cau dung, nguoi go, mo ta, ky vong)
    ("The main problem is staff training.", "The main problem is staff training.", "go dung y het", 100),
    ("The main problem is staff training.", "the main problem is staff training", "khong hoa, khong cham", 100),
    ("The main problem is staff training.", "The main problem is staff trainning.", "sai chinh ta 1 tu", None),
    ("The main problem is staff training.", "The main problem is training.", "nghe sot 1 tu", None),
    ("The main problem is staff training.", "The main problem is the staff training.", "go thua 1 tu", None),
    ("I will send the quote this afternoon.", "I will sent the quote this afternoon.", "send/sent", None),
    ("We have five outlets in the city.", "We have five outlet in the city.", "thieu s so nhieu", None),
    ("Can you say that again?", "Can you see that again", "say -> see (nghe sai)", None),
    ("It is difficult to hire good cashiers.", "", "bo trong hoan toan", 0),
    ("Don't talk with your mouth full.", "Dont talk with your mouth full", "dau nhay bi bo", 100),
    ("The nurse checked my blood pressure.", "The nurse checked my blood pressure and more.", "them duoi", 75),
    ("Sales are up fifteen percent.", "Sales are up fifty percent.", "fifteen/fifty - PHAI la sai tu", None),
]

bad = 0
for correct, typed, desc, want in CASES:
    pct, ops = score(correct, typed)
    flag = ""
    if want is not None and pct != want:
        flag = "   <<< SAI, ky vong %d%%" % want; bad += 1
    print("%-34s %3d%%  %s%s" % (desc, pct, show(ops), flag))

print("\nKiem rieng nearly() - phan biet sai chinh ta vs sai tu:")
pairs = [("training","trainning",True),("send","sent",True),("outlets","outlet",True),
         ("say","see",False),("fifteen","fifty",False),("quote","quiet",False),
         ("their","there",False),("accept","except",False)]
for a,b,want in pairs:
    got = nearly(a,b)
    ok = "OK " if got==want else "SAI"
    print("  %s %-9s vs %-9s -> gan dung=%-5s (mong doi %s, lev=%d)" % (ok,a,b,got,want,lev(a,b)))
    if got!=want: bad += 1

print("\n==> %s" % ("TAT CA DUNG" if bad==0 else "CO %d CA SAI" % bad))
sys.exit(0 if bad==0 else 1)
