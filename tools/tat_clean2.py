# -*- coding: utf-8 -*-
import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_PROJ = _os.path.dirname(_HERE)
"""Loai cau rac (long ma tuy, meme, ngu phap sai, obscure) khoi data-dictation-tatoeba.js."""
import re, io
F = _PROJ + r"\data-dictation-tatoeba.js"
s = io.open(F, encoding="utf-8").read()

DROP = {
"You got the money?", "I buy, therefore I am.", "This is your guys' house.",
"How could I say?", "I want some blow.", "I want some coke.", "I want a doggo.",
"I want a doggy.", "I want a pupper.", "I am my struggles.", "That was very trippy.",
"This city is cursed.", "You are a scoundrel.", "Do you have diarrhea?",
"We have a stegosaurus.", "I love you bunches.", "There was an attempt.",
"They were the losers.", "Your love is false.", "I want some whisky.",
"The night is dusky.", "Do you know kabuki?", "She can speak Kabyle.",
"Is the food halal?", "Some do think so.", "Sorry, is that weird?",
"I want some coke.",
}

lines = s.split("\n")
out, dropped = [], []
for ln in lines:
    m = re.search(r't:"((?:[^"\\]|\\.)*)"', ln)
    if m and m.group(1) in DROP:
        dropped.append(m.group(1)); continue
    out.append(ln)
io.open(F, "w", encoding="utf-8").write("\n".join(out))
kept = len(re.findall(r'\{id:"', "\n".join(out)))
print("Da loai:", len(dropped), "| con lai:", kept, "cau Tatoeba")
for d in dropped: print("   -", d)
