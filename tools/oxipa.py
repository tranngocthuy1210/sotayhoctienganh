# -*- coding: utf-8 -*-
"""Tra IPA giọng MỸ chính thống từ Oxford Learner's Dictionaries.

- Chỉ lấy phiên âm (dữ liệu sự kiện, chuỗi rất ngắn) — KHÔNG chép câu ví dụ của họ.
- Có cache ra đĩa: chạy lại không tải lại.
- Có nghỉ giữa các request cho lịch sự với máy chủ.

Dùng:  python oxipa.py <file-tu-moi-dong>   -> ghi ox_ipa.json
"""
import requests, re, json, io, os, sys, time, random

BASE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(BASE, "ox_cache.json")
OUT = os.path.join(BASE, "ox_ipa.json")
HDR = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                     "(KHTML, like Gecko) Chrome/126.0 Safari/537.36",
       "Accept-Language": "en-US,en;q=0.9"}

cache = {}
if os.path.exists(CACHE):
    try: cache = json.load(io.open(CACHE, encoding="utf-8"))
    except Exception: cache = {}

def save_cache():
    json.dump(cache, io.open(CACHE, "w", encoding="utf-8"), ensure_ascii=False)

def us_ipa(html):
    """Lấy chuỗi IPA trong khối phons_n_am (giọng Bắc Mỹ)."""
    i = html.find('class="phons_n_am"')
    if i < 0: return None
    m = re.search(r'<span class="phon">([^<]*)</span>', html[i:i + 3000])
    if not m: return None
    return m.group(1).strip().strip("/").strip()

def slugs(word):
    w = word.strip().lower()
    s = w.replace(" ", "-").replace("'", "-")
    out = [s, s + "_1", s + "_2"]
    if s.endswith("-"): out.insert(0, s.rstrip("-"))
    return out

def lookup(word, sess):
    if word in cache: return cache[word]
    res = {"ipa": None, "url": None, "status": "notfound"}
    for sl in slugs(word):
        url = "https://www.oxfordlearnersdictionaries.com/definition/english/" + sl
        try:
            r = sess.get(url, headers=HDR, timeout=25)
        except Exception as e:
            res["status"] = "error:" + type(e).__name__
            continue
        if r.status_code == 404:
            continue
        if r.status_code != 200:
            res["status"] = "http%d" % r.status_code
            continue
        ip = us_ipa(r.text)
        if ip:
            res = {"ipa": ip, "url": url, "status": "ok"}
            break
        res["status"] = "no_us_ipa"
    cache[word] = res
    return res

def main():
    if len(sys.argv) < 2:
        print("Thieu file danh sach tu"); return 1
    words = [l.strip() for l in io.open(sys.argv[1], encoding="utf-8") if l.strip()]
    sess = requests.Session()
    done = 0
    for w in words:
        if w in cache:
            done += 1; continue
        lookup(w, sess)
        done += 1
        if done % 20 == 0:
            save_cache()
            print("  ...%d/%d" % (done, len(words)), flush=True)
        time.sleep(random.uniform(0.35, 0.7))
    save_cache()
    out = {w: cache.get(w, {}).get("ipa") for w in words}
    json.dump(out, io.open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    bad = [w for w in words if not out.get(w)]
    print("XONG. Tra duoc %d/%d. Khong lay duoc: %d" % (len(words) - len(bad), len(words), len(bad)))
    if bad: print("   ", ", ".join(bad[:40]))
    return 0

if __name__ == "__main__":
    sys.exit(main())
