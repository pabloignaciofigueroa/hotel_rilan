# RILÁN — Plan de construcción del sitio (20 fases)

Encargo de Pablo Figueroa (5 oct 2026). Sitio estático HTML + CSS + JS, muy visual, que se sienta hecho por RILÁN.

## Reglas que no se negocian
- **Ghostwriter de la marca**: todo título y texto sale de lo que RILÁN ya publicó (Instagram, destacadas, web actual, ficha de Booking). Cada texto del sitio lleva su fuente en `content/copy.md`. Nada de frases inventadas ni empalagosas. Si hace falta un texto de conexión, se arma con palabras de la marca y se marca como `[conector]`.
- **Aire**: secciones a pantalla completa con fotos o video de fondo de borde a borde, nada encajonado, márgenes generosos.
- **Motion**: arranque y cierre suaves (custom cubic-bezier / expo-out), ejecución rápida (200–700 ms). Revelados con máscara, parallax, sliders, cards, swipe en móvil, masas (bloques que se desplazan con inercia), micro-interacciones. Respetar `prefers-reduced-motion`.
- Solo material real de RILÁN: fotos, videos, logos y reseñas reales (citas literales).
- Referencias de diseño: skill `frontend-design`; además las guías "impeccable" y "taste" si se pueden obtener de GitHub (si no, se aplican sus principios conocidos: jerarquía tipográfica, ritmo, contraste, cero relleno genérico).
- Assets fuente: `C:\Users\pfigug\Desktop\hotel_rilan` (01_imagenes, 02_videos, 03_textos).
- Rama de trabajo: `dev`. `main` se publica solo en la Fase 20.

## Las 20 fases
| # | Fase | Entregable |
|---|------|-----------|
| 01 | Arranque e inventario | Estructura del repo, assets copiados desde el PC a `assets/raw/`, inventario |
| 02 | Investigación de voz | `content/brand-voice.md`: corpus literal de títulos, frases y hashtags de IG, destacadas, web actual y Booking, con fuente |
| 03 | Tipografías | `brand/typography.md`: fuentes reales detectadas (estilos computados de rilanhotel.com y piezas gráficas), equivalentes web licenciables, escala tipográfica |
| 04 | Paleta de color | `brand/palette.md` + `css/tokens.css`: colores extraídos (k-means) de fotos y piezas, roles, contraste AA |
| 05 | Logos multi-escala | `brand/logo/`: SVG vectorizados (completo, isotipo, horizontal, claro/oscuro, mono), favicons 16–512, OG image |
| 06 | Guion de textos | `content/copy.md`: arquitectura del sitio y texto por sección, ES/EN, solo palabras de la marca con su fuente |
| 07 | Curaduría de medios | Selección por sección, recortes, WebP/AVIF responsive + LQIP, videos comprimidos mp4/webm + posters |
| 08 | Dirección de arte y motion | `brand/art-direction.md`: moodboard, wireframes, sistema de movimiento (curvas, duraciones, coreografía) |
| 09 | Base técnica | `index.html` semántico, CSS (tokens, reset, grid fluido), JS modular, Lenis + GSAP/ScrollTrigger + Swiper vendorizados |
| 10 | Hero | Video a pantalla completa, revelado del logo, titular con máscara, indicador de scroll |
| 11 | Territory + Mysticism | Secciones a sangre con parallax, revelados de texto, galerías de las destacadas |
| 12 | Habitaciones | Slider/cards con swipe, detalle por habitación |
| 13 | Cocina Rucalaf + La cava | Galería con scroll horizontal, cards con hover, masas en movimiento |
| 14 | Refuge + Heritage + Mónica y Rodrigo | Historia, detalles artísticos, cita de los anfitriones |
| 15 | Reseñas, cómo llegar, reserva, footer | Reseñas reales en carrusel, mapa, CTA de reserva directa, contacto, redes |
| 16 | Micro-interacciones | Preloader, navegación, cursor, botones magnéticos, transiciones, hover states |
| 17 | Responsive + accesibilidad | Móvil/tablet, swipe táctil, teclado, alt texts, reduced motion |
| 18 | Performance + QA visual | Carga diferida, Lighthouse, capturas con Playwright en 3 tamaños, corrección de errores |
| 19 | Auditoría de voz y pulido | Revisión independiente: cada texto con fuente, coherencia visual, detalles finos |
| 20 | Publicación + aviso | Merge a `main`, push, GitHub Pages, correo a pabloignaciofigueroa@gmail.com |
