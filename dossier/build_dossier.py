#!/usr/bin/env python3
"""Dossier de decisiones de diseño — RILÁN.

Genera dossier/rilan-dossier-diseno.html: láminas de 13 × 8,5 in para imprimir.
Izquierda: la sección del sitio (escritorio + celular). Derecha: la disección.
Todo queda embebido (imágenes y tipografías) para enviarlo como un solo archivo.
Uso: python3 dossier/build_dossier.py
"""
import base64, glob, html, io, pathlib
from PIL import Image, ImageOps

ROOT = pathlib.Path(__file__).resolve().parent.parent
D = ROOT / 'dossier'
SH = D / 'shots'
RAW = ROOT / 'assets/raw/01_imagenes'
VID = ROOT / 'assets/raw/02_videos/1_exteriores_territorio'


# ---------------------------------------------------------------- imágenes
def b64img(img, w, q=80):
    img = img.convert('RGB')
    if img.width > w:
        img = img.resize((w, round(img.height * w / img.width)), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, 'JPEG', quality=q, optimize=True, progressive=True)
    return 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode()


def shot(name, w=1500):
    p = SH / f'{name}.jpg'
    return b64img(Image.open(p), w) if p.exists() else ''


def src(stem, w=420):
    """Miniatura del archivo original (sin recortar)."""
    hits = glob.glob(str(RAW / '*' / f'{stem}.jpg')) or glob.glob(str(VID / f'{stem}.jpg'))
    if not hits:
        return ''
    return b64img(ImageOps.exif_transpose(Image.open(hits[0])), w, 76)


def raw(stem, w=1950):
    hits = glob.glob(str(RAW / '*' / f'{stem}.jpg'))
    return b64img(ImageOps.exif_transpose(Image.open(hits[0])), w, 82)


def font(name):
    return 'data:font/woff2;base64,' + base64.b64encode((ROOT / 'assets/fonts' / f'{name}.woff2').read_bytes()).decode()


def png_file(rel, w=900):
    im = Image.open(ROOT / rel).convert('RGBA')
    if im.width > w:
        im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, 'PNG', optimize=True)
    return 'data:image/png;base64,' + base64.b64encode(buf.getvalue()).decode()


def svg_file(rel):
    return 'data:image/svg+xml;base64,' + base64.b64encode((ROOT / rel).read_bytes()).decode()


E = html.escape
MARK = '<svg class="mk" viewBox="0 0 513 590" aria-hidden="true"><path d="M5 585L250 5L508 585L425 585L243 128L75 585Z"/><rect x="223" y="519" width="54" height="54"/></svg>'
COORDS = '42° 32\' 55" S&nbsp;&nbsp;&nbsp;73° 43\' 16" O'

# Orden real del sitio (para el indicador de recorrido)
RECORRIDO = ['Precarga', 'Portada', 'Ventana Λ', 'Bienvenida', 'Territory', 'Senderos', 'Mysticism',
             'Se escucha', 'Refuge', 'Habitaciones', 'Fuego', 'Rucalaf', 'La cava', 'The Long Table',
             'Heritage', 'Arquitectura', 'Mónica y Rodrigo', 'Cómo llegar', 'Reservar']

# Fuentes citables
IG = {
    '02': 'Instagram · 1 sep 2026 · reel de bienvenida',
    '03': 'Instagram · 2 sep 2026',
    '04': 'Instagram · 3 sep 2026',
    '05': 'Instagram · 4 sep 2026',
    '06': 'Instagram · 5 sep 2026',
    '07': 'Instagram · 8 sep 2026',
    '09': 'Instagram · 10 sep 2026',
    '10': 'Instagram · 11 sep 2026',
    '11': 'Instagram · 13 sep 2026',
    '12': 'Instagram · 15 sep 2026 · video',
    '13': 'Instagram · 17 sep 2026',
    '14': 'Instagram · 19 sep 2026',
    '15': 'Instagram · 23 sep 2026',
    '16': 'Instagram · 1 oct 2026',
    '17': 'Instagram · 3 oct 2026 · The Long Table',
}
GAL = 'Galería de fotos del hotel'


# ---------------------------------------------------------------- piezas de lámina
def quote(text, source):
    return f'<blockquote class="q"><p>{text}</p><cite>{E(source)}</cite></blockquote>'


def thumbs(items):
    """items: [(stem, pie)]"""
    out = []
    for stem, cap in items:
        u = src(stem)
        if u:
            out.append(f'<figure class="th"><img src="{u}" alt=""><figcaption>{cap}</figcaption></figure>')
    return f'<div class="ths">{"".join(out)}</div>'


def chips(items):
    return '<div class="chips">' + ''.join(
        f'<span class="chip"><i style="background:{hx}"></i><b>{E(n)}</b> {hx}</span>' for n, hx in items) + '</div>'


def block(title, body, cls=''):
    return f'<section class="bk {cls}"><h4>{title}</h4>{body}</section>'


def recorrido(cur):
    li = ''.join(f'<li class="{"on" if r == cur else ""}">{E(r)}</li>' for r in RECORRIDO)
    return f'<ol class="rec">{li}</ol>'


def lamina_seccion(n, nombre, titulo, lead, desk, mob, bloques, nota_izq='', desk2=None):
    left_extra = f'<img class="desk2" src="{shot(desk2)}" alt="">' if desk2 else ''
    if desk2:
        mob = None
    mob_html = f'<img class="mob" src="{shot(mob, 520)}" alt="">' if mob else ''
    return f'''
<article class="lam">
  <div class="L {'two' if desk2 else ''}">
    <p class="lab">Sitio · computador</p>
    <img class="desk" src="{shot(desk)}" alt="">
    {left_extra}
    <div class="Lrow">
      {f'<div class="mobw"><p class="lab">Celular</p>{mob_html}</div>' if mob else ''}
      <div class="Linfo">
        <p class="lab">Lugar en el recorrido</p>
        {recorrido(nombre)}
        {f'<p class="lnote">{nota_izq}</p>' if nota_izq else ''}
      </div>
    </div>
  </div>
  <div class="R">
    <p class="kick">{n:02d} · {E(nombre)}</p>
    <h2>{titulo}</h2>
    <p class="lead">{lead}</p>
    <div class="grid">{''.join(bloques)}</div>
    <footer class="pf"><span>RILÁN · Decisiones de diseño del sitio</span><span>{COORDS}</span><span>{n:02d}</span></footer>
  </div>
</article>'''


def lamina_libre(n, left_html, right_html, left_cls='', right_cls=''):
    return f'''
<article class="lam">
  <div class="L {left_cls}">{left_html}</div>
  <div class="R {right_cls}">{right_html}
    <footer class="pf"><span>RILÁN · Decisiones de diseño del sitio</span><span>{COORDS}</span><span>{n:02d}</span></footer>
  </div>
</article>'''


# ---------------------------------------------------------------- contenido
L = []
n = 0


def nx():
    global n
    n += 1
    return n


# 01 · Portada del dossier
nx()
L.append(f'''
<article class="lam cover">
  <div class="L full"><img class="bleed" src="{raw('web_rilan_35')}" alt="" style="object-position:58% 70%"></div>
  <div class="R center">
    {MARK}
    <h1>RILÁN</h1>
    <p class="sub">Decisiones de diseño del sitio web</p>
    <p class="for">Preparado para Mónica y Rodrigo</p>
    <p class="meta">Península de Rilán · Chiloé · Octubre 2026</p>
    <p class="coords">{COORDS}</p>
    <footer class="pf"><span>hotelrilan.vercel.app</span><span></span><span>01</span></footer>
  </div>
</article>''')

