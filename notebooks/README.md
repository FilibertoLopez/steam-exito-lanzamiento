# Notebooks

Ejecutar en orden numérico. Cada notebook exporta sus figuras a `reports/figures/` y sus métricas a `reports/metrics/`.

- Los notebooks numerados se versionan **con** resultados para que las gráficas se vean en GitHub.
- Los de `borradores/` se versionan sin resultados (`nbstripout`).

## Datos

Los notebooks buscan `steam_games.csv.gz` (versión del 2026-11-19) en este orden:

1. La ruta de la variable de entorno `STEAM_GAMES_CSV`.
2. `data/raw/steam_games.csv.gz` o `data/raw/steam_games.csv`.
3. `Proyecto Final/Datos/steam_games.csv.gz`, dos niveles arriba de la raíz del repositorio.

## Análisis exploratorio

Documento: [`docs/03-analisis-exploratorio.md`](../docs/03-analisis-exploratorio.md).

| Notebook | Contenido | Origen |
|---|---|---|
| `02_eda.ipynb` | Resumen del conjunto, ceros «sin dato», lanzamientos por año y variable objetivo | Nuevo |
| `02a_antiguedad_resenas.ipynb` | Antigüedad vs volumen de reseñas | Script `antiguedadVsResenas.py` (eliminado) |
| `02b_percentiles_cohorte.ipynb` | Percentiles dentro de la cohorte de lanzamiento | Script `percentilesPorCohorte.py` (eliminado) |
| `02c_resenas_genero_categoria.ipynb` | Mediana de reseñas por género y categoría | Script `medianaResenasPorGenero.py` (eliminado) |
| `02d_evolucion_top100.ipynb` | Evolución mensual del top 100 por recomendaciones | Script `evolucion_top100_recomendaciones.py` (eliminado) |

`02d` reutiliza `data/interim/top100.csv` y `hist.csv` (descargados de Steam el 2026-11-22). Cambia `descargarHistorial = True` para volver a consultar Steam; los datos cambiarán.
