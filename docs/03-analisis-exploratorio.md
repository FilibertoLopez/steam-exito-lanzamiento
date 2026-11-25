---
titulo: Análisis exploratorio de datos
estado: borrador (generado a partir de notebooks/02_eda.ipynb)
notebook: notebooks/02_eda.ipynb
datos: versión congelada del 2026-11-24 (151,023 filas)
---

# Análisis exploratorio de datos

Resumen del EDA unificado. Todas las cifras salen de `notebooks/02_eda.ipynb` y las tablas están en `reports/metrics/02_eda_*.csv`. Las figuras están en `reports/figures/02_eda_*.png`. Este texto es la base de la §6 del reporte (tarea S1-R3): al pasarlo al reporte hay que convertirlo en prosa continua, numerar tablas y figuras e interpretarlas.

## 1. Resumen del conjunto

- **Fuente:** *Steam Games Dataset – All Games* (Hubert Sidorowicz, Kaggle, licencia MIT), con datos de Steam Store y SteamSpy. Se actualiza a diario.
- **Versión congelada:** descarga del 24-nov-2026, **151,023 juegos** y 33 columnas (42 originales menos 9 columnas pesadas). `app_id` es único.
- **Problema de reproducibilidad resuelto:** los cuatro EDA individuales se hicieron con descargas distintas (145,257; 150,199; 150,643 y 151,023 filas), por eso sus cifras no coincidían (p. ej., entre 62,178 y 67,929 juegos sin reseñas). Desde aquí todo el equipo usa un único archivo, verificado con `carga.verificarVersion`.
- **Archivo de reseñas:** `steam_games_reviews.csv` contiene citas de prensa del 9 % de los juegos, no reseñas de usuarios; no se usa.
- **Disponibilidad temporal de las columnas:** 11 columnas son posteriores al lanzamiento (reseñas, propietarios estimados, jugadores simultáneos, tiempos de juego, Metacritic, etc.), 5 son «Pre\*» (precio, categorías, idiomas, DLC: el valor es el de la tienda hoy) y el resto se conoce antes del lanzamiento.

## 2. Calidad de los datos

**Faltantes.** Un faltante puede ser nulo, texto vacío, lista `[]` o un 0 que significa «sin dato». Contando las cuatro formas (Figura 1): `user_score` 99.9 %, tiempos de juego 94–99 %, `metacritic_score` 97 %, `peak_ccu` 87 %, `recommendations` 85 %, `full_audio_languages` 79 %, `achievements` 18 %, `estimated_owners` 14 % y alrededor de 6 % en `developers`, `publishers`, `genres`, `categories` e idiomas (las mismas filas). Las columnas posteriores al lanzamiento son las más vacías.

**Filas que se eliminan** (tabla del embudo, `02_eda_embudo_filas.csv`):

| Paso | Juegos |
|---|---:|
| Archivo congelado | 151,023 |
| Fecha de lanzamiento inválida | −82 |
| Precio atípico (2 registros de 107,500 USD, ambos de 2026) | −2 |
| No son videojuegos (software, video) | −1,555 |
| **Universo limpio (todos los años)** | **149,384** |
| Lanzados después de 2024 (D-002) | −53,480 |
| **Universo hasta 2024** | **95,904** |
| Con menos de 50 reseñas | −67,196 |
| **Muestra de modelado** | **28,708** |

Otros precios altos (16,000 y 1,900 USD) son de 2025–2026 y D-002 los excluye de todos modos.

**Formato mixto.** `genres` y `categories` vienen como lista de textos u objetos con `description`; el cambio ocurre alrededor de 2019–2020. Es un artefacto de la recolección: la diferencia de `pct_pos` entre formatos (0.759 contra 0.824) casi desaparece al comparar dentro del mismo año (diferencia de +0.007). Decisión: leerlos con `parsers.aLista` y no usar el formato como variable (Figura 2).

**Idiomas.** `supported_languages` trae, en 28,319 juegos, un solo texto HTML con marcas (y un asterisco para el doblaje completo) o con comas. Se resuelve con `parsers.idiomasYAudio`; sin esa corrección, esos juegos contarían como si tuvieran un solo idioma.

## 3. Variable objetivo y muestra

**Objetivo.** `pct_pos = positive / (positive + negative)`, definido solo con reseñas. El 21 % del universo hasta 2024 no tiene ninguna.

**Umbral mínimo de reseñas** (`02_eda_umbrales.csv`, Figura 3):

| Umbral | Juegos hasta 2024 | % del universo | Desv. de pct_pos |
|---:|---:|---:|---:|
| 1 | 75,799 | 79.0 | 0.238 |
| 10 | 52,663 | 54.9 | 0.180 |
| 30 | 35,378 | 36.9 | 0.162 |
| **50** | **28,708** | **29.9** | **0.156** |
| 100 | 21,424 | 22.3 | 0.148 |
| 500 | 9,961 | 10.4 | 0.130 |