# 02 · Carta
nx()
L.append(lamina_libre(n,
    f'<img class="bleed" src="{raw("web_rilan_51")}" alt="" style="object-position:40% 50%">',
    f'''<p class="kick">Antes de empezar</p>
    <h2>Un sitio hecho con lo que ustedes ya dijeron</h2>
    <div class="letter">
      <p>Mónica, Rodrigo:</p>
      <p>Este sitio nació de mirar con atención lo que RILÁN ya publica. No hay frases inventadas ni promesas de agencia: cada título y cada párrafo sale de sus posts de Instagram, de sus historias destacadas, de su bio o de lo que sus huéspedes escribieron en Booking. Lo que hicimos fue ordenarlo, darle aire y ponerlo en movimiento.</p>
      <p>Tampoco hay fotos de banco de imágenes. Todas las imágenes y los dos videos son de RILÁN, y la tipografía, los colores y el isotipo se reconstruyeron a partir de sus propias piezas gráficas.</p>
      <p>Este documento explica, sección por sección, qué se decidió y por qué. En cada lámina, a la izquierda está la sección tal como se ve en el sitio, en computador y en celular. A la derecha, de dónde salió cada texto e imagen, qué letra y qué color se usó, cómo se compuso y por qué va en ese lugar del recorrido.</p>
      <p>Es un regalo. Ojalá lo disfruten tanto como nosotros disfrutamos haciéndolo.</p>
      <p class="sign">Pablo Figueroa G.<br>Director de estudio</p>
    </div>''', left_cls='full'))

# 03 · De dónde viene todo
nx()
grid_ig = ''.join(f'<img src="{src(s, 300)}" alt="">' for s in [
    'ig_2026-09-02_DczRbckRl74', 'ig_2026-09-03_Dc00-W6RwgS', 'ig_2026-09-04_Dc4OjPFxmeq',
    'ig_2026-09-05_Dc41N1BRYMT', 'ig_2026-09-08_DdB-aHPxysK', 'ig_2026-09-09_DdEiX-IROtq', 'ig_2026-09-10_DdHRZK0RRZJ',
    'ig_2026-09-11_DdJ6xS-xtDC', 'ig_2026-09-13_DdOtAZ-xADQ', 'ig_2026-09-17_DdZd85rRxkm', 'ig_2026-09-19_DdeJ_vyRYHF',
    'ig_2026-09-23_DdoqxbhxKbG', 'ig_2026-10-01_Dd9lVx2hs4R', 'ig_2026-10-03_DeCNBLVEfM9_04', 'ig_2026-10-03_DeCNBLVEfM9_01'])
dest = ''.join(f'<img src="{src(s, 240)}" alt="">' for s in ['ig-destacada_TERRITORY_01', 'ig-destacada_MYSTICISM_01', 'ig-destacada_REFUGE_01', 'ig-destacada_HERITAGE_01'])
L.append(lamina_libre(n,
    f'''<p class="lab">Instagram · publicaciones de agosto a octubre de 2026</p>
    <div class="igrid">{grid_ig}</div>
    <p class="lab" style="margin-top:.18in">Historias destacadas · TERRITORY · MYSTICISM · REFUGE · HERITAGE</p>
    <div class="dgrid">{dest}</div>''',
    f'''<p class="kick">Materia prima</p>
    <h2>De dónde viene todo</h2>
    <p class="lead">Antes de diseñar, reunimos todo lo que RILÁN ya había publicado y lo ordenamos en carpetas: exteriores, interiores, gastronomía, habitaciones, detalles y piezas gráficas.</p>
    <div class="grid">
      {block('Instagram @rilanhotel', '<p><b>17 publicaciones</b>, con sus textos completos en español e inglés, y <b>2 videos</b>: el reel de bienvenida y el paisaje sonoro submarino.</p>')}
      {block('Historias destacadas', '<p><b>4 destacadas, 18 imágenes.</b> Sus nombres (Territory, Mysticism, Refuge, Heritage) se convirtieron en los cuatro capítulos del sitio.</p>')}
      {block('Galería de fotos', '<p><b>41 fotografías</b> de la galería del hotel. De Booking se rescataron en su mayor tamaño, para que se vean nítidas a pantalla completa.</p>')}
      {block('Booking.com', '<p><b>99 reseñas</b> con nota 9,5, Excepcional, y la ficha del hotel: horarios, normas, distancias y habitación. Son los únicos datos "duros" del sitio.</p>')}
      {block('La regla', '<p>Cada texto del sitio tiene su origen identificado: qué post, qué destacada o qué reseña. Las reseñas se citan tal cual, en su idioma original y con su ortografía. Solo se corrigieron tres concordancias gramaticales en textos de RILÁN.</p>', 'wide')}
    </div>'''))

# 04 · La voz
nx()
L.append(lamina_libre(n,
    f'''<p class="lab">Pieza gráfica · The Long Table · Instagram, 3 oct 2026</p>
    <img class="piece" src="{src('ig_2026-10-03_DeCNBLVEfM9_01', 900)}" alt="">
    <div class="pair"><img src="{src('ig_2026-10-03_DeCNBLVEfM9_03', 600)}" alt=""><img src="{src('ig-destacada_MYSTICISM_02', 600)}" alt=""></div>''',
    f'''<p class="kick">Sistema · voz</p>
    <h2>Escribir como RILÁN</h2>
    <p class="lead">El sitio no agrega adjetivos ni promesas: escribe con la voz que la marca ya construyó y pone cada frase en el lugar justo.</p>
    <div class="grid">
      {block('Frases cortas, enumeraciones de materia', quote('La madera, el fuego, el patrimonio, el silencio.', IG['02']) + quote('El viento, las aves, la madera, el agua, el bosque.', IG['11']))}
      {block('Un vocabulario propio', '<p>Territorio, misticismo, archipiélago, refugio, ritmo, retornar. Y dos palabras locales que se mantuvieron tal cual: <b>Chilwe</b>, en lugar de "Chiloé", cuando ustedes la usan, y <b>bordemar</b>.</p>')}
      {block('Bilingüe, como en sus posts', '<p>Los posts vienen en español e inglés; el sitio usa la versión del idioma elegido. Lo que existe en un solo idioma (la bio, la destacada Mysticism, las reseñas en francés o alemán) se muestra como fue escrito: le da el tono internacional que tienen sus huéspedes.</p>')}
      {block('Sin superlativos', '<p>No hay "el mejor", "único" ni "exclusivo". El tono es sereno y contemplativo, y la confianza la ponen los huéspedes: 9,5 en 99 reseñas.</p>')}
      {block('Las coordenadas como firma', f'<p>Las destacadas cierran con <span class="tl">{COORDS}</span>. En el sitio cumplen el mismo papel: aparecen en la carga, en cada portada de capítulo y en el pie.</p>', 'wide')}
    </div>'''))

