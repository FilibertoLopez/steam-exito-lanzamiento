# Éxito de videojuegos en Steam: factores previos al lanzamiento

Proyecto Final de **Aprendizaje de Máquina** (Maestría en Ciencias de la Computación).

**Pregunta:** ¿qué factores, disponibles antes del lanzamiento, aumentan las posibilidades de éxito de un juego nuevo en Steam?

## Contenido

| Carpeta | Contenido |
|---|---|
| [`docs/`](docs/00-indice.md) | Documentación en Markdown (bóveda de Obsidian) |
| [`notebooks/`](notebooks/) | Notebooks de Jupyter con el análisis en Python |
| [`src/steam_exito/`](src/steam_exito/) | Funciones reutilizables |
| [`data/`](data/README.md) | Datos (solo muestra y documentación; los crudos no se versionan) |
| [`reports/`](reports/) | Figuras, métricas, presentación y conclusiones (PDF) |
| [`references/`](references/README.md) | Referencias bibliográficas y fichas de lectura |
| [`R/`](R/) | Exploración opcional en R / Positron |

## Reproducir

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
git lfs install && git lfs pull
```

Descarga los datos según [`data/README.md`](data/README.md) y ejecuta los notebooks en orden numérico.

## Flujo

```mermaid
flowchart LR
    A[Datos crudos] --> B[Perfilado y EDA]
    B --> C[Limpieza]
    C --> D[Ingeniería de variables]
    D --> E[Selección de variables]
    E --> F[Modelos base]
    F --> G[Ajuste de hiperparámetros]
    G --> H[Interpretación]
    H --> I[Conclusiones y presentación]
```
