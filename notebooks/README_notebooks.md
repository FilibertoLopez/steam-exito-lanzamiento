# Notebooks

Ejecutar en orden numérico. Cada notebook exporta sus figuras a `reports/figures/` y sus métricas a `reports/metrics/`.

- Los notebooks numerados se versionan **con** resultados para que las gráficas se vean en GitHub.
- Los de `borradores/` se versionan sin resultados (`nbstripout`).
- Los notebooks son delgados: importan de `src/steam_exito/` y solo orquestan, grafican y comentan.

## Datos

Todos los notebooks usan la **versión congelada del 2026-11-24** (151,023 filas × 33 columnas). Se cargan con `steam_exito.carga.cargarSlim()` y se comprueban con `verificarVersion()`. Cómo obtener el archivo: [`data/README.md`](../data/README.md).

No se debe volver a descargar el CSV público de Kaggle para las cifras finales: cambia todos los días.

## Análisis exploratorio

Documento: [`docs/03-analisis-exploratorio.md`](../docs/03-analisis-exploratorio.md).

| Notebook | Contenido |
|---|---|
| `02_eda.ipynb` | EDA unificado: calidad, variable objetivo y muestra, deriva temporal, predictores, historial del desarrollador, auditoría de fuga y hallazgos. Figuras `reports/figures/02_eda_*.png` y tablas `reports/metrics/02_eda_*.csv` |
| `02a_antiguedad_resenas.ipynb` | Antigüedad vs volumen de reseñas |
| `02b_percentiles_cohorte.ipynb` | Percentiles dentro de la cohorte de lanzamiento |
| `02c_resenas_genero_categoria.ipynb` | Mediana de reseñas por género y categoría |
| `02d_evolucion_top100.ipynb` | Evolución mensual del top 100 por recomendaciones |

Pendiente (acuerdo A-012): `02a` a `02d` todavía leen la descarga del 2026-11-19 y deben adaptarse a `cargarSlim()` y a la fecha de corte de `config.VERSION_DATOS`. `02d` reutiliza `data/interim/top100.csv` y `hist.csv` (descargados de Steam el 2026-11-22); cambia `descargarHistorial = True` para volver a consultar Steam, y los datos cambiarán.

## Limpieza y variables (Sprint 1)

| Notebook | Contenido | Responsable |
|---|---|---|
| `03_limpieza.ipynb` | Embudo de filas, antes y después, figuras de calidad | Filiberto (S1-14) |
| `04_ingenieria_variables.ipynb` | Columnas por bloque y correlaciones del resultado | Filiberto (S1-14) |