# 05 · Tipografía
nx()
L.append(lamina_libre(n,
    f'''<p class="lab">Original de RILÁN (pieza gráfica)</p>
    <img class="piece" src="{src('ig_2026-10-03_DeCNBLVEfM9_01', 900)}" alt="" style="max-height:2.6in;object-fit:cover;object-position:50% 52%">
    <p class="lab" style="margin-top:.2in">Equivalentes elegidas para la web</p>
    <div class="spec">
      <p class="sp1">THE LONG TABLE</p><p class="cap">Marcellus · títulos y rótulos en mayúsculas espaciadas</p>
      <p class="sp2">Una mesa larga y abierta a todos. Cocina de campo y mar del archipiélago.</p><p class="cap">Newsreader liviana · texto de lectura</p>
      <p class="sp3">42° 32' 55" S&nbsp;&nbsp;73° 43' 16" O</p><p class="cap">Marcellus pequeña y muy espaciada · coordenadas y rótulos</p>
    </div>''',
    f'''<p class="kick">Sistema · tipografía</p>
    <h2>Dos letras, las suyas</h2>
    <p class="lead">El sitio actual no estaba en línea, así que identificamos la tipografía comparando sus piezas gráficas con decenas de candidatas de uso libre, una al lado de la otra.</p>
    <div class="grid">
      {block('Marcellus · títulos', '<p>Es una romana tallada, de trazos que se abren hacia los remates, muy cercana a las mayúsculas de THE LONG TABLE, MENÚ y de sus destacadas. Se usa solo en mayúsculas espaciadas: nombres de capítulo, títulos y coordenadas.</p>')}
      {block('Newsreader · lectura', '<p>Es una serif con altura generosa y números de estilo antiguo ($70.000), como el texto de sus piezas. Se usa en su versión liviana para títulos largos y en la normal para párrafos, sin negritas.</p>')}
      {block('Tamaños', '<p>Pocos tamaños y muy contrastados: las palabras de capítulo, enormes, casi como paisaje; los títulos, grandes y apretados; los párrafos, cómodos y con mucho espacio entre líneas; los rótulos, pequeños y muy espaciados.</p>')}
      {block('Descartadas', '<p>Cinzel, Cormorant, Forum y Tenor Sans se compararon y quedaron fuera: eran demasiado ornamentales o demasiado geométricas frente a la letra de RILÁN.</p>')}
      {block('Un detalle', '<p>Las letras viajan con el propio sitio y ya están listas cuando se abre la portada. Así el texto nunca cambia de forma mientras se lee.</p>', 'wide')}
    </div>'''))

# 06 · Paleta
nx()
pal_imgs = ''.join(f'<img src="{src(s, 330)}" alt="">' for s in ['ig_2026-10-03_DeCNBLVEfM9_06', 'ig_2026-09-23_DdoqxbhxKbG', 'ig_2026-09-11_DdJ6xS-xtDC', 'ig-destacada_MYSTICISM_04', 'web_rilan_11', 'web_rilan_35'])
L.append(lamina_libre(n,
    f'''<p class="lab">De estas imágenes salen los colores</p><div class="pgrid">{pal_imgs}</div>
    <div class="swatches">
      <span style="background:#EAE9E3;color:#544F4C">Niebla<br>#EAE9E3</span><span style="background:#544F4C">Piedra<br>#544F4C</span><span style="background:#121311">Noche<br>#121311</span>
      <span style="background:#2C362F">Bosque<br>#2C362F</span><span style="background:#644B34">Madera<br>#644B34</span><span style="background:#B07436">Fuego<br>#B07436</span>
    </div>''',
    f'''<p class="kick">Sistema · color</p>
    <h2>La paleta está en sus fotos</h2>
    <p class="lead">No elegimos colores "de diseño". Medimos los tonos que más se repiten en sus fotografías y en sus piezas gráficas, y de ahí salió la paleta.</p>
    <div class="grid">
      {block('Base de marca', chips([('Niebla', '#EAE9E3'), ('Piedra', '#544F4C'), ('Ceniza', '#847F7B')]) + '<p>El fondo claro y el gris cálido de sus piezas gráficas: son el 90 % del color de THE LONG TABLE.</p>')}
      {block('Territorio', chips([('Noche', '#121311'), ('Bosque', '#2C362F'), ('Madera', '#644B34')]) + '<p>Las sombras de los exteriores, el verde de los helechos y la madera de los muros.</p>')}
      {block('Un solo acento', chips([('Fuego', '#B07436')]) + '<p>Es el cobre del fuego y de la luz cálida de los interiores. Se usa con mesura: en la barra de avance, en el marcador del mapa y en pequeñas notas. Nunca en textos largos.</p>')}
      {block('Legibilidad', '<p>Cada combinación de texto y fondo se revisó para que se lea con holgura, incluso con poca vista o con el sol sobre la pantalla.</p>')}
    </div>'''))

# 07 · Isotipo
nx()
L.append(lamina_libre(n,
    f'''<div class="logos">
      <p class="lab" style="grid-column:1/-1;margin-bottom:4pt">Isotipo redibujado · variantes de uso</p>
      <div class="lg light"><img src="{png_file('brand/logo/png/rilan-isotipo-dark.png', 500)}" alt=""></div>
      <div class="lg dark"><img src="{png_file('brand/logo/png/rilan-isotipo-light.png', 500)}" alt=""></div>
      <div class="lg light wide"><img src="{png_file('brand/logo/png/rilan-horizontal-dark.png', 1100)}" alt=""></div>
      <div class="lg dark"><img src="{png_file('brand/logo/png/rilan-vertical-light.png', 600)}" alt=""></div>
      <div class="lg light"><img src="{png_file('brand/logo/png/favicon-512.png', 400)}" alt="" style="width:46%"></div>
    </div>''',
    f'''<p class="kick">Sistema · isotipo</p>
    <h2>Λ. a cualquier tamaño</h2>
    <p class="lead">El isotipo, una A sin travesaño con un punto cuadrado bajo el vértice, se midió sobre una de sus piezas ampliada y se redibujó para que sea nítido a cualquier tamaño, desde el ícono de la pestaña del navegador hasta un letrero.</p>
    <div class="grid">
      {block('Proporciones respetadas', '<p>El trazo izquierdo es más fino que el derecho, como en el original. El punto es un cuadrado centrado y el vértice va levemente aplanado.</p>')}
      {block('Variantes', '<p>Isotipo, logotipo RILÁN, versión vertical (como en las destacadas) y horizontal, cada una en claro y oscuro. Además, el ícono de la pestaña del navegador y la imagen que aparece al compartir el enlace.</p>')}
      {block('Logotipo', '<p>RILÁN se compuso en Marcellus con espaciado amplio. Quedó dibujado como imagen, para que se vea idéntico en cualquier pantalla o impresión.</p>')}
      {block('Dónde aparece', '<p>Se dibuja en la pantalla de carga, encabeza cada capítulo como en sus destacadas y es la "ventana" del video de bienvenida.</p>')}
    </div>''', left_cls='full'))

# 08 · Recorrido
nx()
strip = ''.join(f'<figure><img src="{shot(s, 420)}" alt=""><figcaption>{c}</figcaption></figure>' for s, c in [
    ('d-hero', 'Portada'), ('d-portal-b', 'Ventana Λ'), ('d-territory', 'Territory'), ('d-mysticism', 'Mysticism'),
    ('d-refuge', 'Refuge'), ('d-kitchen', 'Rucalaf'), ('d-heritage', 'Heritage'), ('d-hosts', 'Mónica y Rodrigo'), ('d-book', 'Reservar')])
L.append(lamina_libre(n,
    f'<p class="lab">El recorrido completo, de arriba hacia abajo</p><div class="strip">{strip}</div>',
    f'''<p class="kick">Sistema · recorrido</p>
    <h2>Un relato en cuatro capítulos</h2>
    <p class="lead">El orden de la página no es una lista de servicios: es un viaje que va de lo más amplio a lo más íntimo, y termina en una invitación.</p>
    <div class="grid">
      {block('1 · Llegar', '<p>Primero se ve la noche y el hotel encendido; luego la Λ se abre al video. Antes de hablar del hotel, se cuenta dónde está: "Al sur del mundo".</p>')}
      {block('2 · Los cuatro capítulos', '<p><b>Territory, Mysticism, Refuge y Heritage</b> son sus propias historias destacadas, y cada capítulo abre igual que ellas: foto a sangre, Λ, palabra y coordenadas.</p>')}
      {block('3 · Habitar', '<p>Dentro de Refuge están las habitaciones y el fuego. La cocina de Rucalaf, la cava y The Long Table siguen como una sobremesa.</p>')}
      {block('4 · Confiar y venir', '<p>Heritage cierra el relato con la iglesia y el oficio. Después hablan los huéspedes (Mónica y Rodrigo), y recién entonces: cómo llegar y reservar.</p>')}
      {block('Ritmo', '<p>Se alternan secciones a pantalla completa, oscuras e inmersivas, con secciones claras de lectura, como respirar. Ninguna composición se repite dos veces seguidas.</p>', 'wide')}
    </div>'''))

