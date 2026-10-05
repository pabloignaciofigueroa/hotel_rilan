#!/usr/bin/env python3
"""Arma index.html desde src/index.html.

Reemplaza cada <x-img ...> por un <img> responsivo con srcset, ancho/alto
reales y un placeholder borroso (LQIP). Uso: python3 tools/build.py
"""
import json, re, pathlib, html

ROOT = pathlib.Path(__file__).resolve().parent.parent
META = json.loads((ROOT / 'assets/img/meta.json').read_text())
SRC = (ROOT / 'src/index.html').read_text()


def attrs(s):
    kv = {k: (a if a else b) for k, a, b in re.findall(r"([\w-]+)=(?:\"([^\"]*)\"|'([^']*)')", s)}
    bare = re.sub(r"[\w-]+=(?:\"[^\"]*\"|'[^']*')", '', s).split()
    return kv | {k: '' for k in bare}


def repl(m):
    a = attrs(m.group(1))
    i = a['id']
    meta = META[i]
    eager = 'eager' in a
    cls = a.get('class', '')
    sizes = a.get('sizes', '100vw')
    alt = a.get('alt', '')
    extra = a.get('data', '')
    return (
        f'<img class="{cls}" src="assets/img/{i}-l.webp" '
        f'srcset="assets/img/{i}-s.webp 800w, assets/img/{i}-l.webp 1800w" sizes="{sizes}" '
        f'width="{meta["w"]}" height="{meta["h"]}" alt="{html.escape(alt)}" '
        f'{"fetchpriority=\"high\"" if eager else "loading=\"lazy\""} decoding="async" '
        f'style="background-image:url({meta["lqip"]})" {extra}>'
    )


out = re.sub(r'<x-img\s+([^>]*?)\s*/?>', repl, SRC)
(ROOT / 'index.html').write_text(out)
missing = re.findall(r'<x-img', out)
print('index.html listo', len(out) // 1024, 'KB', 'pendientes:', len(missing))
