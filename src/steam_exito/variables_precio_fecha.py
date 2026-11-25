"""Variables de precio y de fecha. Responsable: Filiberto. Issue: S1-02.

Precio: la columna ``price`` es el precio ACTUAL (Pre*), no el del lanzamiento (D-010).
Por eso se ofrecen versiones relativas a la cohorte, menos sensibles a inflación y rebajas.
"""
import pandas as pd

from steam_exito.contrato import bloqueVariables


@bloqueVariables("precio_")
def variablesPrecio(df: pd.DataFrame) -> pd.DataFrame:
    """Columnas esperadas (índice app_id):

    - ``precio_log``: log1p(price); NaN si no hay precio.
    - ``precio_es_gratis``: price == 0 (booleano).
    - ``precio_sin_dato``: price nulo (juego retirado), booleano.
    - ``precio_rango``: 0 gratis, 1 (0,5], 2 (5,10], 3 (10,20], 4 (20,40], 5 >40 (entero).
    - ``precio_pct_cohorte``: percentil (0-1) del precio dentro de su año de lanzamiento.
    Nota: ``precio_log`` y ``precio_pct_cohorte`` tienen correlación ~0.98; el equipo decide cuál conservar.
    """
    raise NotImplementedError("Pendiente: Filiberto (S1-02)")


@bloqueVariables("fecha_")
def variablesFecha(df: pd.DataFrame) -> pd.DataFrame:
    """Calendario de lanzamiento: ``fecha_mes``, ``fecha_dia_semana``, ``fecha_mes_sin``,
    ``fecha_mes_cos`` (codificación cíclica) y ``fecha_es_fin_de_semana``.

    PROHIBIDO devolver año o antigüedad: el test cae en años que el modelo no vio y un juego
    nuevo siempre tiene antigüedad cero al lanzamiento.
    """
    raise NotImplementedError("Pendiente: Filiberto (S1-02)")