La dispersión cae con rapidez hasta unas 50 reseñas; después mejora poco y la muestra se reduce. Propuesta: 50 como valor principal y sensibilidad a 30 y 100.

**Distribución.** En la muestra, media 0.782, mediana 0.817, desviación 0.156, asimetría −1.06; el 5 % de los juegos está por debajo de 0.47 y el 5 % superior por encima de 0.97. Es asimétrica a la izquierda: conviene reportar MAE además de RMSE.

**Tres definiciones de éxito** (Figura 4). `pct_pos` y el límite inferior de Wilson casi coinciden con ≥50 reseñas (Spearman 0.974); el percentil por cohorte elimina la tendencia temporal por construcción. Propuesta: `pct_pos` como objetivo principal y la etiqueta de «cuartil superior de su cohorte» (25 % de la muestra) como objetivo de clasificación secundario.

**Sesgo de selección** (Figura 5). La oferta crece de 2,461 lanzamientos en 2015 a 19,748 en 2024, pero la proporción que llega a 50 reseñas cae de 77 % a 16 %. La muestra describe juegos que lograron cierta tracción, no el catálogo completo; es una limitación que debe declararse. Excluir 2025–2026 elimina casi todos los juegos con menos de 12 meses, por lo que D-002 cubre la regla de antigüedad mínima. El 79 % de la muestra tiene 4 años o más.

## 4. Deriva temporal y partición

La media de `pct_pos` por año de lanzamiento sube de 0.713 (2014) a 0.834 (2024) (Figura 6). Una partición aleatoria mezclaría épocas y sobreestimaría el desempeño, así que se propone partición temporal 70/15/15 por fecha de lanzamiento:

| Conjunto | Juegos | Desde | Hasta | Media |
|---|---:|---|---|---:|
| Train | 20,098 | 1997-06-30 | 2021-11-01 | 0.764 |
| Valid | 4,311 | 2021-11-02 | 2023-08-02 | 0.815 |
| Test | 4,299 | 2023-08-03 | 2024-12-31 | 0.831 |

Predecir la media del train en el test da RMSE = 0.150 con un sesgo de +0.067; la desviación del test es 0.135. Cualquier modelo debe superar estas referencias, y el sesgo debe reportarse. La «tasa base de la cohorte» (hipótesis nula) se evalúa con la media del año anterior, no con la del propio año.

## 5. Predictores disponibles antes del lanzamiento

Las comparaciones usan la muestra (≥50 reseñas, hasta 2024) y `dif_cohorte` (diferencia contra la media de su año). Valores positivos indican mejor recepción que su cohorte.

- **Precio (Figura 7).** Relación no lineal (H3): 5–20 USD por encima de su cohorte (+0.012 a +0.016), menos de 5 USD y gratis alrededor de −0.01, y 40 USD o más en −0.027. Spearman entre log-precio y `dif_cohorte`: +0.044. Es el precio actual, no el del lanzamiento.
- **Plataformas y mes (Figura 8).** Casi todo es Windows (100 % en la muestra). Mac y Linux se asocian con mejor recepción (+0.052 y +0.053 en `dif_cohorte`; Spearman ≈ 0.15), por lo que H6 («la plataforma aporta poco») no se sostiene; probablemente son un proxy del esfuerzo del estudio. El mes de lanzamiento varía poco (rango de 0.02).
- **Géneros (Figura 9).** 33 géneros tras normalizar. *Massively Multiplayer* (−0.108) y *Early Access* (−0.068) son los más rezagados; *Casual* (+0.010) el mejor entre los frecuentes. *Early Access* y *Free To Play* se comportan distinto del tipo de juego, lo que respalda separar marketing de género. El número de géneros por juego se asocia negativamente con la recepción (Spearman −0.12).
- **Categorías (Figura 10).** 66 categorías, 36 con al menos 1 % de los juegos. Mejor: *Remote Play on TV* (+0.056), *Steam Workshop*, *Steam Leaderboards*, *Steam Cloud*, *Full controller support*. Peor: *Online Co-op* y *Online PvP* (−0.041), *PvP* y *Multi-player* (H5). *Steam Trading Cards* se excluye porque Steam la activa según las ventas.
- **Idiomas (Figura 11).** Una vez contados correctamente (143 idiomas base, pendientes de normalizar nombres traducidos), la asociación con la recepción es débil: Spearman +0.055 con `pct_pos` y +0.011 con `dif_cohorte`. H4 solo se sostiene de forma leve (11 o más idiomas: +0.010 contra −0.004 para 1 idioma).
- **Ficha.** Tener logros: +0.044 sobre no tenerlos. Sitio web, URL de soporte, correo y aviso adulto: diferencias menores a 0.02.

## 6. Historial del desarrollador y del publisher (Figura 12)

