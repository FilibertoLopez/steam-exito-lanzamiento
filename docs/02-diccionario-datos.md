---
titulo: Diccionario de datos
estado: en revisión
notebook: notebooks/01_carga_perfilado.ipynb
version_datos: 2026-11-19
filas: 150199
columnas: 42
---

# Diccionario de datos

Describe las 42 columnas de `steam_games.csv` y las 3 de `steam_games_reviews.csv`. Para cada una dice qué contiene, si se conoce antes del lanzamiento y qué papel tendrá en el modelo. Lo que se hace con cada columna está en [Estrategia de limpieza](04-estrategia-limpieza.md), y las variables que se derivan de ellas en [Ingeniería de variables](05-ingenieria-variables.md).

## Fuente

| Atributo | Valor |
|---|---|
| Conjunto | Steam Games Dataset – All Games |
| Autor | Hubert Sidorowicz |
| URL | <https://www.kaggle.com/datasets/hubertsidorowicz/steam-games-dataset-daily-updates> |
| Licencia | MIT |
| Origen de los datos | Steam Store y SteamSpy (columnas `steam_store_available` y `steam_spy_available`) |
| Frecuencia de actualización | Diaria |
| Versión usada | Descarga del 2026-11-19 (archivos fechados 2026-11-19 03:40) |
| Ubicación local | `data/raw/` (no se versiona; ver [data/README.md](../data/README.md)) |

> [!info] Cómo se construyó este diccionario
> Los tipos, conteos, porcentajes y rangos se calcularon leyendo los CSV completos con pandas. El autor no publica un diccionario oficial campo por campo, así que las descripciones se infieren del nombre de cada columna, de su contenido y de la descripción del dataset en Kaggle.

## Archivos

| Archivo | Tamaño | Filas | Columnas | Llave |
|---|---:|---:|---:|---|
| `steam_games.csv` | 1.14 GB | 150,199 | 42 | `app_id` (único, sin duplicados) |
| `steam_games_reviews.csv` | 4.9 MB | 13,568 | 3 | `app_id` (todos existen en `steam_games.csv`) |

Los dos archivos se unen por `app_id`.

## Convenciones

### Momento

Indica cuándo se conoce el dato. Es el criterio central del proyecto, porque solo se pueden usar como predictores los factores disponibles antes del lanzamiento.

| Momento | Significado | Uso en el modelo |
|---|---|---|
| **Id** | Identificador o metadato de la fuente | Llave o filtro; sin valor predictivo |
| **Pre** | Se conoce antes del lanzamiento | Candidata a predictora |
| **Pre\*** | Se conoce antes, pero el valor guardado es el actual de la tienda al 2026-11-19 y pudo cambiar después del lanzamiento | Predictora con reserva; se documenta como limitación |
| **Post** | Se genera después del lanzamiento | Variable objetivo, validación o descarte por fuga de información |

### Rol

| Rol | Significado |
|---|---|
| **Predictora** | Entra al modelo, directamente o mediante variables derivadas |
| **Objetivo** | Se usa para construir la variable a predecir |
| **Validación** | Solo sirve para contrastar resultados |
| **Filtro** | Se usa para quitar filas y después se elimina |
| **Llave** | Identifica el registro |
| **Descartar** | No se usa |

### Faltantes y «sin dato»

- **% faltantes** cuenta celdas nulas, en blanco, `[]` o `{}` sobre las 150,199 filas.
- En las columnas marcadas con **⁰**, la fuente usa un valor para indicar que no tiene información, y ese valor también cuenta como faltante:
  - `0` en `recommendations`, `peak_ccu`, `metacritic_score`, `user_score` y los cuatro tiempos de juego.
  - El rango `0 - 0` en `estimated_owners`.
- En las demás columnas el `0` es un valor real: `price` = gratis, `positive` y `negative` = sin reseñas, `achievements` = sin logros, `dlc_count` = sin DLC.
- Las columnas de tipo lista o diccionario vienen como texto JSON y se convierten con `json.loads`.
- Al leer el CSV hay que usar `keep_default_na=False, na_values=[""]`. Si no, pandas convierte en nulos el juego llamado «NULL» y una nota con el texto «None».

## Variables de `steam_games.csv`

