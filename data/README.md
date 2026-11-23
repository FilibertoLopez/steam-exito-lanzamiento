# Datos

## Fuente

- **Conjunto:** Steam Games Dataset (Kaggle), con estimaciones de SteamSpy.
- **URL:** _pendiente_
- **Fecha de descarga:** _pendiente_
- **Licencia:** _pendiente_

## Carpetas

| Carpeta | Contenido | ¿Se versiona? |
|---|---|---|
| `raw/` | Archivos originales sin modificar | No |
| `interim/` | Resultados intermedios de limpieza | No |
| `processed/` | Datos listos para modelar | No |
| `sample/` | Muestra pequeña con semilla fija (también para R/Positron) | Sí |

## Descarga

```bash
# Ejemplo con la CLI de Kaggle
kaggle datasets download -d <usuario>/<dataset> -p data/raw --unzip
```

## Partición

Los índices de entrenamiento / validación / prueba se guardan en `data/processed/` con semilla fija para garantizar reproducibilidad y evitar fuga de información.
