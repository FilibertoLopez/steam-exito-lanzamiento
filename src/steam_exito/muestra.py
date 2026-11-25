"""Variable objetivo y definición de la muestra. Responsable: Alejandra. Issues: S1-10 a S1-12."""
import pandas as pd

from steam_exito import config
from steam_exito.contrato import bloqueVariables, pasoLimpieza


@bloqueVariables("y_", permitirPost=True)
def construirObjetivo(df: pd.DataFrame, umbral: int = config.UMBRAL_RESENAS) -> pd.DataFrame:
    """Calcula TODAS las variantes del objetivo (decisión 0001 abierta). Índice app_id.

    - ``y_n_resenas``: positive + negative.
    - ``y_pct_pos``: positive / (positive + negative); NaN si no hay reseñas (nunca 0).
    - ``y_wilson_inf``: límite inferior del intervalo de Wilson al 95 %.
    - ``y_pct_cohorte``: percentil (0-1) de ``y_pct_pos`` dentro del año de lanzamiento, calculado
      solo entre juegos con >= ``umbral`` reseñas.
    - ``y_bueno``: 1 si está en el cuartil superior de su cohorte, 0 si no; NaN si no elegible.
    Es el ÚNICO bloque que puede usar positive/negative. Issue: S1-10.
    """
    raise NotImplementedError("Pendiente: Alejandra (S1-10)")


@pasoLimpieza("muestra")
def filtrarMuestra(df: pd.DataFrame, umbral: int = config.UMBRAL_RESENAS,
                   anioMax: int = config.ANIO_MAX, anioMin=config.ANIO_MIN) -> pd.DataFrame:
    """Filtra la tabla unificada a la muestra de modelado (D-002, D-008).

    Conserva juegos con ``y_n_resenas >= umbral`` y año de lanzamiento en [anioMin, anioMax]
    (anioMin=None = sin límite inferior). Sin pesos. Con los datos congelados debe dar 28,708 juegos. Issue: S1-11.
    """
    raise NotImplementedError("Pendiente: Alejandra (S1-11)")


def sensibilidadMuestra(df: pd.DataFrame, umbrales=config.UMBRALES_SENSIBILIDAD,
                        aniosMin=(None, config.ANIO_MIN_SENSIBILIDAD)) -> pd.DataFrame:
    """Tabla (A-003): para cada combinación umbral x año mínimo, # de juegos, media y desviación
    de ``y_pct_pos`` y % de la base. No es un bloque ni un paso: devuelve una tabla para el
    reporte y se guarda en ``reports/metrics/``. Issue: S1-12.
    """
    raise NotImplementedError("Pendiente: Alejandra (S1-12)")