| # | Columna | Tipo | Descripción | Momento | Rol | % faltantes | Notas |
|---:|---|---|---|---|---|---:|---|
| 1 | `app_id` | Entero | Identificador de la aplicación en Steam | Id | Llave | 0.00 % | Rango 10 – 5,547,990. Único. Une con `steam_games_reviews.csv`. |
| 2 | `name` | Texto | Nombre del juego | Id | Filtro | 0.01 % | 15 vacíos reales. Espacios al inicio y Unicode raro. Sirve para marcar lo que no es juego (Soundtrack, Demo, Playtest, SDK). |
| 3 | `release_date` | Fecha (`AAAA-MM-DD`) | Fecha de lanzamiento | Pre | Predictora y filtro | 0.05 % | Rango 1997-06-30 – 2026-11-18. Define la cohorte (año de lanzamiento) y el filtro de antigüedad. 2026 es el año con más registros (28,168). |
| 4 | `price` | Decimal (USD) | Precio actual | Pre\* | Predictora | 0.95 % | Valor al 2026-11-19, no el de lanzamiento; puede incluir descuentos. 28,651 en 0 (gratis). Mediana 4.99, p99 49.99. Máximo atípico de 107,500. Los vacíos coinciden con `price_status = unavailable`. |
| 5 | `price_status` | Categórico | Estado del precio | Pre | Filtro | 0.00 % | `paid` 120,128 · `free` 28,651 · `unavailable` 1,420. Redundante con `price`. |
| 6 | `estimated_owners` ⁰ | Categórico ordinal (rango) | Rango estimado de propietarios (SteamSpy) | Post | Validación | 14.04 % | 21,089 en `0 - 0`. Dos formatos para el mismo rango (`0 - 20000` y `0 .. 20,000`): 26 cadenas para 14 rangos reales. El equipo la considera poco confiable como objetivo. Ver [Rangos de `estimated_owners`](#rangos-de-estimated_owners). |
| 7 | `developers` | Lista JSON | Estudios desarrolladores | Pre | Predictora (derivadas) | 5.63 % | 94,963 desarrolladores distintos: no se usa el nombre directamente, sino historial previo (juegos anteriores, éxito promedio). Nombres escritos de varias formas y valores `[" "]`. |
| 8 | `publishers` | Lista JSON | Distribuidores | Pre | Predictora (derivadas) | 5.89 % | Unos 80,000 distintos. Permite distinguir autopublicación de distribuidor externo. |
| 9 | `genres` | Lista JSON multicategórica | Géneros oficiales de Steam | Pre | Predictora y filtro | 5.62 % | 43 valores. Dos formatos: lista de textos (87,555) u objetos `{"id","description"}` (54,210). Hay géneros traducidos, géneros de software y etiquetas comerciales. Ver [Géneros](#géneros-genres). |
| 10 | `categories` | Lista JSON multicategórica | Características de Steam (Single-player, Co-op, logros, controles…) | Pre | Predictora | 5.97 % | 98 valores. Mismos dos formatos que `genres` (87,317 / 53,920). Claves sin traducir (`#category_…`). Steam Trading Cards se excluye porque Steam la activa por ventas. |
| 11 | `tags` | Lista o diccionario JSON | Etiquetas de la comunidad (SteamSpy) | Pre\* / Post | Descartar | 44.42 % | 459 valores. Lista (48,162) o `{etiqueta: votos}` (35,320). Las asignan los usuarios después del lanzamiento: riesgo de fuga. Solo para análisis descriptivo. |
| 12 | `positive` | Entero | Reseñas positivas de usuarios | Post | Objetivo | 0.00 % | 46 % en 0 (valor real). Mediana 1, máximo 7,642,084. Muy sesgada. |
| 13 | `negative` | Entero | Reseñas negativas de usuarios | Post | Objetivo | 0.00 % | 55 % en 0 (valor real). Máximo 1,173,003. 67,108 juegos no tienen ninguna reseña. |
| 14 | `recommendations` ⁰ | Decimal (conteo) | Recomendaciones totales en la tienda | Post | Validación | 85.10 % | 52,077 nulos + 75,737 ceros. El mínimo distinto de 0 es 101, lo que sugiere que Steam solo publica la cifra a partir de 100 (valor censurado; umbral por confirmar en una fuente primaria). |
| 15 | `peak_ccu` ⁰ | Entero | Pico de jugadores simultáneos del día anterior (SteamSpy) | Post | Descartar | 86.89 % | 130,511 ceros. 414 juegos con más de 1,000 reseñas positivas tienen pico 0. No es el pico del lanzamiento. |
| 16 | `metacritic_score` ⁰ | Decimal (0–100) | Calificación de Metacritic | Post | Validación | 97.14 % | 61,407 nulos + 84,493 ceros. Los 4,299 valores reales (6 – 97) coinciden con las filas que tienen `metacritic_url`. Sesgada a títulos grandes. |
| 17 | `user_score` ⁰ | Entero (0–100) | Calificación de usuarios | Post | Descartar | 99.95 % | Solo 69 valores reales (37 – 100). |
| 18 | `average_playtime_forever` ⁰ | Entero (minutos) | Tiempo medio de juego histórico | Post | Descartar | 93.86 % | 140,973 ceros: SteamSpy no tiene muestra de jugadores. Máximo atípico de 359,665 min. |
| 19 | `median_playtime_forever` ⁰ | Entero (minutos) | Mediana histórica del tiempo de juego | Post | Descartar | 93.86 % | Mismas filas en 0 que el promedio. |
| 20 | `average_playtime_2weeks` ⁰ | Entero (minutos) | Tiempo medio en las últimas 2 semanas | Post | Descartar | 98.78 % | Depende de la fecha de descarga. |
| 21 | `median_playtime_2weeks` ⁰ | Entero (minutos) | Mediana en las últimas 2 semanas | Post | Descartar | 98.78 % | Depende de la fecha de descarga. |
| 22 | `short_description` | Texto | Descripción breve de la tienda | Pre | Predictora | 5.55 % | Longitud 1 – 342. Caracteres de control al inicio y emojis. Apta para longitud o NLP. |
| 23 | `about_the_game` | Texto (HTML) | Sección «Acerca del juego» | Pre | Predictora | 5.61 % | Hasta 91,113 caracteres. Mezcla HTML y marcadores como `[figure 1]`. |
| 24 | `detailed_description` | Texto (HTML) | Descripción detallada | Pre | Descartar | 5.59 % | Casi idéntica a `about_the_game`. |
| 25 | `notes` | Texto | Aviso de contenido para adultos | Pre | Predictora | 81.52 % | El vacío es esperado: solo los juegos con contenido maduro tienen aviso. |
| 26 | `achievements` | Decimal (conteo) | Número de logros definidos | Pre | Predictora | 17.46 % | 44,047 en 0; mediana 9. Máximo atípico de 10,979. Viene como decimal aunque es un conteo. |
| 27 | `dlc_count` | Entero | Número de DLC asociados | Pre\* | Descartar | 0.00 % | 85 % en 0; máximo 3,966. Los DLC se publican después y siguen al éxito: fuga. |
| 28 | `packages` | Lista JSON | Paquetes y suscripciones de compra | Pre\* | Descartar | 19.32 % | Lista de IDs (56,862) u objetos con `title`, `subs` y `price` (64,323). Valor actual y poco informativo. |
| 29 | `supported_languages` | Lista JSON o texto HTML | Idiomas de interfaz o subtítulos | Pre | Predictora | 5.59 % | Unos 102 idiomas oficiales (hasta 103 con variantes). Lista JSON (87,541) o HTML con `<strong>*</strong>` para el audio completo (54,292). Restos HTML, claves `#lang_…` y nombres traducidos. |
| 30 | `full_audio_languages` | Lista JSON | Idiomas con doblaje completo | Pre | Predictora | 78.49 % | 54,160 nulos (las filas en formato HTML de `supported_languages`, donde el audio va marcado con `*`) + 63,729 listas vacías (sin doblaje, valor real). |
| 31 | `windows` | Booleano | Disponible en Windows | Pre | Descartar | 0.01 % | Casi constante: True 150,119 · False 66. |
| 32 | `mac` | Booleano | Disponible en macOS | Pre | Predictora | 0.01 % | True 25,406 (16.9 %). Se lee como texto por 14 vacíos. |
| 33 | `linux` | Booleano | Disponible en Linux | Pre | Predictora | 0.01 % | True 19,265 (12.8 %). Mismo problema de tipo que `mac`. |
| 34 | `header_image` | Texto (URL) | Imagen de cabecera de la tienda | Pre | Descartar | 0.06 % | El parámetro `?t=` guarda la fecha de la última actualización de la imagen (fuga temporal). |
| 35 | `screenshots` | Lista JSON | Capturas de pantalla | Pre\* | Predictora | 4.02 % | Lista de URL (79,170) u objetos con `path_thumbnail` y `path_full` (64,986). Se usa el conteo. Refleja las capturas actuales. |
| 36 | `movies` | Lista JSON (objetos) | Tráileres | Pre\* | Predictora | 57.78 % | El vacío significa sin tráiler (valor real). Celdas de hasta 36 KB. Se usa el conteo. |
| 37 | `website` | Texto (URL) | Sitio web oficial | Pre | Predictora | 61.69 % | URL sin protocolo en algunos casos. Se usa como indicador. |
| 38 | `support_url` | Texto (URL) | Página de soporte | Pre | Predictora | 57.29 % | Valores basura: espacios y texto en lugar de URL («없음»). |
| 39 | `support_email` | Texto (correo) | Correo de soporte | Pre | Predictora | 16.85 % | Tabuladores, espacios y Unicode estilizado (𝗰𝗼𝗺). |
| 40 | `metacritic_url` | Texto (URL) | Ficha en Metacritic | Post | Descartar | 97.14 % | Redundante con `metacritic_score`. |
| 41 | `steam_store_available` | Booleano | Se obtuvieron datos de la Steam Store | Id | Filtro | 0.00 % | True 150,185 · False 14. Las 14 filas en False coinciden con los vacíos de `windows`, `mac` y `linux`. |
| 42 | `steam_spy_available` | Booleano | Se obtuvieron datos de SteamSpy | Id | Descartar | 0.00 % | Constante (siempre True) en esta versión. |

## Variables de `steam_games_reviews.csv`

| # | Columna | Tipo | Descripción | Momento | Rol | % faltantes | Notas |
|---:|---|---|---|---|---|---:|---|
| 1 | `app_id` | Entero | Identificador del juego (llave foránea) | Id | Llave | 0.00 % | 13,568 valores únicos; todos existen en `steam_games.csv`. |
| 2 | `name` | Texto | Nombre del juego | Id | Descartar | 0.00 % | Redundante con el archivo principal. |
| 3 | `reviews` | Texto | Citas de prensa o premios que el estudio publica en su página | Pre\* | Descartar | 0.00 % | No son reseñas de usuarios. Longitud mediana 273, máxima 2,913. Cubre solo el 9 % de los juegos. |

> [!warning] Diferencia con la descripción de Kaggle
> Kaggle dice que este archivo trae hasta 100 reseñas en inglés por juego, en JSON. En la versión descargada (2026-11-19), `reviews` es texto plano con citas de prensa, una fila por juego.

## Valores categóricos

### Rangos de `estimated_owners`

Las 26 cadenas del CSV se reducen a 14 rangos ordinales. Los conteos suman los dos formatos.

| Nivel | Rango | Juegos |
|---:|---|---:|
| 0 | `0 - 0` (sin dato) | 21,089 |
| 1 | 0 – 20K | 103,478 |
| 2 | 20K – 50K | 11,415 |
| 3 | 50K – 100K | 5,371 |
| 4 | 100K – 200K | 3,469 |
| 5 | 200K – 500K | 2,863 |
| 6 | 500K – 1M | 1,160 |
| 7 | 1M – 2M | 728 |
| 8 | 2M – 5M | 405 |
| 9 | 5M – 10M | 126 |
| 10 | 10M – 20M | 51 |
| 11 | 20M – 50M | 31 |
| 12 | 50M – 100M | 9 |
| 13 | 100M – 200M | 4 |

El rango 100M – 200M solo aparece en el formato con puntos (`100,000,000 .. 200,000,000`).

### Géneros (`genres`)

Según el acuerdo de la sesión del 2026-11-22, los géneros se separan en tres grupos, porque las etiquetas comerciales son independientes del tipo de juego:

| Grupo | Valores | Tratamiento |
|---|---|---|
| Géneros de juego | Action, Adventure, Casual, Simulation, Strategy, RPG, Sports, Racing, Massively Multiplayer | Predictoras (multi-hot) |
| Etiquetas comerciales | Indie, Early Access, Free To Play | Predictoras separadas de los géneros |
| Aviso de contenido | Violent, Gore, Nudity, Sexual Content | Indicador de contenido maduro |
| Software y no juegos | Utilities, Design & Illustration, Animation & Modeling, Education, Video Production, Game Development, Audio Production, Software Training, Photo Editing, Web Publishing, Accounting, Movie, Documentary, Episodic, Short, Tutorial, 360 Video | Filtro: se quitan los títulos cuyos únicos géneros son de este grupo |
| Variantes traducidas | Aventure, Occasionnel, インディー, 早期アクセス, Strategie, Gratuit, Indépendant, Stratégie, Aventura, Simuladores | Se mapean al nombre en inglés |

Education, Episodic y Short quedan en el filtro solo cuando son el único género; si acompañan a un género de juego, el título se conserva. Las listas completas de categorías, etiquetas e idiomas con sus frecuencias están en la nota «Perfil de columnas – steam_games.csv».

## Resumen por momento y rol

| Momento | Columnas | Predictora | Objetivo | Validación | Filtro / llave | Descartar |
|---|---:|---:|---:|---:|---:|---:|
| Id | 4 | 0 | 0 | 0 | 3 | 1 |
| Pre | 20 | 16 | 0 | 0 | 1 | 3 |
| Pre\* | 6 | 3 | 0 | 0 | 0 | 3 |
| Post | 12 | 0 | 2 | 3 | 0 | 7 |
| **Total** | **42** | **19** | **2** | **3** | **4** | **14** |

`tags` se cuenta como Pre\* y `release_date` como predictora, aunque también funciona como filtro. Hay dos cambios respecto a la estrategia de limpieza: `estimated_owners` pasa de objetivo a validación, por el acuerdo de usar la proporción de reseñas positivas como variable objetivo, y `price_status` queda como filtro, porque `price` ya contiene la información de gratis o de pago.

## Variable objetivo

La variable objetivo acordada es la proporción de reseñas positivas:

\[
\text{positiveRatio} = \frac{positive}{positive + negative}
\]

El volumen \( \log(1 + positive + negative) \) queda como medida complementaria de alcance. Las dos se construyen solo con juegos de las cohortes acordadas (se excluyen 2025 y 2026). Los detalles están en [0001 Variable objetivo](decisiones/0001-variable-objetivo.md) y [0002 Mínimo de reseñas](decisiones/0002-minimo-de-resenas.md).

## Problemas de calidad

1. **Formatos mezclados**: `genres`, `categories`, `screenshots`, `supported_languages`, `tags`, `packages` y `estimated_owners` traen dos estructuras distintas, probablemente de dos versiones del proceso de recolección. En `categories` el cambio ocurre alrededor de 2019.
2. **Ceros que significan «sin dato»** en las nueve columnas marcadas con ⁰.
3. **Instantánea, no historia**: precio, DLC, capturas, tráileres y etiquetas reflejan la tienda al 2026-11-19, no el día del lanzamiento (columnas Pre\*).
4. **Juegos recientes**: muchos títulos de 2025 y 2026 aún no acumulan reseñas.
5. **No todo es videojuego**: hay software y contenido audiovisual.
6. **Valores atípicos**: `price` = 107,500, `achievements` = 10,979, `dlc_count` = 3,966 y `average_playtime_forever` = 359,665.
7. **Columnas constantes o casi vacías**: `steam_spy_available`, `windows`, `user_score` y `metacritic_url`.
8. **Alta cardinalidad**: `developers` y `publishers` no pueden codificarse directamente.

## Pendientes

- [ ] Auditar una muestra de juegos de 2021–2024 con cero reseñas contra la tienda para saber si son ceros reales o datos sin actualizar.
- [ ] Confirmar en una fuente primaria el umbral de publicación de `recommendations`.
- [ ] Medir el porcentaje de filas en que `detailed_description` es idéntica a `about_the_game`.
- [ ] Contar cuántas filas quita el filtro de software.
- [ ] Decidir si `mac` y `linux` se conservan, después del análisis por plataforma (pregunta abierta de la sesión del 2026-11-22).
