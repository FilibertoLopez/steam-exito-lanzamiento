---
titulo: Estrategia de limpieza de datos
estado: borrador
notebook: notebooks/03_limpieza.ipynb
codigo: src/steam_exito/limpieza_basica.py
actualizado: 2026-11-26
acuerdos: [A-005, A-008, D-002, D-004, D-012, D-021, D-022]
---

# Estrategia de limpieza de datos

Este documento explica qué hace la limpieza básica (tarea S1-01, [`limpieza_basica.py`](../src/steam_exito/limpieza_basica.py)) y por qué. Las cifras se calcularon con la versión congelada del 2026-11-24 (151,023 filas × 33 columnas, A-008), por lo que difieren un poco de las del [diccionario de datos](02-diccionario-datos.md), que usó la descarga del 2026-11-19 (150,199 filas).

La limpieza son cuatro pasos `df → df` que el pipeline ejecuta en este orden: `convertirTipos → limpiarFechas → limpiarPrecios → marcarSinDato`. Después viene `quitarNoJuegos` (S1-04, Luis). Cada paso queda registrado en la bitácora (`contrato.BITACORA`). La limpieza **no** filtra por año ni por número de reseñas: eso lo hace `muestra.filtrarMuestra` (S1-11), según [0002](decisiones/0002-minimo-de-resenas.md) y [0004](decisiones/0004-periodo-de-la-muestra.md).

## Valores faltantes

**Criterio.** Las filas con un valor faltante no se eliminan, salvo cuando falta la fecha de lanzamiento: sin fecha no se puede asignar una cohorte ni ubicar el juego en la partición temporal ([0003](decisiones/0003-particion-temporal.md)). En el resto de las columnas el faltante se conserva como `NaN`/`<NA>`, y cada bloque de variables decide cómo tratarlo, con un indicador `*_sin_dato` cuando el faltante tiene significado (reglas de integración, §3.2).

Faltantes después de la limpieza básica (150,939 filas):

| Columna | Faltantes | % | Origen | Tratamiento |
|---|---:|---:|---|---|
| `release_date` | 0 | 0.00 | Los 82 vacíos de origen se eliminan | `limpiarFechas` quita la fila |
| `price` | 1,380 | 0.91 | Todos con `price_status = unavailable` (juegos retirados de la venta) | Se conservan; `precio_sin_dato` (S1-02) |
| `achievements` | 26,937 | 17.85 | Nulo en el origen | Se conservan; el 0 sí es real (ver abajo) |
| `developers` | 8,435 | 5.59 | Lista vacía `[]` | `marcarSinDato` → `NaN` |
| `publishers` | 8,835 | 5.85 | Lista vacía `[]` | `marcarSinDato` → `NaN` |
| `genres` | 8,419 | 5.58 | Lista vacía `[]` | `marcarSinDato` → `NaN`; el juego **no** se elimina como no-juego (S1-04) |
| `categories` | 8,947 | 5.93 | Lista vacía `[]` | `marcarSinDato` → `NaN` |
| `supported_languages` | 8,382 | 5.55 | 30 nulos y 8,352 listas vacías | `marcarSinDato` → `NaN` |
| `full_audio_languages` | 56,179 | 37.22 | Nulos de las filas con `supported_languages` en formato HTML, donde el doblaje va marcado con `*` | **No se toca**: lo resuelve `parsers.idiomasYAudio` (S1-06) |
| `name` | 1 | 0.00 | Vacío real | Se conserva |
| `mac`, `linux`, `windows` | 0 | 0.00 | Los 14 vacíos de origen coinciden con fechas vacías | Desaparecen al quitar las fechas inválidas |

Las columnas `has_website`, `has_support_url`, `has_support_email` y `has_notes` no tienen faltantes: son indicadores que se construyen al cargar los datos (`carga._aIndicadores`).

**Las 82 fechas inválidas** son celdas vacías, no textos con otro formato. Incluyen las 14 filas sin datos de la tienda (`steam_store_available = False`), que también tienen vacías las plataformas y el nombre. Entre las 82 suman 54,918 reseñas, pero sin fecha no pueden entrar en ninguna cohorte.

## Ceros válidos vs. sin dato

