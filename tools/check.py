import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_PROJ = _os.path.dirname(_HERE)
import re, sys, io
from html.parser import HTMLParser

p = _PROJ + r"\index.html"
src = io.open(p, encoding="utf-8").read()
ok = True

# 1. JS inline qua esprima
import esprima
blocks = re.findall(r"<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>", src, re.S)
print("So khoi <script> inline:", len(blocks))
for i, b in enumerate(blocks, 1):
    try:
        esprima.parseScript(b)
        print("  JS #%d OK (%d dong)" % (i, b.count("\n")))
    except Exception as e:
        ok = False
        print("  JS #%d LOI: %s" % (i, e))

# 2. Can bang the HTML
VOID = set("area base br col embed hr img input link meta param source track wbr".split())
class P(HTMLParser):
    def __init__(s):
        super().__init__(convert_charrefs=True); s.stack=[]; s.err=[]
    def handle_starttag(s, tag, attrs):
        if tag not in VOID: s.stack.append((tag, s.getpos()))
    def handle_startendtag(s, tag, attrs): pass
    def handle_endtag(s, tag):
        if tag in VOID: return
        if not s.stack: s.err.append("Dong thua </%s> tai %s" % (tag, s.getpos())); return
        if s.stack[-1][0] != tag:
            s.err.append("Lech: </%s> tai %s nhung dang mo <%s> tu %s" % (tag, s.getpos(), s.stack[-1][0], s.stack[-1][1]))
            for j in range(len(s.stack)-1, -1, -1):
                if s.stack[j][0] == tag: del s.stack[j:]; return
            return
        s.stack.pop()
pp = P(); pp.feed(src)
if pp.err or pp.stack:
    ok = False
    for e in pp.err: print("  HTML:", e)
    for t, pos in pp.stack: print("  HTML: chua dong <%s> mo tai %s" % (t, pos))
else:
    print("HTML can bang the: OK")

# 3. Ngoac trong <style>
for st in re.findall(r"<style[^>]*>(.*?)</style>", src, re.S):
    o, c = st.count("{"), st.count("}")
    print("CSS: { = %d , } = %d -> %s" % (o, c, "OK" if o == c else "LECH"))
    if o != c: ok = False

print("\n==> " + ("TAT CA OK" if ok else "CO LOI"))
sys.exit(0 if ok else 1)