# ---------------------------------------------------------------- secciones
def S(nombre, titulo, lead, desk, mob, bloques, nota='', desk2=None):
    L.append(lamina_seccion(nx(), nombre, titulo, lead, desk, mob, bloques, nota, desk2))


S('Precarga', 'La espera como umbral',
  'Antes de entrar, el sitio descarga lo esencial: tipografías, portada, portadas de capítulo y el video. Mientras tanto se dibuja la Λ y corre un porcentaje real de lo que falta.',
  'd-loader', None, [
      block('Qué se ve', '<p>La Λ se traza y luego se rellena. Debajo, el avance va de 00 a 100 % en la misma letra de las coordenadas. Al llegar a 100, el número se desvanece, aparecen <span class="tl">' + COORDS + '</span> y se levanta la cortina.</p>'),
      block('Por qué', '<p>Un sitio hecho de fotos y video se rompe si carga a saltos. Esta espera breve asegura que todo lo que se ve primero ya esté listo, y la convierte en un momento de marca.</p>'),
      block('Tiempos', '<p>Dura casi dos segundos aunque la conexión sea rápida, para que se sienta. Y nunca más de ocho hasta ver la portada, aunque la conexión sea lenta. El resto del sitio se descarga en segundo plano mientras se mira la portada.</p>'),
      block('Color y letra', chips([('Noche', '#121311'), ('Niebla', '#EAE9E3')]) + '<p>Marcellus pequeña y espaciada, la misma letra de las coordenadas.</p>'),
  ], nota='Captura tomada mientras el porcentaje avanza.')

S('Portada', 'La noche, el hotel encendido',
  'La primera imagen es la más característica de RILÁN: sus volúmenes de madera iluminados bajo la Vía Láctea. Sobre el cielo, solo el nombre y una frase suya.',
  'd-hero', 'm-hero', [
      block('Textos', quote('Bienvenidos al misticismo del archipiélago.', IG['03']) + quote('A secluded hotel on the Rilán Peninsula. Within a UNESCO World Heritage landscape.', 'Bio de Instagram · en su idioma original')),
      block('Imagen', thumbs([('web_rilan_35', 'web_rilan_35 · ' + GAL)]) + '<p>Se ancló al borde inferior para que el título quede sobre el cielo y nunca tape las ventanas encendidas.</p>'),
      block('Letra', '<p>RILÁN en Marcellus, enorme y con letras espaciadas: es el logotipo, a escala de paisaje. La frase va en Newsreader itálica liviana.</p>'),
      block('Movimiento', '<p>Las letras suben una a una, como si salieran de detrás de una línea, y la foto se asienta desde un leve zoom. Al bajar, el nombre se separa y se desvanece.</p>'),
      block('Por qué primero', '<p>Responde en un segundo dónde y qué es. La noche estrellada anticipa el silencio y el aislamiento que valoran los huéspedes.</p>', 'wide'),
  ])

S('Ventana Λ', 'El isotipo se abre',
  'Es el momento memorable del sitio. El isotipo se convierte en una ventana con forma de A, como las casas de RILÁN, que deja ver el reel de bienvenida. Al bajar, crece hasta llenar la pantalla.',
  'd-portal-a', None, [
      block('Textos', quote('Al sur del mundo, una isla donde el tiempo sigue un ritmo propio.', IG['02']) + quote('La madera, el fuego, el patrimonio, el silencio.', IG['02']) + '<p>Las cuatro palabras aparecen una a una cuando el video ya ocupa toda la pantalla.</p>'),
      block('Video', thumbs([('ig_2026-09-01_DcwvNlMxpss_portada', 'Reel de bienvenida · Instagram, 1 sep 2026')]) + '<p>Es el mismo reel de Instagram (54 s). Se aligeró a la mitad de su peso, sin pérdida visible, y se descarga durante la espera inicial para que nunca se corte.</p>'),
      block('Composición', '<p>El fondo es niebla y el texto va a la izquierda. La ventana triangular está centrada y lleva el punto del isotipo en su base. Se abre al bajar por la página, sin botones.</p>'),
      block('Por qué aquí', '<p>Después de la noche, la marca "abre la puerta": se entra literalmente por el isotipo.</p>'),
  ], desk2='d-portal-b', nota='Arriba, la ventana cerrada. Abajo, abierta, con las cuatro palabras.')

S('Bienvenida', 'Bienvenidos a RILÁN',
  'Una pausa clara y centrada después del video, con mucho aire. Es la primera vez que el texto respira solo.',
  'd-welcome', 'm-welcome', [
      block('Textos', quote('Aquí, el misticismo del archipiélago se revela lentamente, moldeado por la tierra, el mar y siglos de tradición.', IG['02']) + quote('Bienvenidos a RILÁN', IG['02']) + '<p class="small">Se corrigió la concordancia del original ("se revelan", "moldeados").</p>'),
      block('Letra y color', chips([('Niebla', '#EAE9E3'), ('Piedra', '#544F4C')]) + '<p>El párrafo va en Newsreader liviana y grande, y el título, en Marcellus en mayúsculas. Solo un pequeño Λ como ornamento.</p>'),
      block('Movimiento', '<p>Las líneas aparecen una tras otra, subiendo desde abajo, con arranque rápido y frenado suave.</p>'),
      block('Por qué aquí', '<p>Cierra el prólogo con el mismo saludo con que termina el texto del reel, y abre paso a los capítulos.</p>'),
  ])

S('Territory', 'Chilwe es territorio antes que destino',
  'El primer capítulo abre como su historia destacada: foto a sangre, Λ, la palabra TERRITORY y las coordenadas. Después, una sección clara con la frase que define el capítulo.',
  'd-territory', 'm-chapter', [
      block('Textos', quote('Chilwe es territorio antes que destino. Una geografía marcada por su bordemar, por el bosque, por el agua y por las personas…', IG['06'])),
      block('Imágenes', thumbs([('ig_2026-09-23_DdoqxbhxKbG', 'Helechos · ' + IG['15']), ('ig_2026-09-05_Dc41N1BRYMT', 'Musgo · ' + IG['06']), ('ig-destacada_TERRITORY_01', 'Destacada TERRITORY')])),
      block('Composición', '<p>La portada tiene la misma gramática que la destacada, pero a pantalla completa. Al pasar, la palabra "respira": sus letras, muy separadas al principio, se van juntando. La sección clara es asimétrica: título grande a la izquierda y foto vertical a la derecha.</p>'),
      block('Color', chips([('Helecho', '#113A1F'), ('Niebla', '#EAE9E3')]) + '<p>El verde viene de la propia foto.</p>'),
  ], desk2='d-chapter')