En nueve columnas la fuente usa un valor para indicar «no hay información» ([diccionario de datos](02-diccionario-datos.md#faltantes-y-sin-dato)). `marcarSinDato` los convierte a nulo para que no se confundan con un valor real. La lista vive en `config.COLUMNAS_CERO_ES_NULO`.

| Columna | Nulos de origen | Ceros → `NaN` | Faltantes después | % | Momento |
|---|---:|---:|---:|---:|---|
| `recommendations` | 53,721 | 74,826 | 128,547 | 85.16 | Post |
| `peak_ccu` | 0 | 131,309 | 131,309 | 86.99 | Post |
| `metacritic_score` | 63,280 | 83,362 | 146,642 | 97.15 | Post |
| `user_score` | 0 | 150,834 | 150,834 | 99.93 | Post |
| `average_playtime_forever` | 0 | 141,799 | 141,799 | 93.94 | Post |
| `median_playtime_forever` | 0 | 141,799 | 141,799 | 93.94 | Post |
| `average_playtime_2weeks` | 0 | 149,144 | 149,144 | 98.81 | Post |
| `median_playtime_2weeks` | 0 | 149,144 | 149,144 | 98.81 | Post |
| `estimated_owners` (rango `0 - 0` o `0 .. 0`) | 0 | 21,076 | 21,076 | 13.96 | Post |

Todas son variables POST: no se usan como predictoras (D-012). Se limpian porque sirven para validar y para la auditoría de fuga, y porque un 0 que significa «sin dato» distorsiona cualquier promedio o correlación.

**Ceros que son valores reales** y que `marcarSinDato` **no** modifica:

| Columna | Ceros | Significado |
|---|---:|---|
| `price` | 28,736 | Juego gratuito |
| `positive` + `negative` | 67,848 juegos con 0 reseñas | Sin reseñas; `y_pct_pos` queda `NaN` (S1-10) y el juego queda fuera de la muestra por el umbral |
| `achievements` | 43,540 | El juego no define logros |
| `dlc_count` | 127,787 | Sin DLC (la columna se descarta, D-012) |
| `full_audio_languages` = `[]` | 62,989 | Sin doblaje completo |

## Duplicados

**Llave.** `app_id` es único en la versión congelada (0 repetidos), y el contrato de integración lo vuelve a verificar al final de cada paso (`pasoLimpieza` falla si aparece un `app_id` duplicado). No hay que eliminar duplicados por llave.

**Duplicados de contenido.** Hay juegos con el mismo nombre, fecha y desarrollador, pero con `app_id` distinto:

| Criterio | Filas | Grupos | En la muestra* |
|---|---:|---:|---:|
| Todas las columnas iguales salvo `app_id` | 14 | 7 | — |
| Mismo `name`, `release_date` y `developers` | 179 | 67 | 141 filas (61 grupos) |
| Mismo nombre (sin distinguir mayúsculas) | 3,802 | 1,700 | — |

\* Hasta 2024 y con al menos 50 reseñas, antes de quitar los no-juegos.

- Los grupos de nombre, fecha y desarrollador son, sobre todo, **ediciones o versiones regionales** de títulos de 2006 a 2015 (por ejemplo, *Alpha Protocol*, *Assassin's Creed 2* o *BRINK*, con dos o tres fichas). Cada ficha tiene su propia página en la tienda y **sus propias reseñas** (*Assassin's Creed 2*: 48,815 y 15,726 positivas), así que no son registros repetidos y no se pueden fusionar sin inventar datos.
- Los 7 pares idénticos en todo menos el `app_id` (*Crazy Machines 1.5*, *RIP - Trilogy™*, *EA SPORTS FC™ 24*, entre otros) tienen pocas reseñas o ninguna; solo *RIP - Trilogy™* (340 reseñas) llega a la muestra, dos veces.
- El mismo nombre sin más coincidencias no indica duplicado: son títulos genéricos de juegos distintos (*Escape*, *Alone*, *Echoes*).

**Decisión de la limpieza básica:** no se eliminan duplicados de contenido. Esto no genera fuga, por dos razones:

1. La partición temporal nunca parte un mismo día ([0003](decisiones/0003-particion-temporal.md)), así que las fichas de un mismo grupo caen siempre en el mismo conjunto.
2. El historial del desarrollador no cuenta los juegos del mismo día (S1-07, prueba obligatoria 2).

Queda una pregunta abierta sobre estos grupos, registrada para la sesión del 2026-11-30 en el [registro de sesiones](equipo/sesiones/README.md#preguntas-abiertas-pendientes).

## Valores atípicos

**Criterio.** Solo se elimina un registro cuando el valor es **imposible o claramente erróneo**. Los valores extremos pero posibles se conservan, y los bloques de variables los suavizan con transformaciones (`precio_log`, `precio_rango`, `ficha_logros_log`) en lugar de recortarlos. Las variables POST no se tratan, porque no son predictoras (D-012).

| Columna | Mediana | p99 | p99.9 | Máximo | Tratamiento |
|---|---:|---:|---:|---:|---|
| `price` (USD) | 4.99 | 49.99 | 199.99 | 107,500 → 16,000 | Se eliminan los 2 registros de 107,500 (D-004); el resto se conserva |
| `achievements` | 10 | 100 | 1,730 | 10,979 | Se conservan; `ficha_logros_log` (S1-03) |
| `dlc_count` | 0 | 6 | 42 | 3,966 | No se usa (D-012) |
| `positive` | 1 | 10,040 | 128,321 | 7,642,084 | Solo construye el objetivo; la proporción no depende de la escala |
| `average_playtime_forever` (min) | 221 | 9,145 | 85,279 | 359,665 | POST: no se usa (D-012) |

Mediana y percentiles sobre los valores no nulos, después de la limpieza básica.

**Precio (D-004).** Los dos registros de 107,500 USD (*The Honored Wife* y *Soft Money*, ambos de 2026) se eliminan con `config.PRECIO_MAX_VALIDO = 100_000`. Después quedan otros precios extremos:

- 268 juegos con más de 100 USD y 17 con más de 200 USD.
- Los únicos por encima de 1,000 USD (*Strict Sensei*, 16,000 USD; *MolCollabo v2*, 1,900 USD) son de 2025 y 2026, así que los excluye el periodo de la muestra (D-022).
- Hasta 2024 el máximo es 999.98 USD, pero ninguno de esos juegos caros llega a la muestra (ver la tabla siguiente).

**Precio en la muestra.** Juegos hasta 2024 con al menos 50 reseñas (29,043 antes de quitar los no-juegos):

| Medida | Valor |
|---|---:|
| Sin precio (retirados de la venta) | 586 |
| Gratis | 3,600 (12.4 %) |
| Mediana / media | 8.99 / 11.29 USD |
| Mediana / media de los de pago | 9.99 / 12.93 USD |
| p75 / p90 / p95 | 14.99 / 24.99 / 29.99 USD |
| p99 / p99.9 | 59.99 / 79.99 USD |
| Más de 60 / 100 / 200 USD | 83 / 12 / 3 |
| Máximo | 299 USD |

La distribución es muy asimétrica a la derecha: el 99 % de los juegos cuesta 59.99 USD o menos. Los 12 juegos de más de 100 USD son de dos tipos:

| Tipo | Juegos | Precio | Qué pasa con ellos |
|---|---:|---|---|
| Programas profesionales: *Houdini Indie* (299), *3DF Zephyr Lite* (249), cuatro ediciones de *VEGAS* (149.99 a 249) y *Substance 3D Modeler 2025* (149.99) | 7 | 149.99 – 299 | Todos sus géneros están en `config.GENEROS_NO_JUEGO` (Animation & Modeling, Video Production, etc.), así que `quitarNoJuegos` (S1-04) debe quitarlos |
| Juegos con precio de broma: *Spooky Men*, *★ Fallalypse ★*, *✌ Johnny Rocket*, *Monkey vs Dino* (199.99 cada uno) y *Mushroom Challenge* (120) | 5 | 120 – 199.99 | Se quedan en la muestra; el precio es real aunque no sea representativo |

Después del filtro de no-juegos, el precio máximo de la muestra baja a 199.99 USD. Por eso no se propone bajar `PRECIO_MAX_VALIDO`: el periodo (D-022) y el filtro de no-juegos resuelven los casos extremos, y `precio_log` y el rango «40+» del EDA (533 juegos, EDA §5.1) reducen la influencia de los precios altos.

**Logros.** 166 juegos tienen más de 1,000 logros y 3 más de 5,000 (máximo: *The Mexican Dream*, 10,979). Son valores posibles: hay juegos que inflan los logros como reclamo. En la muestra quedan 145 juegos con más de 1,000. Se conservan y se usan en escala logarítmica, junto con el indicador `ficha_tiene_logros`.

### Preguntas para el equipo

Se proponen para la sesión del 2026-11-30, junto con la sensibilidad de la muestra (S1-12). Mientras no se decidan, la limpieza básica no cambia.

La pregunta sobre los duplicados de contenido ([Duplicados](#duplicados)) está en el [registro de sesiones](equipo/sesiones/README.md#preguntas-abiertas-pendientes), como tema de la sesión del 2026-11-30, y se discute en el [issue #3](https://github.com/FilibertoLopez/steam-exito-lanzamiento/issues/3#issuecomment-7206821360).

| # | Pregunta | Datos | Propuesta |
|---|---|---|---|
| 1 | ¿Excluir de la muestra los 5 juegos con precio de broma (120 a 199.99 USD)? | 5 juegos de 29,043; todos los demás cuestan 100 USD o menos | Conservarlos: el precio es real y `precio_log` limita su peso. Revisarlos como casos influyentes en el Sprint 2 |

## Tipos y formatos

`convertirTipos` asigna los tipos sin quitar filas. Los booleanos y enteros usan tipos **anulables** de pandas (`boolean`, `Int64`) para que un faltante no convierta la columna a `object` o a decimal.

| Columna | Tipo de origen | Tipo después | Regla |
|---|---|---|---|
| `mac`, `linux`, `windows` | texto (`"True"`/`"False"`, 14 vacíos) | `boolean` | `parsers.aBooleano`; los vacíos quedan `<NA>` |
| `achievements` | decimal (`float64`) | `Int64` | Es un conteo; no hay valores fraccionarios ni negativos, así que el redondeo no cambia ningún dato |
| `price` | decimal | decimal | `pd.to_numeric`; garantiza que sea numérico también con el CSV público |
| `positive`, `negative` | entero | numérico | `pd.to_numeric` |
| `release_date` | texto `AAAA-MM-DD` | `datetime64` | `limpiarFechas`, formato ISO estricto; lo que no cumple el formato queda inválido |

**Listas guardadas como texto.** `developers`, `publishers`, `genres`, `categories` y `supported_languages` mezclan dos formatos (lista de textos y lista de objetos `{"id", "description"}`), y unas 28 mil celdas de `supported_languages` traen un solo texto HTML. La limpieza básica **no** cambia el formato: solo marca como `NaN` las listas vacías con `parsers.esVacio`. Cada bloque lee las listas con `parsers.aLista` o `parsers.idiomasYAudio`, nunca con `split(",")` (reglas de integración, §4.3). El formato original no se usa como variable, porque es un artefacto de la recolección (EDA §2.3).

## Reglas aplicadas

Bitácora de la limpieza básica sobre la versión congelada (`contrato.resumenBitacora()`):

| # | Paso | Función | Filas antes | Filas después | Quitadas | Regla | Acuerdo |
|---:|---|---|---:|---:|---:|---|---|
| 1 | `tipos` | `convertirTipos` | 151,023 | 151,023 | 0 | Tipos booleanos, enteros y numéricos | Diccionario |
| 2 | `fechas` | `limpiarFechas` | 151,023 | 150,941 | 82 | Fecha vacía o inválida, o posterior a `config.VERSION_DATOS["fecha_max_lanzamiento"]` (2026-11-24; ninguna) | A-005, A-008 |
| 3 | `precios` | `limpiarPrecios` | 150,941 | 150,939 | 2 | `price > config.PRECIO_MAX_VALIDO` (100,000): los dos juegos de 107,500 USD, ambos de 2026 | D-004 |
| 4 | `sin_dato` | `marcarSinDato` | 150,939 | 150,939 | 0 | Ceros y rangos «sin dato» → `NaN`; listas vacías → `NaN` | Diccionario |

Después de la limpieza quedan juegos con fechas del 1997-06-30 al 2026-11-24. Los filtros de periodo (hasta 2024, D-022) y de mínimo de reseñas (50, D-014) se aplican después, en la construcción de la muestra. El embudo completo, con `quitarNoJuegos` y la muestra final de 28,708 juegos, se presenta en `notebooks/03_limpieza.ipynb` (S1-14).

Para reproducir la tabla:

```python
from steam_exito import carga, contrato
from steam_exito.limpieza_basica import convertirTipos, limpiarFechas, limpiarPrecios, marcarSinDato

contrato.BITACORA.clear()
df = carga.cargarSlim()
carga.verificarVersion(df)
df = marcarSinDato(limpiarPrecios(limpiarFechas(convertirTipos(df))))
contrato.resumenBitacora()
```
