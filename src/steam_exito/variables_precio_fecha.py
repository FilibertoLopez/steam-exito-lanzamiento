"""Variables de precio y de fecha. Responsable: Filiberto. Issue: S1-02.

Precio: la columna ``price`` es el precio ACTUAL (Pre*), no el del lanzamiento (D-010).
Por eso se ofrecen versiones relativas a la cohorte, menos sensibles a inflación y rebajas.

Son bloques de variables (decorador ``bloqueVariables``): reciben el DataFrame limpio, con
``price`` numérico y ``release_date`` como fecha (S1-01), y devuelven un DataFrame indexado
por ``app_id`` con una fila por juego de la entrada.
"""
import numpy as np
import pandas as pd

from steam_exito import config
from steam_exito.contrato import bloqueVariables


def _indiceAppId(df: pd.DataFrame) -> pd.Index:
    """Índice ``app_id`` con el mismo orden que la entrada."""
    return pd.Index(df["app_id"].to_numpy(), name="app_id")


@bloqueVariables("precio_")
def variablesPrecio(df: pd.DataFrame) -> pd.DataFrame:
    """Columnas esperadas (índice app_id):

    - ``precio_log``: log1p(price); NaN si no hay precio.
    - ``precio_es_gratis``: price == 0 (booleano); False si no hay precio.
    - ``precio_sin_dato``: price nulo (juego retirado), booleano.
    - ``precio_rango``: 0 gratis, 1 (0,5], 2 (5,10], 3 (10,20], 4 (20,40], 5 >40 (entero
      anulable; <NA> si no hay precio). Los cortes viven en ``config.CORTES_PRECIO``.
    - ``precio_pct_cohorte``: percentil (0-1] del precio dentro de su año de lanzamiento; los
      empates (p. ej., los juegos gratis) reciben el rango promedio. NaN si no hay precio.

    El año de lanzamiento solo se usa para agrupar la cohorte; no se devuelve (D-013).

    Recomendación: ``precio_log`` y ``precio_pct_cohorte`` tienen correlación ~0.98 (Spearman
    0.982 en la muestra). Se recomienda conservar ``precio_pct_cohorte`` como variable principal,
    porque absorbe la deriva del precio por época (mediana de 9.99 USD en 2012 contra 3.99 USD
    en 2024, EDA §8), y usar ``precio_log`` en el baseline lineal y en la ablación con y sin Pre*
    del Sprint 2. La decisión final es del equipo.
    """
    precio = df["price"].astype("Float64")
    anio = df["release_date"].dt.year
    rango = np.searchsorted(config.CORTES_PRECIO, precio.fillna(-1).to_numpy(dtype=float), side="left")
    salida = pd.DataFrame({
        "precio_log": np.log1p(precio.astype(float)),
        "precio_es_gratis": (precio == 0).fillna(False).astype(bool),
        "precio_sin_dato": precio.isna().astype(bool),
        "precio_rango": pd.Series(rango, index=df.index).astype("Int64").mask(precio.isna()),
        "precio_pct_cohorte": precio.astype(float).groupby(anio).rank(pct=True),
    })
    salida.index = _indiceAppId(df)
    return salida


@bloqueVariables("fecha_")
def variablesFecha(df: pd.DataFrame) -> pd.DataFrame:
    """Calendario de lanzamiento (índice app_id):

    - ``fecha_mes``: 1 a 12 (entero anulable).
    - ``fecha_dia_semana``: 0 lunes ... 6 domingo (entero anulable).
    - ``fecha_mes_sin``, ``fecha_mes_cos``: codificación cíclica del mes,
      sin/cos(2*pi*(mes - 1)/12), para que diciembre quede junto a enero.
    - ``fecha_es_fin_de_semana``: sábado o domingo (booleano).

    PROHIBIDO devolver año o antigüedad: el test cae en años que el modelo no vio y un juego
    nuevo siempre tiene antigüedad cero al lanzamiento.
    """
    fecha = df["release_date"]
    mes, diaSemana = fecha.dt.month, fecha.dt.day_of_week
    angulo = 2 * np.pi * (mes - 1) / 12
    salida = pd.DataFrame({
        "fecha_mes": mes.astype("Int64"),
        "fecha_dia_semana": diaSemana.astype("Int64"),
        "fecha_mes_sin": np.sin(angulo),
        "fecha_mes_cos": np.cos(angulo),
        "fecha_es_fin_de_semana": (diaSemana >= 5).astype(bool),
    })
    salida.index = _indiceAppId(df)
    return salida
