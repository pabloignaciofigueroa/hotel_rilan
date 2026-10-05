# RILÁN — sitio web

Sitio estático (HTML, CSS y JS) del hotel RILÁN, en la península de Rilán, Chiloé.
Publicado con GitHub Pages: https://pabloignaciofigueroa.github.io/hotel_rilan/

## Estructura
| Ruta | Contenido |
|---|---|
| `index.html` | Página final, generada; no se edita a mano |
| `src/index.html` | Plantilla editable. Las imágenes se marcan como `<x-img id="…">` |
| `tools/build.py` | Genera `index.html`: arma srcset, ancho y alto, y placeholder borroso |
| `css/main.css` | Estilos y tokens de marca |
| `js/main.js` | Movimiento: GSAP + ScrollTrigger, Lenis, Swiper |
| `vendor/` | Librerías incluidas en el repositorio (sin CDN) |
| `assets/img`, `assets/video`, `assets/fonts` | Medios optimizados y fuentes Marcellus y Newsreader |
| `brand/` | Logos SVG/PNG/favicons, paleta, tipografía, dirección de arte |
| `content/` | Textos fuente (Instagram, Booking), voz de marca y guion `copy.md` con la fuente de cada texto |
| `_plan/` | Plan de 20 fases y bitácora |

## Editar
1. Cambia `src/index.html`, `css/main.css` o `js/main.js`.
2. Ejecuta `python3 tools/build.py`.
3. Sube los cambios a `main`. GitHub Pages publica solo.

Para agregar una imagen nueva hay que regenerar sus versiones WebP y registrarla en `assets/img/meta.json`; el script de la fase 07 está en el historial.

## Reglas de contenido
Todo texto visible sale de lo que RILÁN ya publicó o de un dato verificable. `content/copy.md` registra la fuente de cada uno. Las reseñas son citas literales de Booking.com.

## Notas
- The Long Table se oculta sola después del 10 de octubre de 2026.
- Idioma ES/EN con selector; la elección se recuerda en el navegador.
- Con `prefers-reduced-motion` el sitio no usa scroll suave, fijaciones (pins) ni parallax.
