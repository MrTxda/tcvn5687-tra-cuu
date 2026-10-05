#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build web app 1 file duy nhất: nhúng data JSON vào template.html -> index.html"""
import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))
TPL = os.path.join(BASE, "template.html")
DATA = os.path.join(BASE, "..", "data", "tcvn5687_data.json")
OUT = os.path.join(BASE, "index.html")

with open(TPL, encoding="utf-8") as f:
    tpl = f.read()
with open(DATA, encoding="utf-8") as f:
    data = json.load(f)

js = "const TCVN_DATA = " + json.dumps(data, ensure_ascii=False) + ";"
html = tpl.replace("/*__DATA__*/", js, 1)
assert "/*__DATA__*/" not in html, "placeholder chưa được thay thế"

with open(OUT, "w", encoding="utf-8") as f:
    f.write(html)
print(f"OK: {OUT} ({os.path.getsize(OUT)//1024} KB)")