S('Senderos', 'Perderse también es retornar',
  'Una galería horizontal: al bajar, el paisaje avanza de lado, como caminar por un sendero. En celular se recorre deslizando con el dedo.',
  'd-hscroll', None, [
      block('Textos', quote('Perderse en los senderos de RILÁN es otra forma de entrar en el bosque. […] Aquí, perderse también es una forma de retornar.', IG['13']) + quote('El bosque guarda su propio ritmo.', IG['15'])),
      block('Imágenes', thumbs([('ig_2026-09-17_DdZd85rRxkm', 'Sendero · ' + IG['13']), ('web_rilan_47', 'Vista aérea · galería'), ('web_rilan_03', 'Iglesia entre árboles · galería'), ('ig_2026-09-13_DdOtAZ-xADQ', 'Pilotes · ' + IG['11'])])),
      block('Composición', '<p>Fotos de tres formatos (vertical, panorámica y media) a distintas alturas, como pasos irregulares. Cada foto entra con una cortina lateral y se desplaza levemente dentro de su marco.</p>'),
      block('Sin tropiezos', '<p>Está construida para que la página no dé saltos al entrar ni al salir de la galería: el paso de vertical a horizontal se siente continuo.</p>'),
  ], nota='En celular es un carrusel horizontal con deslizamiento.')

S('Mysticism', 'El silencio aquí tiene capas',
  'El segundo capítulo es el más contemplativo: cielo, niebla y silencio. La portada usa el texto de su propia destacada, en el idioma en que fue escrito.',
  'd-mysticism', 'm-silence', [
      block('Textos', quote('The more intimate, atmospheric and contemplative side of Chiloé. Sunsets, silence, fire, mist, changing skies…', 'Destacada MYSTICISM · en su idioma original') + quote('El silencio aquí tiene capas. El viento, las aves, la madera, el agua, el bosque.', IG['11'])),
      block('Imágenes', thumbs([('ig_2026-09-02_DczRbckRl74', 'Nubes · ' + IG['03']), ('web_rilan_16', 'Terraza en niebla · galería'), ('ig-destacada_MYSTICISM_01', 'Destacada MYSTICISM')])),
      block('Composición', '<p>Las cinco "capas" del silencio se listan una bajo otra, en Marcellus, y se encienden de a una, como sonidos que aparecen al aquietarse.</p>'),
      block('Por qué aquí', '<p>Después del territorio físico, el capítulo invisible: lo que se siente. Prepara el oído para la sección siguiente.</p>'),
  ], desk2='d-silence')

S('Se escucha', 'Chilwe también se escucha',
  'Una sección de video con sonido opcional: la ballena del post del 15 de septiembre, con los registros submarinos del investigador Francisco Viddi.',
  'd-listen', 'm-listen', [
      block('Textos', quote('Chilwe también se escucha. Bajo la superficie, el archipiélago tiene su propio paisaje sonoro…', IG['12']) + '<p>El crédito "Registro sonoro: Francisco Viddi" se mantiene tal como ustedes lo publicaron.</p>'),
      block('Video', thumbs([('ig_2026-09-15_DdUL3rhEeI1_portada', 'Ballena · Instagram, 15 sep 2026')])),
      block('Interacción', '<p>Un botón "Escuchar" con barras de sonido animadas. El volumen sube de a poco. El video se pausa al salir de pantalla y el sonido nunca arranca solo.</p>'),
      block('Por qué aquí', '<p>Remata Mysticism con algo que solo RILÁN tiene: el paisaje sonoro bajo el mar que rodea al hotel.</p>'),
  ])

S('Refuge', 'Un refugio no pide dejar el mundo atrás',
  'El tercer capítulo entra al hotel. La portada es la luz de la tarde sobre las bancas con pieles, y la sección clara alterna dos fotos de interior con dos textos suyos.',
  'd-refuge', 'm-refuge-text', [
      block('Textos', quote('Un refugio no pide dejar el mundo atrás. Solo tomar la distancia suficiente para volver a mirarlo de otra manera.', IG['07']) + quote('En RILÁN, la madera crea esa sensación de estar protegido sin dejar de pertenecer al paisaje.', IG['05'])),
      block('Imágenes', thumbs([('ig_2026-09-11_DdJ6xS-xtDC', 'Luz entre listones · ' + IG['10']), ('web_rilan_42', 'Sala al atardecer · galería'), ('ig_2026-10-01_Dd9lVx2hs4R', 'Rincón de lectura · ' + IG['16'])])),
      block('Composición', '<p>La foto horizontal grande va a la izquierda y la vertical pequeña, desplazada hacia abajo, a la derecha, para que la página no quede simétrica. Las fotos entran con una cortina vertical.</p>'),
      block('Color', chips([('Madera', '#644B34'), ('Niebla', '#EAE9E3')])),
  ], desk2='d-refuge-text')

S('Habitaciones', 'La misma materia que lo rodea',
  'Un carrusel que se arrastra con el mouse o el dedo, con fotos grandes y verticales alternadas. Sobre él, cuatro datos precisos de Booking.',
  'd-rooms', 'm-rooms', [
      block('Textos', quote('Un refugio construido con la misma materia que lo rodea.', IG['05']) + '<p><b>Datos (Booking):</b> 8 habitaciones · 30 m² · vista al mar con balcón · cama king o dos individuales.</p>'),
      block('Imágenes', thumbs([('web_rilan_13', 'Ventanal al mar · galería'), ('ig_2026-09-04_Dc4OjPFxmeq', 'Lana · ' + IG['05']), ('ig_2026-09-09_DdEiX-IROtq', 'Lavamanos · Instagram 9 sep'), ('web_rilan_56', 'Ducha con vista · galería')])),
      block('Interacción', '<p>Al pasar sobre el carrusel aparece la etiqueta "Arrastrar", sin ocultar el cursor. Tiene un contador de 01 a 09, una barra de avance y flechas para quien navega con teclado.</p>'),
      block('Por qué así', '<p>Las reseñas destacan la vista desde la cama y desde el baño. Por eso hay más fotos de ventanales que de muebles.</p>'),
  ])

S('Fuego', 'Un refugio para otro ritmo',
  'Una pausa a pantalla completa: la sala con la estufa encendida y la frase que mejor resume la estadía.',
  'd-fire', 'm-fire', [
      block('Textos', quote('RILÁN es un refugio para otro ritmo. Fuego, silencio y paisaje construyen la estadía, hasta generar esa extraña sensación de estar lejos y, al mismo tiempo, haber vuelto a casa.', IG['16'])),
      block('Imagen', thumbs([('web_rilan_51', 'Sala con estufa · galería')]) + '<p>Lleva un velo oscuro para que el texto se lea sin perder el fuego.</p>'),
      block('Letra', '<p>El título va en Marcellus en mayúsculas y la segunda frase, en Newsreader itálica, como una voz más baja.</p>'),
      block('Por qué aquí', '<p>Cierra Refuge con la idea de "haber vuelto a casa", la misma que repiten los huéspedes en Booking.</p>'),
  ])

S('Rucalaf', 'Donde el mar encuentra la mesa',
  'La cocina se presenta como una "masa" de fotos: tres columnas que se desplazan a distinta velocidad mientras el texto queda fijo a la izquierda.',
  'd-kitchen', 'm-kitchen', [
      block('Textos', quote('Una cocina profundamente arraigada al lugar, donde el mar y su herencia encuentran su camino hasta la mesa.', IG['09']) + quote('Una recolección de la isla, para ti.', IG['14']) + '<p><b>Dato práctico (Booking):</b> solo cena, que se coordina cada día hasta las 15:30. Algunos huéspedes no lo sabían al llegar, y lo comentaron en Booking.</p>'),
      block('Imágenes', thumbs([('ig_2026-09-10_DdHRZK0RRZJ', 'Mariscos · ' + IG['09']), ('web_rilan_32', 'Ostras · galería'), ('web_rilan_39', 'Fogón · galería'), ('web_rilan_17', 'Cóctel · galería')])),
      block('Composición', '<p>Nueve platos en tres columnas desfasadas. Al pasar el cursor por uno, los demás se oscurecen. La coctelería sigue en una sección clara con dos fotos de distinto tamaño.</p>'),
      block('Color', chips([('Noche', '#121311'), ('Fuego', '#B07436')]) + '<p>El acento cobre marca solo la nota práctica.</p>'),
  ], desk2='d-cocktail')

