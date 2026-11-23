"""Reglas de limpieza (ver docs/04-estrategia-limpieza.md)."""
import pandas as pd


def reportarFaltantes(df: pd.DataFrame) -> pd.DataFrame:
    """Tabla con conteo y porcentaje de faltantes por columna."""
    conteo = df.isna().sum()
    return pd.DataFrame({"faltantes": conteo, "porcentaje": 100 * conteo / len(df)}).sort_values("porcentaje", ascending=False)