El nombre no se usa (94,211 desarrolladores y 79,912 publishers, casi todos con un solo juego). Se derivan variables del historial **solo con el pasado** y, además, **solo con juegos con al menos 12 meses de antigüedad**, porque las reseñas de un juego reciente siguen acumulándose después de su lanzamiento.

| Variable | Con juegos previos | Con historial calificado | Spearman vs `pct_pos` |
|---|---:|---:|---:|
| Desarrollador, sin regla de madurez | 46.5 % | 42.1 % | 0.540 |
| **Desarrollador, 12 meses de madurez** | 46.5 % | 32.5 % | **0.475** |
| Publisher, 12 meses de madurez | 59.1 % | 46.1 % | 0.451 |

Es el predictor con mayor asociación (H1; Spearman con `dif_cohorte` de 0.43), pero solo el 33 % de la muestra tiene historial calificado. La regla de madurez baja la correlación y la cobertura: es el costo de evitar fuga. Los juegos sin historial (*cold start*) necesitan un indicador. El historial del publisher y el del desarrollador son muy parecidos (Spearman 0.82). El 63 % de los juegos está autopublicado. Se reportará el modelo con y sin esta variable, y se evaluará también con partición agrupada por desarrollador.

## 7. Auditoría de fuga (variables POST, Figura 13)

Spearman con `pct_pos` entre los juegos de la muestra: `metacritic_score` 0.58 (13.8 % de cobertura), `recommendations` 0.22, `peak_ccu` 0.15, `estimated_owners` 0.14 y tiempos de juego cerca de 0. `user_score` correlaciona 0.997, pero existe en apenas 0.2 % de los juegos. Se excluyen todas como predictoras (solo `positive` y `negative` construyen el objetivo), y también `tags` y `dlc_count`.

## 8. Variables «Pre\*» (Figura 14)

El valor guardado es el de la tienda al 24-nov-2026, no el del lanzamiento. Si los juegos exitosos reciben después traducciones y contenido, la señal podría ser consecuencia del éxito. Resultado por año de lanzamiento (todos los juegos 2012 → 2024):

| Variable | 2012 | 2024 |
|---|---:|---:|
| Precio mediano (USD) | 9.99 | 3.99 |
| % de juegos gratuitos | 6.9 | 26.1 |
| Idiomas (promedio) | 4.35 | 7.06 |
| Categorías (promedio) | 5.45 | 3.63 |
| % con sitio web | 88.7 | 29.6 |

Las categorías, los logros y el sitio web son más frecuentes en los juegos viejos (posible acumulación posterior o supervivencia de los títulos que siguen en la tienda); los idiomas y los juegos gratuitos aumentan en los recientes. En todos los casos hay un efecto de época que se controla en parte comparando contra la cohorte. La valoración definitiva del riesgo es la **ablación** (modelo con y sin Pre\*) del Sprint 2.

## 9. Relaciones entre predictores (Figura 15)

Los pares más correlacionados son `log_precio` con `precio_pct_cohorte` (0.98) y el historial del desarrollador con el del publisher (0.82); hay que elegir cuál conservar. Correlación con `dif_cohorte`: historial del desarrollador 0.43, historial del publisher 0.40, Mac 0.17, Linux 0.15, logros 0.12, número de géneros −0.12 y el resto menor a 0.1.

## 10. Hallazgos y decisiones

La tabla completa de 17 hallazgos con su evidencia y la decisión para el pipeline está en `reports/metrics/02_eda_hallazgos.md` (y al final del notebook). Los puntos principales:

1. Una sola versión de datos congelada.
2. Muestra de 28,708 juegos (≥50 reseñas, hasta 2024); sensibilidad a 30 y 100.
3. Objetivo `pct_pos`; la partición debe ser temporal porque la recepción sube con los años.
4. Historial del desarrollador con regla de madurez de 12 meses: la señal más fuerte, con cobertura limitada.
5. Excluir todas las variables POST.
6. Variables Pre\* con reserva y ablación en el Sprint 2.
7. Mac, Linux, logros, categorías de calidad de producto y mercado multijugador en línea: señales moderadas; idiomas y mes: débiles.

## 11. Limitaciones

- Asociación, no causalidad: son datos observacionales de una sola fotografía de la tienda.
- Sesgo de selección: la muestra solo incluye juegos con al menos 50 reseñas.
- No hay seguidores, listas de deseos, presupuesto de marketing ni búsquedas previas, que la literatura señala como predictores importantes.
- Las variables Pre\* reflejan el valor actual de la tienda.
- `tags` de usuarios y texto de descripciones no se usan (fuga y D-007).

## 12. Pendientes

- Cerrar las decisiones 0001 (objetivo), 0002 (umbral) y 0003 (partición).
- Auditar con la tienda una muestra de juegos de 2021–2024 con cero reseñas.
- Normalizar los nombres de idiomas traducidos (Luis).
- Idiomas como «mercado potencial» (número de hablantes): extensión opcional.
