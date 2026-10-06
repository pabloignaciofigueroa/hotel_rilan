#!/usr/bin/env python3
"""Arma index.html desde src/index.html.

Reemplaza cada <x-img ...> por un <img> responsivo con srcset, ancho/alto
reales y un placeholder borroso (LQIP). Uso: python3 tools/build.py
"""
import json, re, pathlib, html

ROOT = pathlib.Path(__file__).resolve().parent.parent
META = json.loads((ROOT / 'assets/img/meta.json').read_text())
SRC = (ROOT / 'src/index.html').read_text()
ALT_EN = json.loads((ROOT / 'tools/alt-en.json').read_text())


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
    if alt and i in ALT_EN:
        extra += f' data-alt-en="{html.escape(ALT_EN[i])}"'
    elif alt:
        raise SystemExit(f'Falta alt en inglés para {i} (tools/alt-en.json)')
    return (
        f'<img class="{cls}" src="assets/img/{i}-l.webp" '
        f'srcset="assets/img/{i}-s.webp 800w, assets/img/{i}-l.webp 1800w" sizes="{sizes}" '
        f'width="{meta["w"]}" height="{meta["h"]}" alt="{html.escape(alt)}" '
        f'{"fetchpriority=\"high\"" if eager else "loading=\"lazy\""} decoding="async" '
        f'style="background-image:url({meta["lqip"]})" {extra}>'
    )


out = re.sub(r'<x-img\s+([^>]*?)\s*/?>', repl, SRC)

# Carga crítica: lo que la precarga espera (con su peso real) antes de entrar.
# frac = fracción del ancho de pantalla que ocupa la imagen (para elegir la variante s/l).
def size(rel):
    return (ROOT / rel).stat().st_size
CRITICAL_IMGS = [
    ('web_rilan_35', 1.0),                 # portada
    ('ig_2026-09-23_DdoqxbhxKbG', 1.0),    # Territory
    ('ig_2026-09-05_Dc41N1BRYMT', 0.42),   # Chilwe es territorio
    ('ig_2026-09-17_DdZd85rRxkm', 0.36),   # galería: sendero
    ('web_rilan_47', 0.52),                # galería: vista aérea
    ('ig_2026-09-02_DczRbckRl74', 1.0),    # Mysticism
    ('ig_2026-09-11_DdJ6xS-xtDC', 1.0),    # Refuge
    ('ig_2026-09-03_Dc00-W6RwgS', 1.0),    # Heritage
]
crit = {
    'fonts': [{'url': f'assets/fonts/{f}.woff2', 'bytes': size(f'assets/fonts/{f}.woff2')} for f in
              ['marcellus-latin-400-normal', 'newsreader-latin-300-normal', 'newsreader-latin-300-italic',
               'newsreader-latin-400-normal', 'newsreader-latin-400-italic']],
    'imgs': [{'frac': fr,
              's': {'url': f'assets/img/{i}-s.webp', 'bytes': size(f'assets/img/{i}-s.webp')},
              'l': {'url': f'assets/img/{i}-l.webp', 'bytes': size(f'assets/img/{i}-l.webp')}} for i, fr in CRITICAL_IMGS],
    'video': {'webm': {'url': 'assets/video/bienvenida.webm', 'bytes': size('assets/video/bienvenida.webm')},
              'mp4': {'url': 'assets/video/bienvenida.mp4', 'bytes': size('assets/video/bienvenida.mp4')},
              'poster': {'url': 'assets/video/bienvenida-poster.jpg', 'bytes': size('assets/video/bienvenida-poster.jpg')}},
}
out = out.replace('<!--CRITICAL-->', '<script type="application/json" id="critical">' + json.dumps(crit, separators=(',', ':')) + '</script>')
(ROOT / 'index.html').write_text(out)
missing = re.findall(r'<x-img', out)
print('index.html listo', len(out) // 1024, 'KB', 'pendientes:', len(missing))
