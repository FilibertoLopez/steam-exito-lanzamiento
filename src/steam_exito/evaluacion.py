"""Particiones, métricas y comparación de modelos (ver docs/07). Responsable: Alejandra."""
import pandas as pd

from steam_exito import config


def particionTemporal(df: pd.DataFrame, fraccionTrain: float = config.FRACCION_TRAIN,
                      fraccionValid: float = config.FRACCION_VALID) -> pd.Series:
    """Asigna 'train' / 'valid' / 'test' por fecha de lanzamiento (decisión 0003). Issue: S1-13.

    Ordena por ``release_date`` y corta por cuantiles; juegos con la misma fecha van al mismo
    conjunto. Devuelve una Serie indexada por ``app_id``. Debe guardar las fechas de corte en
    ``reports/metrics/``. No usa aleatoriedad. El EDA propone cortes 2021-11-01 y 2023-08-02.
    """
    raise NotImplementedError("Pendiente: Alejandra (S1-13)")
