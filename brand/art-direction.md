# Dirección de arte y movimiento

## Lectura del encargo
Sitio para RILÁN, hotel boutique de 8 habitaciones en la península de Rilán, Chiloé. Va dirigido a parejas que buscan silencio, paisaje y cocina local; 83 de las 99 reseñas de Booking son de parejas. La tarea del sitio es que el visitante sienta el ritmo del lugar y reserve directo.

## El mundo visual ya existe: las historias destacadas
El sistema de la marca se ve en Instagram:
- Foto a sangre.
- Isotipo Λ. blanco al centro.
- Palabra pilar en mayúsculas espaciadas.
- Coordenadas al pie.

El sitio lleva ese sistema a pantalla completa. **Cada capítulo (TERRITORY, MYSTICISM, REFUGE, HERITAGE) se abre como una de sus portadas.** Lo que hace distinto al sitio es el uso de su propia gramática, no un adorno inventado.

## El momento memorable (uno solo)
**La ventana Λ.** Después de la portada, el isotipo se convierte en una ventana con forma de A-frame (que es además la forma de las casas de RILÁN) que deja ver el video de bienvenida. Con el scroll, la ventana crece hasta llenar la pantalla y aparecen, una a una, "La madera, el fuego, el patrimonio, el silencio."

Es un clip-path escalado con GSAP ScrollTrigger y scrub.

## Ritmo de página
```
[ HERO foto nocturna · RILÁN · bio · coords ]           oscuro, a sangre
[ VENTANA Λ → video a pantalla completa ]                pin + scrub
[ Bienvenidos a RILÁN · párrafo ]                        niebla, mucho aire, centrado estrecho
[ TERRITORY portada ]                                    a sangre
[ texto izq. + galería horizontal arrastrable → ]        pin horizontal (escritorio), swipe (móvil)
[ MYSTICISM portada ] [ silencio ] [ ballena + sonido ]  a sangre / niebla / oscuro
[ REFUGE portada ] [ texto ] [ slider habitaciones ]     ...
[ living con fuego a sangre + cita IG-16 ]               parallax
[ RILÁN by Rucalaf: masa de imágenes a dos velocidades ] oscuro
[ La cava ] [ THE LONG TABLE (piedra, como la pieza) ]
[ HERITAGE portada ] [ texto + 3 detalles ]
[ Mónica y Rodrigo: reseñas en carrusel lento ]          niebla
[ Cómo llegar: mapa + datos ] [ Reservar ] [ pie ]
```
Los textos de capítulo van alineados a la izquierda, con una medida de 34 a 38 ch, y el resto de la pantalla queda vacío como aire. Las portadas van centradas, como las destacadas.

## Movimiento
- **Curvas**:
  - `--ease-out: cubic-bezier(.16,1,.3,1)` (expo-out): arranque rápido y frenado suave.
  - `--ease-io: cubic-bezier(.76,0,.24,1)`: cortinas y transiciones.
- **Duraciones**: 0,25 s en micro-interacciones, 0,7 s en revelados y 1,1 s en cortinas.
- **Revelados de texto**: líneas que suben desde una máscara (overflow hidden), con un desfase de 0,06 s.
- **Imágenes**: entran con clip-path de abajo hacia arriba y escala de 1,15 a 1. Dentro de su marco tienen parallax de ±8 %.
- **Masas**: en la cocina, dos columnas de fotos se desplazan a velocidades distintas (scrub).
- **Micro-interacciones**:
  - Botones magnéticos (desplazamiento máximo de 6 px).
  - Subrayado que crece desde la izquierda.
  - En los sliders, el cursor muestra una etiqueta "Arrastrar" sin ocultar el cursor nativo.
  - El contador del slider cambia con la diapositiva.
- **Scroll suave**: Lenis (lerp 0.1), sincronizado con ScrollTrigger.
- `prefers-reduced-motion`: sin Lenis, sin pins y sin parallax. Todo el contenido queda visible y estático.

## Superficies
- Radio 0 en todo: la marca es arquitectura de madera y líneas rectas.
- Solo las líneas finas de las piezas (1 px `--bruma`), y únicamente donde la pieza original las usa (datos del evento y normas).
- Velo de `--noche` sobre las fotos con texto.
- Grano fino fijo con pointer-events none.
- Selección de texto en `--fuego` sobre `--niebla`.
