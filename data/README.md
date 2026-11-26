# Datos

## Fuente

- **Conjunto:** Steam Games Dataset – All Games (Kaggle), con estimaciones de SteamSpy.
- **Autor:** Hubert Sidorowicz · **Licencia:** MIT
- **URL:** <https://www.kaggle.com/datasets/hubertsidorowicz/steam-games-dataset-daily-updates>
- **Frecuencia de actualización:** diaria. **Por eso el proyecto trabaja con una versión congelada** (acuerdo A-005).

## Versión congelada del proyecto

| Atributo | Valor |
|---|---|
| Fecha de descarga | 2026-11-24 |
| Última fecha de lanzamiento en los datos | 2026-11-24 |
| Filas × columnas | 151,023 × 33 (42 originales menos 9 columnas pesadas) |
| SHA-256 del parquet original | `eb64467236ae174808e76ff94e8f9304bcc0ad7faec756c2bc9099cb49431992` |
| Huella de `app_id` (verifica la versión) | `337e875fa555995e2668a38019fe3c5bb4567418c2e92dd09c166d0a9c9d0cd3` |

El archivo "slim" quita `about_the_game`, `detailed_description`, `short_description`, `header_image`,
`screenshots`, `movies`, `packages`, `tags` y `metacritic_url`; y convierte `website`, `support_url`,
`support_email` y `notes` en indicadores `has_*`. Se compartió en 8 partes (`steam_parte_1..8.parquet`).

`carga.verificarVersion()` falla si el archivo no coincide con la versión congelada. **No se debe volver a
descargar el dataset de Kaggle**: cambia todos los días y rompería la reproducibilidad.

## Carpetas

| Carpeta | Contenido | ¿Se versiona? |
|---|---|---|
| `raw/` | `steam_games_slim.parquet` o las partes `steam_parte_*.parquet` | Sí (8 archivos congelados) |
| `interim/` | Resultados intermedios de limpieza | No |
| `processed/` | Datos listos para modelar y partición | No |
| `sample/` | Muestra pequeña con semilla fija | Sí |

## Cómo obtener los datos

`carga.cargarSlim()` busca en `data/raw/`, en este orden: `steam_games_slim.parquet`, `steam_parte_*.parquet` y
`steam_games.csv`. Elige **una** de estas formas.

### Opción 1 (recomendada): el parquet congelado desde un dataset privado de Kaggle

Es la versión exacta con la que se calcularon todas las cifras del EDA.

1. **Quien tiene el archivo** (el notebook de Kaggle donde se creó `steam_games_slim.parquet`): *Output → New Dataset*,
   nombre `steam-games-slim`, visibilidad **Private**, y lo comparte con los demás integrantes.
2. **Cada quien** instala el cliente y su token (*Kaggle → Settings → API → Create New Token*; guarda `kaggle.json` en
   `~/.kaggle/` o, en Windows, `C:\Users\<usuario>\.kaggle\`):

```bash
pip install kaggle
kaggle datasets download -d <usuario-kaggle>/steam-games-slim -p data/raw --unzip
```

### Opción 2: el CSV público de Kaggle (versión distinta)

```bash
kaggle datasets download -d hubertsidorowicz/steam-games-dataset-daily-updates -p data/raw --unzip
```

Deja `data/raw/steam_games.csv`. `cargarSlim()` lo lee, descarta las columnas pesadas y crea los indicadores `has_*`.
**Advertencia:** ese conjunto se actualiza a diario, así que **no es la versión congelada**: los conteos pueden variar
(p. ej., la muestra de 28,708 juegos) y `verificarVersion()` avisará. Sirve para trabajar y probar, pero las cifras
finales del reporte deben salir de la Opción 1.

### Comprobar la versión

```bash
python -c "from steam_exito.carga import cargarSlim, verificarVersion; verificarVersion(cargarSlim())"
```

## Partición

Los índices de entrenamiento / validación / prueba salen de `evaluacion.particionTemporal` (por fecha de
lanzamiento, sin aleatoriedad) y se guardan en `data/processed/`.