S('La cava', 'Una cava especial por su diseño',
  'La cava habla por boca de sus huéspedes, en tres idiomas: español, alemán e inglés, tal como lo escribieron.',
  'd-cava', 'm-cava', [
      block('Textos', quote('…una cava especial por su diseño muy particular…', 'Gonzalez · Chile · Booking.com') + quote('Die Auswahl an Weinen ist enorm.', 'Beatrice · Suiza · Booking.com') + quote('…the fantastic wine cellar and the fantastic hosts.', 'Veronica · Suiza · Booking.com')),
      block('Imagen', thumbs([('web_rilan_11', 'La cava · galería')]) + '<p>Los muros curvos de nichos llenan la pantalla. La foto se acerca lentamente al bajar.</p>'),
      block('Por qué reseñas', '<p>Ustedes aún no publican sobre la cava, pero sus huéspedes sí. "Hotel & Cava" fue parte del nombre anterior del hotel.</p>'),
      block('Letra', '<p>LA CAVA en Marcellus, al tamaño de las palabras de capítulo. Las citas, en Newsreader itálica.</p>'),
  ])

S('The Long Table', 'Una mesa larga, abierta a todos',
  'El evento del sábado 10 de octubre, compuesto igual que su pieza gráfica: fondo piedra, título en mayúsculas, filas separadas por líneas finas.',
  'd-table', 'm-table', [
      block('Textos', quote('Una mesa larga, abierta a todos. Una forma de encontrarse con Chiloé desde la cocina, el territorio y el tiempo.', IG['17']) + quote('Íntima, sin apuros y con todos los sentidos', 'Pieza gráfica · The Long Table')),
      block('Imágenes', thumbs([('ig_2026-10-03_DeCNBLVEfM9_04', 'Mesa con velas · Instagram, 3 oct 2026'), ('ig_2026-10-03_DeCNBLVEfM9_05', 'Mesa frente al mar'), ('ig_2026-10-03_DeCNBLVEfM9_03', 'Pieza original')])),
      block('Datos', '<p>13:00 h · $70.000 por persona · 15 % de descuento en alojamiento esa noche · a cargo de La Lancha Chilota. El botón lleva al WhatsApp del post.</p>'),
      block('Detalle', '<p>La sección se oculta sola después del 10 de octubre, para que el sitio nunca muestre un evento pasado. Va solo en español porque así se publicó.</p>'),
  ])

S('Heritage', 'La madera atraviesa la historia',
  'El último capítulo: la iglesia en la niebla y el oficio de la madera. La sección clara combina tres detalles (repisas, cestería y velas) como un pequeño museo.',
  'd-heritage', 'm-heritage-text', [
      block('Textos', quote('Patrimonio Mundial de la UNESCO, las iglesias de Chiloé son testimonio de una arquitectura única, nacida de la madera, el oficio y el tiempo.', IG['04']) + quote('La madera atraviesa la historia del archipiélago. Fue casa, iglesia, bote, herramienta, calor y refugio.', IG['10'])),
      block('Imágenes', thumbs([('ig_2026-09-03_Dc00-W6RwgS', 'Iglesia · ' + IG['04']), ('web_rilan_15', 'Repisas · galería'), ('web_rilan_10', 'Cestería · galería'), ('ig_2026-10-03_DeCNBLVEfM9_09', 'Velas · Instagram, 3 oct 2026')])),
      block('Composición', '<p>Tres imágenes de tamaños distintos a alturas distintas, para que se recorran con la mirada como objetos en una sala.</p>'),
      block('Por qué al final', '<p>Lo patrimonial da profundidad a todo lo anterior: la madera del hotel es la misma de las iglesias.</p>'),
  ], desk2='d-heritage-text')

S('Arquitectura', 'Los volúmenes del hotel',
  'Una cinta de seis fotos de arquitectura que se desliza lateralmente al bajar: fachadas, pasarelas, patio y quincho.',
  'd-arch', 'm-arch', [
      block('Imágenes', thumbs([('web_rilan_01', 'Fachada · galería'), ('web_rilan_55', 'Noche · galería'), ('web_rilan_34', 'Pasarelas · galería'), ('ig_2026-09-08_DdB-aHPxysK', 'Patio · ' + IG['07'])])),
      block('Por qué', '<p>Las reseñas lo llaman "bijou arquitectónico" y "design hotel". Esta cinta lo muestra sin decirlo y sirve de puente entre el relato y las voces de los huéspedes.</p>'),
      block('Composición', '<p>Una sola fila a lo ancho, con la misma altura y anchos distintos. Al pasar el cursor, la foto se acerca suavemente.</p>'),
  ])

S('Mónica y Rodrigo', 'Lo que dicen sus huéspedes',
  'La sección lleva sus nombres porque son lo que más se repite en las 99 reseñas. Es un carrusel internacional con 11 citas literales, cada una en su idioma.',
  'd-hosts', 'm-hosts', [
      block('Citas', quote('Una de las mayores joyas de este hotel son sus dueños, Mónica y Rodrigo.', 'Velasquez · Chile') + quote('Un écrin de sérénité et de confort', 'Patrice · Francia') + quote('Das Hotel ist architektonisch ein Highlight.', 'Beatrice · Suiza') + quote('It was the most peaceful hotel stay we have ever experienced.', 'Cezanne · Estados Unidos')),
      block('Dato', '<p><b>9,5 · Excepcional · 99 comentarios</b>, tal como lo muestra Booking.com.</p>'),
      block('Por qué así', '<p>Español, inglés, francés y alemán, sin traducir: así se ve quién llega a RILÁN. Las citas se acortaron solo con […], sin cambiar palabras.</p>'),
      block('Interacción', '<p>Avanza solo cada pocos segundos y se detiene al pasar el cursor. Se puede arrastrar y tiene contador y flechas.</p>'),
  ])

S('Cómo llegar', 'El punto exacto del hotel',
  'Un mapa en gris que se puede mover y acercar. El cuadrado cobre pulsante queda anclado a las coordenadas del hotel, se mueva como se mueva el mapa.',
  'd-arrive-prod', None, [
      block('Datos', '<p>La Estancia s/n, Península de Rilán · Castro 8 km · Iglesia de Rilán 11 km · Aeropuerto Mocopulli 28–37 km · traslado al aeropuerto disponible. Todo viene de Booking.</p>'),
      block('Por qué', '<p>La crítica más repetida en Booking es que cuesta llegar: el GPS falla y faltan letreros. Por eso hay un mapa preciso, con las mismas coordenadas de sus destacadas, y un enlace directo a Google Maps.</p>'),
      block('Interacción', '<p>La rueda del mouse sigue bajando la página; el zoom se hace con + y −. En celular, el mapa se mueve con dos dedos. El botón "Volver al hotel" recentra.</p>'),
      block('Color', chips([('Niebla', '#EAE9E3'), ('Fuego', '#B07436')]) + '<p>El mapa va en escala de grises para que solo el hotel tenga color.</p>'),
  ], nota='Captura del sitio publicado, con el mapa real.')

