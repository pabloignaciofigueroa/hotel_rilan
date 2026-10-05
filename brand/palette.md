# Paleta RILÁN

Extraída con k-means (k = 7) de 100 fotos y de las 5 piezas gráficas de la marca. El porcentaje indica la presencia del color en el grupo.

## Base de marca (piezas gráficas)
| Token | Hex | Origen |
|---|---|---|
| `--niebla` | #EAE9E3 | Fondo de las piezas (52 %) |
| `--piedra` | #544F4C | Tinta y fondo oscuro de las piezas (38 %) |
| `--ceniza` | #847F7B | Texto secundario de las piezas |
| `--bruma` | #CCCBC4 | Líneas divisorias |

## Territorio (fotos)
| Token | Hex | Origen |
|---|---|---|
| `--noche` | #121311 | Sombras de exteriores, gastronomía y habitaciones |
| `--bosque` | #2C362F | Exteriores (22 %) |
| `--helecho` | #113A1F | TERRITORY |
| `--madera` | #644B34 | Interiores, madera de los muros |
| `--fuego` | #B07436 | Interiores y gastronomía: fuego y cobre (acento) |
| `--mar` | #A6B6C4 | Cielo y agua de exteriores |
| `--archipielago` | #4C5255 | MYSTICISM: niebla y agua |

## Roles
- **Claro**: fondo `--niebla`, texto `--piedra` (contraste 6,6:1, AA).
- **Oscuro**: fondo `--noche` o `--piedra`, texto `--niebla` (15,3:1 sobre noche y 6,6:1 sobre piedra).
- **Acento**: `--fuego`, con mesura. Se usa solo en hover, en el cursor y en detalles finos, nunca en texto largo. Sobre `--noche` contrasta 4,8:1. `--ceniza` sobre niebla da 3,3:1: solo para texto grande o rótulos.
- **Sobre foto**: texto `--niebla` sobre un velo de `--noche` al 35–55 %.
