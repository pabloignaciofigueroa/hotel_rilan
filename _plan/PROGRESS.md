# Progreso

estado: idle
fase_actual: -
inicio_ejecucion: -
ultima_fase_completada: 20

## Bitácora
- 2026-10-05 17:30 — Plan creado. Próxima: Fase 01.
- 2026-10-05 17:40 — F01 lista: 111 archivos (100 fotos, 2 videos + portadas, 7 textos) en assets/raw (fuera de git; la fuente vive en el PC). Textos copiados a content/.
- 17:55 — F02 voz (content/brand-voice.md) · F03 tipografía Marcellus + Newsreader (brand/typography.md, assets/fonts) · F04 paleta k-means (brand/palette.md) · F05 logos SVG/PNG/favicon (brand/logo). rilanhotel.com fuera de línea; fuentes identificadas por comparación visual.
- 18:10 — F06 guion content/copy.md (todo con fuente) · F07 73 imágenes WebP 800/1800 + LQIP, 2 videos comprimidos · F08 brand/art-direction.md (ventana Λ como momento único; guías impeccable + taste aplicadas).
- 18:35 — F09–F15 sitio construido: index.html (generado desde src/ con tools/build.py), css/main.css, js/main.js. Hero, ventana Λ, 4 capítulos, habitaciones (Swiper), cocina (masas), cava, The Long Table, reseñas, cómo llegar, reservar, pie. Videos WebM + MP4.
- 18:50 — F16 micro-interacciones (menú con imágenes, etiqueta Arrastrar, botones magnéticos, hover en masas, barras de sonido) · F17 responsive 390/1280/1440/1920, foco visible, movimiento reducido verificado, acento de RILÁN corregido.
- 19:05 — F18 performance/QA: Lighthouse (servidor local sin gzip) Perf 75–82 · A11y 96 · BP 100 · SEO 100; CLS 0.08. Swiper diferido, CSS no bloqueante, preload responsivo, imagen OG, sin errores de consola. Capturas en 390/1280/1440/1920.
- 19:25 — F19 auditoría independiente (agente separado). Corregido: desborde horizontal en The Long Table (blocker), citas de reseñas literales (Gonzalez con elipsis, Mariana con su ortografía), The Long Table solo en ES, legibilidad de las citas de la cava, distancia al aeropuerto 28–37 km, nota de llegada reducida al dato de Booking. README.
- 19:35 — F20 main publicado en GitHub; correo enviado a pabloignaciofigueroa@gmail.com. Pendiente manual: activar GitHub Pages y dejar main como rama por defecto (el entorno no permite cambiar la configuración del repo).
- 22:55 — Auditoría post-deploy. Galería horizontal con sticky en vez de pin (CLS de 1,96 a 0,000). Secciones a pantalla completa en 100svh. Idiomas separados (reseñas, cava, bio, Mysticism, alt y aria bilingües, español por defecto). Corregido: fuente fallida bloqueaba el sitio, sticky de la cocina, desborde de la grilla de platos, salto al inicio al cruzar 900 px, listener duplicado, carrera y foco del menú, salto al contenido, autoplay del slider oculto, póster diferido. Verificado con pruebas automáticas.
- 23:10 — Según indicación de Pablo, el contenido de origen vuelve a su idioma original: reseñas internacionales (FR, DE, EN, ES) en un solo carrusel, cava en tres idiomas, bio de IG y Mysticism en inglés en ambas versiones. Solo se traduce la interfaz.
