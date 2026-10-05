#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build web app tra cứu TCVN 5687:2024.

Mặc định: 1 file duy nhất (nhúng data) -> web/index.html (dùng offline,
thuần HTML, không cần mạng, không cần build lại).
Với --split: tách thành index.html (repo root, gọn nhẹ) + data/tcvn5687_data.js
  để deploy online (vd: GitHub Pages), app nạp data qua <script src>.

Bản 1 file được minify + rút gọn key của data nhúng để giảm kích thước,
nhưng lúc chạy JS sẽ giải mã lại key gốc nên template dùng key gốc như thường.
"""
import json
import os
import re
import sys
from collections import Counter

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BASE)
TPL = os.path.join(BASE, "template.html")
DATA = os.path.join(ROOT, "data", "tcvn5687_data.json")
SPLIT = "--split" in sys.argv
PLACEHOLDER = "/*__DATA__*/"
TOKEN = "\x00DATA_PH\x00"


def minify(tpl):
    # Bảo vệ placeholder data trước khi strip comment
    tpl = tpl.replace(PLACEHOLDER, TOKEN)
    # Bỏ block comments /* ... */ (trang trí)
    tpl = re.sub(r"/\*.*?\*/", "", tpl, flags=re.S)
    # Bỏ // comments: template đã xác minh không chứa // trong string, không có http
    kept = []
    for ln in tpl.split("\n"):
        if ln.strip().startswith("//"):
            continue
        idx = ln.find("//")
        if idx != -1:
            ln = ln[:idx]
        kept.append(ln)
    tpl = "\n".join(kept)
    # Bỏ HTML comments trang trí
    tpl = re.sub(r"<!--.*?-->", "", tpl, flags=re.S)
    tpl = tpl.replace(TOKEN, PLACEHOLDER)
    # Minify nhẹ: bỏ indent đầu dòng, whitespace cuối dòng, gộp dòng trống.
    # An toàn vì template không dùng template literals (`), <pre>, hay string nhiều dòng.
    lines, out, prev_blank = tpl.split("\n"), [], False
    for ln in lines:
        s = ln.strip()
        if not s:
            if not prev_blank:
                out.append("")
            prev_blank = True
            continue
        prev_blank = False
        out.append(s)
    return "\n".join(out)


def short_names(n):
    alpha = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    names = list(alpha)
    i = 0
    while len(names) < n:
        names.append("a" + alpha[i % len(alpha)])
        i += 1
    return names[:n]


def shorten_data(data):
    """Rút gọn key của data nhúng (chỉ dùng cho bản 1 file)."""
    cnt = Counter()

    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items():
                cnt[k] += 1
                walk(v)
        elif isinstance(o, list):
            for i in o:
                walk(i)

    walk(data)
    keys_by_freq = [k for k, _ in cnt.most_common()]
    fwd = {k: s for k, s in zip(keys_by_freq, short_names(len(keys_by_freq)))}
    rev = {s: k for k, s in fwd.items()}

    def conv(o):
        if isinstance(o, dict):
            return {fwd[k]: conv(v) for k, v in o.items()}
        if isinstance(o, list):
            return [conv(i) for i in o]
        return o

    return json.dumps(conv(data), ensure_ascii=False, separators=(",", ":")), rev


def dict_compress(s, n_markers=26):
    """Nén chuỗi bằng thay thế các cụm lặp bằng ký tự PUA (U+E000+).

    Trả về (chuỗi đã nén, [từ điển]). Giải mã: thay ngược marker -> cụm.
    """
    used = set()
    dct = []
    for m in range(n_markers):
        marker = chr(0xE000 + m)
        best, best_saved = None, 0
        for L in (12, 10, 8, 6):
            c = Counter()
            for i in range(len(s) - L + 1):
                sub = s[i:i + L]
                if used & set(sub):
                    continue
                c[sub] += 1
            for sub, n in c.most_common(400):
                if n < 4:
                    break
                if used & set(sub):
                    continue
                # mỗi lần xuất hiện tiết kiệm (len-3) byte, trừ chi phí lưu từ điển
                saved = (len(sub.encode("utf-8")) - 3) * (n - 1) - len(sub.encode("utf-8"))
                if saved > best_saved:
                    best_saved, best = saved, sub
        if not best or best_saved <= 0:
            break
        dct.append(best)
        used.add(marker)
        s = s.replace(best, marker)
    return s, dct


def embed_data(data):
    """Tạo JS nhúng data cho bản offline 1 file: rút gọn key + nén từ điển."""
    short_json, rev = shorten_data(data)
    compressed, dct = dict_compress(short_json)
    rev_json = json.dumps(rev, ensure_ascii=False, separators=(",", ":"))
    dct_json = "[" + ",".join(json.dumps(x, ensure_ascii=False) for x in dct) + "]"
    s_json = json.dumps(compressed, ensure_ascii=False)
    js = (
        "const __KM=" + rev_json + ";"
        "const __X=o=>Array.isArray(o)?o.map(__X):o&&typeof o===\"object\"?"
        "Object.keys(o).reduce((r,k)=>(r[__KM[k]||k]=__X(o[k]),r),{}):o;"
        "const __D=" + dct_json + ";"
        "let __S=" + s_json + ";"
        "for(let __i=0;__i<__D.length;__i++)"
        "__S=__S.split(String.fromCharCode(57344+__i)).join(__D[__i]);"
        "const TCVN_DATA=__X(JSON.parse(__S));"
    )
    return js


with open(TPL, encoding="utf-8") as f:
    tpl = minify(f.read())
with open(DATA, encoding="utf-8") as f:
    data = json.load(f)

if SPLIT:
    # Bản online: index.html ở repo root, nạp data qua <script src>
    data_js = "const TCVN_DATA = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";"
    with open(os.path.join(ROOT, "data", "tcvn5687_data.js"), "w", encoding="utf-8") as f:
        f.write(data_js)
    target = "<script>\n" + PLACEHOLDER + "\n</script>"
    assert target in tpl, "không tìm thấy khối placeholder data"
    html = tpl.replace(target, '<script src="data/tcvn5687_data.js"></script>', 1)
    out_html = os.path.join(ROOT, "index.html")
    with open(out_html, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"OK: {out_html} ({os.path.getsize(out_html)//1024} KB)")
    print(f"OK: {os.path.join(ROOT, 'data', 'tcvn5687_data.js')} "
          f"({os.path.getsize(os.path.join(ROOT, 'data', 'tcvn5687_data.js'))//1024} KB)")
else:
    # Bản offline 1 file duy nhất, thuần HTML
    assert PLACEHOLDER in tpl, "không tìm thấy placeholder data"
    html = tpl.replace(PLACEHOLDER, embed_data(data), 1)
    out = os.path.join(BASE, "index.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    size = os.path.getsize(out)
    print(f"OK: {out} ({size//1024} KB, {size} bytes)")
