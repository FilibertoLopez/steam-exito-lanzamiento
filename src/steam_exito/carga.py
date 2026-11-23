"""Carga de datos crudos, intermedios y procesados."""
from pathlib import Path

import pandas as pd

ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT_DIR / "data"


def cargarCrudos(nombreArchivo: str) -> pd.DataFrame:
    """Lee un archivo de data/raw."""
    ruta = DATA_DIR / "raw" / nombreArchivo
    if ruta.suffix == ".json":
        return pd.read_json(ruta)
    return pd.read_csv(ruta)
