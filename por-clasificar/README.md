# Por clasificar

Lugar temporal para material que todavía no sabemos dónde debe vivir en el repositorio: borradores, notas sueltas, artículos encontrados, gráficas de prueba, ideas, archivos que alguien compartió por chat, etc.

**Nada se queda aquí para siempre.** En cada sesión del equipo se revisa esta carpeta y cada archivo se mueve a su lugar definitivo o se elimina.

## Carpetas

| Carpeta | Uso |
|---|---|
| [`diana/`](diana/) | Material que sube Diana |
| [`alejandra/`](alejandra/) | Material que sube Alejandra |
| [`luis/`](luis/) | Material que sube Luis |
| [`filiberto/`](filiberto/) | Material que sube Filiberto |
| [`compartido/`](compartido/) | Material de todos o sin autor claro (p. ej. archivos recibidos por correo o chat) |

Cada quien trabaja en su propia carpeta; así se evitan conflictos al hacer `git pull`.

## Reglas

1. **Nombre del archivo:** `AAAA-MM-DD-descripcion-corta.ext`, en minúsculas, con guiones, sin acentos ni espacios. Ejemplo: `2026-11-24-articulo-precio-vs-resenas.pdf`.
2. **Registro:** agrega una fila a la tabla de abajo al subir algo; sin registro no se sabe de qué es ni por qué está aquí.
3. **No subir:** datos crudos o procesados (van en `data/`, que no se versiona), grabaciones de Zoom (se enlazan en el [registro de sesiones](../docs/equipo/sesiones/README.md)), contraseñas ni archivos de más de 50 MB.
4. **Archivos binarios:** PDF, PPTX, DOCX y XLSX se suben con Git LFS automáticamente (ver `.gitattributes`).
5. **Al clasificar:** mueve el archivo con `git mv` (o desde Obsidian), borra su fila de la tabla y, si el destino es una decisión del equipo, anótalo en [acuerdos](../docs/equipo/acuerdos.md).

## Destinos habituales

| Si es… | Va a |
|---|---|
| Artículo, libro o página de referencia | `references/articulos/` y su ficha en `references/fichas/` |
| Nota sobre análisis, limpieza, variables o modelos | El documento correspondiente en `docs/` |
| Script o notebook | `notebooks/` o `notebooks/borradores/` |
| Función reutilizable | `src/steam_exito/` |
| Gráfica o resultado | `reports/figures/` o `reports/metrics/` |
| Material para la presentación | `reports/presentacion/` |
| Resumen o transcripción de Zoom | `docs/equipo/sesiones/` |

## Material pendiente de clasificar

| Archivo | Subido por | Fecha | Qué es | Destino propuesto |
|---|---|---|---|---|
| [diana/2026-11-24-EDA_Steam_Proyecto_Final_DA.ipynb](diana/2026-11-24-EDA_Steam_Proyecto_Final_DA.ipynb) | Diana | 2026-11-24 | EDA de Diana (acuerdo A-002): notebook de 34 celdas con carga, calidad de datos, variable objetivo (proporción positiva), características de lanzamiento, géneros y categorías (multi-hot), idiomas, relaciones con la recepción (juegos con ≥ 50 reseñas) e historial del desarrollador con control de fuga | `notebooks/02_eda.ipynb` (como base) o `notebooks/borradores/` |
| [diana/2026-11-24-EDA_Steam_DA.docx](diana/2026-11-24-EDA_Steam_DA.docx) | Diana | 2026-11-24 | Documento de EDA de Diana: fuentes, calidad (faltantes, campos vacíos, fechas y precios), variable objetivo y muestra según mínimo de reseñas, características de lanzamiento, relaciones con la recepción e historial del desarrollador; 12 figuras | Contenido a `docs/03-analisis-exploratorio.md`; figuras a `reports/figures/` |
| [filiberto/01-planteamiento.md](filiberto/01-planteamiento.md) | Filiberto | 2026-11-24 | Borrador del planteamiento: contexto, pregunta de investigación, definición de éxito, alcance, restricciones e hipótesis | `docs/01-planteamiento.md` (reemplaza la plantilla) |
| [filiberto/02-diccionario-datos.md](filiberto/02-diccionario-datos.md) | Filiberto | 2026-11-24 | Borrador del diccionario de datos: variables de `steam_games.csv` y `steam_games_reviews.csv` por momento (antes/después del lanzamiento) y rol, valores categóricos, variable objetivo, problemas de calidad y pendientes | `docs/02-diccionario-datos.md` (reemplaza la plantilla) |
| [luis/EDA_LR_V1/ProyectoSteamEDA_LR_V1.ipynb](luis/EDA_LR_V1/ProyectoSteamEDA_LR_V1.ipynb) y [Avance_EDA_Steam.docx](luis/EDA_LR_V1/Avance_EDA_Steam.docx) | Luis | 2026-11-23 | EDA de Luis (acuerdo A-002): notebook de 14 celdas y documento de avance | `notebooks/borradores/` y `docs/03-analisis-exploratorio.md` |