S('Reservar', 'Deja que el tiempo pierda su medida',
  'El cierre es una invitación, no un formulario: una frase suya, dos caminos para reservar y las normas claras. Después, el pie con el nombre a gran escala.',
  'd-book', 'm-book', [
      block('Textos', quote('Deja que el tiempo pierda su medida en RILÁN.', IG['03']) + quote('Bienvenidos al misticismo del archipiélago.', IG['03'] + ' · pie de página')),
      block('Caminos', '<p><b>Reservar por WhatsApp</b> (+56 9 9292 8899, el número del post del 3 oct) y <b>Booking.com</b>. Reservar directo es lo primero.</p>'),
      block('Normas (Booking)', '<p>Check-in de 14:00 a 22:00 · check-out de 8:30 a 12:00 · solo adultos · sin mascotas · calefacción y ventilador, sin aire acondicionado. Se explicitan porque las reseñas mostraron dudas.</p>'),
      block('Lo que no se publicó', '<p>La promoción de "3 noches + 1" era de septiembre y ya venció, así que no aparece.</p>'),
  ], desk2='d-foot')

# Lámina de detalles transversales
nx()
L.append(lamina_libre(n,
    f'''<p class="lab">Menú a pantalla completa</p><img class="desk" src="{shot('d-menu')}" alt="" style="width:84%">
    <p class="lab" style="margin-top:.16in">El mismo sitio en celular</p>
    <div class="mrow">{''.join(f'<img src="{shot(s, 360)}" alt="">' for s in ['m-hero', 'm-territory', 'm-rooms', 'm-cava', 'm-hosts'])}</div>''',
    f'''<p class="kick">Detalles en todo el sitio</p>
    <h2>Lo que no se ve, pero se siente</h2>
    <div class="grid">
      {block('Menú', '<p>Los capítulos se muestran en grande y al pasar sobre cada uno aparece su foto. Se cierra con la tecla Esc o con la X.</p>')}
      {block('Dos idiomas', '<p>Un selector ES / EN. Se traduce todo lo que guía la visita (menús, botones, datos y descripciones de imágenes), y lo publicado en un solo idioma se muestra como fue escrito.</p>')}
      {block('Movimiento con calma', '<p>Todo arranca rápido y frena suave. Quien tenga activada la opción de "reducir movimiento" en su equipo ve el sitio completo y quieto.</p>')}
      {block('Celular primero', '<p>Cada sección tiene su versión para teléfono: galerías que se deslizan con el dedo, textos a una columna y el mapa con dos dedos.</p>')}
      {block('Sin saltos', '<p>La página no "brinca" mientras carga ni al bajar. Se revisó en cuatro tamaños de pantalla, del celular a un monitor grande.</p>')}
      {block('Accesible', '<p>Textos que se leen bien, recorrido completo con el teclado y todas las imágenes descritas en ambos idiomas, para quienes usan lectores de pantalla.</p>')}
    </div>'''))

# Cierre
nx()
L.append(lamina_libre(n,
    f'<img class="bleed" src="{raw("ig_2026-09-03_Dc00-W6RwgS")}" alt="">',
    f'''<div class="center close">
      {MARK}
      <p class="kick">Lo que sigue</p>
      <h2>Hacerlo suyo</h2>
      <p class="lead">Este sitio se hizo solo con lo que ya estaba publicado. Con un par de conversaciones podría ir mucho más lejos:</p>
      <ul class="next">
        <li>Fotografía propia de cada habitación, de la cava y de ustedes dos</li>
        <li>Los contenidos que ustedes quieran contar, con su voz</li>
        <li>Dominio propio .cl y alojamiento a nombre de RILÁN</li>
        <li>Reservas directas y la coordinación diaria de las cenas, más simples</li>
      </ul>
      <p class="invite">Cuando quieran, lo conversamos.</p>
      <p class="who">Pablo Figueroa G.</p>
      <p class="role">Director de estudio</p>
      <p class="contact"><a href="mailto:pablo@bergerac.cl">pablo@bergerac.cl</a> · <a href="tel:+56975892096">+56 9 7589 2096</a></p>
      <p class="link"><a href="https://bergerac.cl">Bergerac.cl</a></p>
      <p class="coords">{COORDS}</p>
    </div>''', left_cls='full'))

