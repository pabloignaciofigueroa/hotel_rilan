# Progreso

estado: idle
fase_actual: 19
inicio_ejecucion: -
ultima_fase_completada: 18

## Bitácora
- 2026-10-05 17:30 — Plan creado. Próxima: Fase 01.
- 2026-10-05 17:40 — F01 lista: 111 archivos (100 fotos, 2 videos + portadas, 7 textos) en assets/raw (fuera de git; la fuente vive en el PC). Textos copiados a content/.
- 17:55 — F02 voz (content/brand-voice.md) · F03 tipografía Marcellus + Newsreader (brand/typography.md, assets/fonts) · F04 paleta k-means (brand/palette.md) · F05 logos SVG/PNG/favicon (brand/logo). rilanhotel.com fuera de línea; fuentes identificadas por comparación visual.
- 18:10 — F06 guion content/copy.md (todo con fuente) · F07 73 imágenes WebP 800/1800 + LQIP, 2 videos comprimidos · F08 brand/art-direction.md (ventana Λ como momento único; guías impeccable + taste aplicadas).
- 18:35 — F09–F15 sitio construido: index.html (generado desde src/ con tools/build.py), css/main.css, js/main.js. Hero, ventana Λ, 4 capítulos, habitaciones (Swiper), cocina (masas), cava, The Long Table, reseñas, cómo llegar, reservar, pie. Videos WebM + MP4.
- 18:50 — F16 micro-interacciones (menú con imágenes, etiqueta Arrastrar, botones magnéticos, hover en masas, barras de sonido) · F17 responsive 390/1280/1440/1920, foco visible, movimiento reducido verificado, acento de RILÁN corregido.
- 19:05 — F18 performance/QA: Lighthouse (servidor local sin gzip) Perf 75–82 · A11y 96 · BP 100 · SEO 100; CLS 0.08. Swiper diferido, CSS no bloqueante, preload responsivo, imagen OG, sin errores de consola. Capturas en 390/1280/1440/1920.
