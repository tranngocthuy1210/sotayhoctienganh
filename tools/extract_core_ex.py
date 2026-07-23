# -*- coding: utf-8 -*-
import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_PROJ = _os.path.dirname(_HERE)
import re, io
s = io.open(_PROJ + r"\data-vocab.js", encoding="utf-8").read()
ex = re.findall(r',ex:"((?:[^"\\]|\\.)*)"', s)
io.open("core_ex.txt", "w", encoding="utf-8").write("\n".join(ex))
print("So cau ex trong data-vocab.js:", len(ex))
for e in ex[:5]: print("  ", e)
