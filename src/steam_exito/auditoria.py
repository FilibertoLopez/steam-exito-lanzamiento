"""Auditoría de variables Pre* (D-010). Responsable: Diana. Issue: S1-09.

Las variables Pre* tienen el valor ACTUAL de la tienda, no el del día del lanzamiento. Si los juegos
exitosos acumulan traducciones, tráileres o rebajas con el tiempo, el modelo podría "aprender" el
éxito en lugar de predecirlo. Esta auditoría lo mide; la ablación (con/sin Pre*) es del Sprint 2.
"""
import pandas as pd


def auditarPreEstrella(df: pd.DataFrame) -> pd.DataFrame:
    """Tabla por año de lanzamiento (filas) con la media o tasa de cada variable Pre* disponible:
    precio mediano, % gratis, # idiomas, # idiomas con audio, # categorías, % con logros,
    % con sitio web, % con correo de soporte.

    El EDA (sección 8) ya contiene el prototipo; esta función lo industrializa. NO es un bloque de
    variables (no lleva decorador). Devuelve la tabla; el notebook la grafica y la guarda en
    ``reports/metrics/``.
    """
    raise NotImplementedError("Pendiente: Diana (S1-09)")
