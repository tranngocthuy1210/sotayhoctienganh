# -*- coding: utf-8 -*-
import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_PROJ = _os.path.dirname(_HERE)
import re, io
s = io.open(_PROJ + r"\data-dictation-tatoeba.js", encoding="utf-8").read()
k = re.findall(r't:"((?:[^"\\]|\\.)*)"', s)
io.open("tat_kept.txt", "w", encoding="utf-8").write("\n".join(k))
print("kept", len(k))
for x in k[:5]: print("  ", x)
