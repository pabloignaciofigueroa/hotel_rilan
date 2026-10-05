# Tipografía RILÁN

## Lo que usa la marca
Revisé las piezas de THE LONG TABLE, la portada MYSTICISM y las portadas de las destacadas en Instagram. Usan dos familias:

1. **Display: romana glífica de terminales abocinados**, en mayúsculas espaciadas. Aparece en THE LONG TABLE, MENÚ, MYSTICISM, TERRITORY y RILÁN. Las astas se ensanchan levemente hacia los remates, como letras talladas, y el contraste es bajo.
2. **Texto: serif de lectura** con altura x generosa y cifras elzevirianas ($70.000). Se usa en párrafos y descripciones.

rilanhotel.com no estaba en línea el 5 de octubre de 2026, así que no se pudieron leer los estilos computados. La identificación se hizo comparando las piezas con fuentes candidatas renderizadas lado a lado.

## Equivalentes web elegidas (licencia SIL OFL, autoalojadas)
| Rol | Fuente | Por qué |
|---|---|---|
| Display / rótulos | **Marcellus** 400 | Es la más cercana a las mayúsculas de las piezas: astas abocinadas, A puntiaguda, G y M de proporciones clásicas. Se descartaron Cinzel, Cormorant SC, Forum y Tenor Sans. |
| Texto | **Newsreader** 300/400/500 + itálica | Altura x y color de mancha muy próximos al texto de las piezas, con cifras elzevirianas. |

Archivos: `assets/fonts/*.woff2`.

## Escala (fluida, clamp)
| Token | Uso | Tamaño |
|---|---|---|
| `--fs-mega` | Palabra pilar (TERRITORY…) | clamp(3.5rem, 11vw, 11rem) · Marcellus · tracking .08em |
| `--fs-h1` | Titular de sección | clamp(2.2rem, 5.2vw, 5rem) · Newsreader 300 |
| `--fs-h2` | Subtítulo | clamp(1.6rem, 3vw, 2.8rem) · Newsreader 300 |
| `--fs-body` | Párrafo | clamp(1.05rem, 1.2vw, 1.25rem) · Newsreader 400 · interlineado 1.55 |
| `--fs-label` | Rótulos y coordenadas | .72rem · Marcellus · mayúsculas · tracking .28em |

Regla de la marca: los rótulos siempre van en mayúsculas espaciadas y los párrafos en caja baja, sin negritas.
