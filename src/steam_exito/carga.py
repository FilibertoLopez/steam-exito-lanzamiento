"""Carga de datos crudos, intermedios y procesados, y verificación de la versión congelada.

``cargarSlim`` entiende tres formas de tener los datos en ``data/raw`` (en este orden):

1. ``steam_games_slim.parquet``: el archivo congelado del equipo (versión del 24-nov-2026).
2. ``steam_parte_*.parquet``: el mismo archivo partido en varias partes.
3. ``steam_games.csv``: el CSV público de Kaggle. OJO: Kaggle lo actualiza a diario, así que NO es la
   versión congelada (las cifras pueden diferir un poco). Se avisa con una advertencia.
"""
import hashlib
import warnings
from pathlib import Path

import pandas as pd

from steam_exito import config
from steam_exito.config import DATA_DIR

NOMBRE_SLIM = "steam_games_slim.parquet"
PATRON_PARTES = "steam_parte_*.parquet"
NOMBRE_CSV = "steam_games.csv"

# Columnas de texto pesado que el proyecto no usa (se descartan al leer el CSV de Kaggle)
COLUMNAS_PESADAS = [
    "about_the_game", "detailed_description", "short_description", "header_image",
    "screenshots", "movies", "packages", "tags", "metacritic_url",
]
# Texto que solo interesa como indicador "tiene / no tiene"
TEXTO_A_INDICADOR = {
    "website": "has_website", "support_url": "has_support_url",
    "support_email": "has_support_email", "notes": "has_notes",
}


def cargarCrudos(nombreArchivo: str) -> pd.DataFrame:
    """Lee un archivo de data/raw."""
    ruta = DATA_DIR / "raw" / nombreArchivo
    if ruta.suffix == ".json":
        return pd.read_json(ruta)
    if ruta.suffix == ".parquet":
        return pd.read_parquet(ruta)
    return pd.read_csv(ruta)


def _aIndicadores(df: pd.DataFrame) -> pd.DataFrame:
    """Convierte website/support_url/support_email/notes en indicadores has_* (si vienen como texto)."""
    df = df.copy()
    for origen, destino in TEXTO_A_INDICADOR.items():
        if origen in df.columns:
            tiene = df[origen].notna() & df[origen].astype("string").str.strip().ne("").fillna(False)
            df[destino] = tiene.astype("boolean")
            df = df.drop(columns=origen)
    return df


def cargarDesdeCsv(ruta) -> pd.DataFrame:
    """Lee el CSV público de Kaggle y lo deja con la misma forma que el parquet slim.

    Descarta las columnas pesadas y convierte el texto de sitio/soporte en indicadores has_*.
    """
    df = pd.read_csv(ruta, usecols=lambda c: c not in COLUMNAS_PESADAS,
                     dtype={"release_date": "string"}, low_memory=False)
    return _aIndicadores(df)


def cargarSlim(carpeta=None) -> pd.DataFrame:
    """Carga los datos del proyecto desde ``data/raw`` (o ``carpeta``). Ver el docstring del módulo."""
    carpeta = Path(carpeta) if carpeta else DATA_DIR / "raw"
    unico = carpeta / NOMBRE_SLIM
    if unico.exists():
        return _aIndicadores(pd.read_parquet(unico))
    partes = sorted(carpeta.glob(PATRON_PARTES))
    if partes:
        return _aIndicadores(pd.concat([pd.read_parquet(p) for p in partes], ignore_index=True))
    csv = carpeta / NOMBRE_CSV
    if csv.exists():
        warnings.warn(
            f"Se leyó {NOMBRE_CSV} de Kaggle. Esa descarga se actualiza a diario y puede NO ser la versión "
            f"congelada del equipo ({config.VERSION_DATOS['fecha_descarga']}); las cifras pueden diferir.")
        return cargarDesdeCsv(csv)
    raise FileNotFoundError(
        f"No se encontró {NOMBRE_SLIM}, {PATRON_PARTES} ni {NOMBRE_CSV} en {carpeta}. "
        "Descarga los datos de Kaggle (ver data/README.md)."
    )


def huellaAppId(df: pd.DataFrame) -> str:
    """SHA-256 de los app_id ordenados: identifica la versión sin depender de cómo se guardó."""
    texto = ",".join(map(str, sorted(df["app_id"].tolist())))
    return hashlib.sha256(texto.encode()).hexdigest()


def verificarVersion(df: pd.DataFrame, estricto: bool = True) -> bool:
    """Comprueba que ``df`` es la versión congelada (A-005). Falla (o avisa si estricto=False)."""
    esperado = config.VERSION_DATOS
    ok = len(df) == esperado["filas"] and huellaAppId(df) == esperado["huella_app_id"]
    if not ok:
        mensaje = (
            f"Los datos no coinciden con la versión congelada ({esperado['fecha_descarga']}, "
            f"{esperado['filas']:,} filas). Se leyeron {len(df):,} filas. Las cifras del EDA y del reporte "
            "se calcularon con la versión congelada; con otra descarga pueden variar. "
            "Para reproducirlas usa el parquet del equipo (ver data/README.md)."
        )
        if estricto:
            raise ValueError(mensaje)
        warnings.warn(mensaje)
    return ok


def guardarProcesado(df: pd.DataFrame, nombre: str, carpeta: str = "processed") -> Path:
    """Guarda un parquet en data/processed (o data/interim). No se versiona."""
    ruta = DATA_DIR / carpeta / f"{nombre}.parquet"
    ruta.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(ruta)
    return ruta