# ---------------------------------------------------------------- documento
CSS = f'''
@font-face{{font-family:"Marcellus";src:url({font("marcellus-latin-400-normal")}) format("woff2")}}
@font-face{{font-family:"Newsreader";font-weight:300;src:url({font("newsreader-latin-300-normal")}) format("woff2")}}
@font-face{{font-family:"Newsreader";font-weight:400;src:url({font("newsreader-latin-400-normal")}) format("woff2")}}
@font-face{{font-family:"Newsreader";font-weight:300;font-style:italic;src:url({font("newsreader-latin-300-italic")}) format("woff2")}}
@page{{size:13in 8.5in;margin:0}}
:root{{--niebla:#EAE9E3;--piedra:#544F4C;--ceniza:#847F7B;--bruma:#CCCBC4;--noche:#121311;--fuego:#B07436}}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{background:#8a8682}}
body{{font-family:"Newsreader",Georgia,serif;color:var(--piedra);-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.lam{{width:13in;height:8.5in;display:grid;grid-template-columns:6.5in 6.5in;overflow:hidden;margin:0 auto .3in;background:var(--niebla);page-break-after:always;break-after:page;position:relative}}
@media print{{html,body{{background:none}}.lam{{margin:0}}}}
.L{{background:var(--piedra);color:var(--niebla);padding:.42in .4in .38in;display:flex;flex-direction:column;gap:.12in;overflow:hidden}}
.L.full{{padding:0}}
.bleed{{width:100%;height:100%;object-fit:cover;display:block}}
.R{{position:relative;padding:.5in .55in .7in;display:flex;flex-direction:column;overflow:hidden}}
.lab{{font-family:"Marcellus";font-size:6.6pt;letter-spacing:.24em;text-transform:uppercase;opacity:.8}}
.desk{{width:100%;display:block;outline:.5pt solid rgba(234,233,227,.22)}}
.desk2{{width:100%;display:block;outline:.5pt solid rgba(234,233,227,.22)}}
.L.two .desk,.L.two .desk2{{width:88%}}
.L.two .Lrow{{margin-top:0}}
.L.two .rec{{columns:4;font-size:5.8pt;line-height:1.7}}
.Lrow{{display:flex;gap:.22in;align-items:flex-start;margin-top:.04in;min-height:0;flex:1}}
.mobw{{display:flex;flex-direction:column;gap:.08in}}
.mob{{width:1.35in;display:block;outline:.5pt solid rgba(234,233,227,.22)}}
.Linfo{{flex:1;display:flex;flex-direction:column;gap:.08in}}
.rec{{list-style:none;columns:2;column-gap:.14in;font-family:"Marcellus";font-size:6.4pt;letter-spacing:.14em;text-transform:uppercase;line-height:1.85}}
.rec li{{opacity:.42;break-inside:avoid}}
.rec li.on{{opacity:1;color:#fff}}
.rec li.on::before{{content:"";display:inline-block;width:5pt;height:5pt;background:var(--fuego);margin-right:4pt;vertical-align:1pt}}
.lnote{{font-size:7.6pt;font-style:italic;opacity:.75;line-height:1.4;margin-top:.04in}}
.kick{{font-family:"Marcellus";font-size:7pt;letter-spacing:.28em;text-transform:uppercase;color:var(--ceniza);margin-bottom:.12in}}
h1{{font-family:"Marcellus";font-weight:400;font-size:64pt;letter-spacing:.14em;margin-right:-.14em;line-height:1;color:var(--piedra)}}
h2{{font-family:"Marcellus";font-weight:400;font-size:21pt;line-height:1.12;letter-spacing:.05em;text-transform:uppercase;margin-bottom:.14in;color:var(--piedra)}}
.lead{{font-size:12.6pt;font-weight:300;line-height:1.42;margin-bottom:.22in;max-width:5.4in}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:.2in .3in;align-content:start}}
.bk h4{{font-family:"Marcellus";font-weight:400;font-size:7.2pt;letter-spacing:.22em;text-transform:uppercase;color:var(--piedra);padding-bottom:4pt;border-bottom:.5pt solid var(--bruma);margin-bottom:6pt}}
.bk p{{font-size:9.4pt;line-height:1.48;margin-bottom:5pt}}
.bk p.small{{font-size:7.4pt;color:var(--ceniza)}}
.bk.wide{{grid-column:1/-1}}
.q{{margin:0 0 6pt}}
.q p{{font-size:9.8pt;font-style:italic;font-weight:300;line-height:1.38;margin-bottom:1.5pt}}
.q p::before{{content:"“"}}.q p::after{{content:"”"}}
.q cite{{display:block;font-style:normal;font-family:"Marcellus";font-size:6.3pt;letter-spacing:.16em;text-transform:uppercase;color:var(--ceniza)}}
.ths{{display:flex;gap:5pt;flex-wrap:wrap;margin-bottom:4pt}}
.th{{width:calc(25% - 4pt);min-width:.62in}}
.ths .th:only-child{{width:1.3in}}
.th img{{width:100%;height:.95in;object-fit:cover;display:block}}
.th figcaption{{font-size:6.2pt;line-height:1.25;color:var(--ceniza);margin-top:2pt}}
.chips{{display:flex;flex-wrap:wrap;gap:4pt 8pt;margin-bottom:4pt}}
.chip{{display:inline-flex;align-items:center;gap:4pt;font-size:7pt}}
.chip i{{width:11pt;height:11pt;display:inline-block;outline:.5pt solid rgba(84,79,76,.3)}}
.chip b{{font-weight:400;font-family:"Marcellus";letter-spacing:.08em;text-transform:uppercase;font-size:6.2pt}}
.tl{{font-family:"Marcellus";font-size:7pt;letter-spacing:.18em}}
.pf{{position:absolute;left:.55in;right:.55in;bottom:.3in;display:flex;justify-content:space-between;font-family:"Marcellus";font-size:6pt;letter-spacing:.22em;text-transform:uppercase;color:var(--ceniza);border-top:.5pt solid var(--bruma);padding-top:6pt}}
.mk{{width:.36in;fill:var(--piedra);display:block}}
/* portada */
.cover .R.center{{justify-content:center;align-items:center;text-align:center;gap:.16in}}
.cover .mk{{width:.5in;margin-bottom:.1in}}
.cover .sub{{font-family:"Marcellus";font-size:10pt;letter-spacing:.3em;text-transform:uppercase}}
.cover .for{{font-size:13pt;font-style:italic;font-weight:300;margin-top:.25in}}
.cover .meta{{font-size:9pt;color:var(--ceniza)}}
.coords{{font-family:"Marcellus";font-size:7pt;letter-spacing:.26em;color:var(--ceniza);margin-top:.3in}}
/* carta */
.letter p{{font-size:10.4pt;line-height:1.55;margin-bottom:8pt;max-width:5.2in}}
.letter .sign,.sign{{font-style:italic;margin-top:6pt}}
/* fuentes */
.igrid{{display:grid;grid-template-columns:repeat(5,1fr);gap:4pt}}
.igrid img{{width:100%;aspect-ratio:1;object-fit:cover;display:block}}
.dgrid{{display:grid;grid-template-columns:repeat(4,1fr);gap:4pt}}
.dgrid img{{width:100%;aspect-ratio:9/16;object-fit:cover;display:block}}
.piece{{width:100%;display:block;max-height:3.9in;object-fit:cover}}
.pair{{display:grid;grid-template-columns:1fr .56fr;gap:6pt;margin-top:6pt}}
.pair img{{width:100%;height:2.3in;object-fit:cover;display:block}}
.spec{{background:var(--niebla);color:var(--piedra);padding:.2in .24in}}
.sp1{{font-family:"Marcellus";font-size:26pt;letter-spacing:.04em}}
.sp2{{font-size:13pt;font-weight:300;line-height:1.35;margin-top:.12in}}
.sp3{{font-family:"Marcellus";font-size:8pt;letter-spacing:.28em;margin-top:.14in}}
.spec .cap{{font-family:"Marcellus";font-size:5.8pt;letter-spacing:.18em;text-transform:uppercase;color:var(--ceniza);margin-top:3pt}}
.pgrid{{display:grid;grid-template-columns:repeat(3,1fr);gap:4pt}}
.pgrid img{{width:100%;aspect-ratio:1;object-fit:cover;display:block}}
.swatches{{display:grid;grid-template-columns:repeat(3,1fr);gap:4pt;margin-top:.12in}}
.swatches span{{height:.78in;padding:6pt;font-family:"Marcellus";font-size:6.4pt;letter-spacing:.16em;text-transform:uppercase;color:var(--niebla);display:flex;align-items:flex-end;line-height:1.5;outline:.5pt solid rgba(234,233,227,.2)}}
.logos{{display:grid;grid-template-columns:1fr 1fr;gap:6pt;padding:.42in .4in;height:100%;align-content:center}}
.lg{{display:grid;place-items:center;height:1.75in;padding:.25in}}
.lg.light{{background:var(--niebla)}}.lg.dark{{background:var(--noche)}}
.lg.wide{{grid-column:1/-1;height:1.2in}}
.lg img{{max-width:100%;max-height:1.15in;width:auto;height:auto;display:block}}
.lg.wide img{{max-height:.6in}}
.L.full .logos{{padding:.42in .4in}}
.strip{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:6pt}}
.strip figure img{{width:100%;aspect-ratio:16/10;object-fit:cover;display:block}}
.strip figcaption{{font-family:"Marcellus";font-size:5.8pt;letter-spacing:.18em;text-transform:uppercase;margin-top:3pt;opacity:.8}}
.mrow{{display:grid;grid-template-columns:repeat(5,1fr);gap:5pt}}
.mrow img{{width:100%;display:block;outline:.5pt solid rgba(234,233,227,.22)}}
.close{{display:flex;flex-direction:column;align-items:flex-start;justify-content:center;height:100%;gap:.1in}}
.close .mk{{margin-bottom:.14in}}
.next{{list-style:none;margin:.04in 0 .2in}}
.next li{{font-size:11pt;font-weight:300;line-height:1.5;padding:5pt 0;border-bottom:.5pt solid var(--bruma)}}
.close a{{color:inherit;text-decoration:none}}
.close .invite{{font-size:13pt;font-style:italic;font-weight:300;margin-bottom:.06in}}
.close .who{{font-family:"Marcellus";font-size:9pt;letter-spacing:.24em;text-transform:uppercase;color:var(--piedra)}}
.close .role{{font-size:9.4pt;margin-top:-4pt}}
.close .contact{{font-size:8.6pt;color:var(--ceniza)}}
.close .link{{font-family:"Marcellus";font-size:13pt;letter-spacing:.24em;text-transform:uppercase;color:var(--fuego);margin-top:.12in}}
.close .coords{{margin-top:.14in}}
'''

DOC = f'''<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>RILÁN · Decisiones de diseño del sitio web</title>
<style>{CSS}</style></head>
<body>
{''.join(L)}
</body></html>'''

out = D / 'rilan-dossier-diseno.html'
out.write_text(DOC, encoding='utf-8')
print(out, round(out.stat().st_size / 1e6, 1), 'MB ·', n, 'láminas')
