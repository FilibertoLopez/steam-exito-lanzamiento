"""Historial de desarrolladores y publishers SIN FUGA. Responsable: Diana. Issues: S1-07, S1-08.

Regla de oro (A-004, D-006, D-009): para el juego J lanzado en la fecha F solo se puede usar
información de juegos lanzados antes de ``F - config.MESES_ANTIGUEDAD_HISTORIAL`` meses, porque
las reseñas de un juego reciente todavía no estaban maduras cuando salió J. Jamás se usa el
nombre del desarrollador como variable ni el valor del propio J.
El prototipo ``historialPrevio`` del notebook 02_eda.ipynb ya implementa la lógica vectorizada.
"""
import pandas as pd

from steam_exito import config
from steam_exito.contrato import bloqueVariables


@bloqueVariables("dev_")
def variablesDesarrollador(df: pd.DataFrame, mesesMinimos: int = config.MESES_ANTIGUEDAD_HISTORIAL,
                           umbralResenas: int = config.UMBRAL_RESENAS) -> pd.DataFrame:
    """Columnas esperadas (índice app_id). Con varios desarrolladores, agrega TODOS (no solo el primero).

    - ``dev_n_previos``: juegos del desarrollador lanzados antes de la fecha (máximo entre sus
      desarrolladores); los del mismo día no cuentan entre sí.
    - ``dev_n_previos_maduros``: de esos, los lanzados con >= ``mesesMinimos`` de anticipación.
    - ``dev_pct_pos_previo``: promedio de la proporción positiva de los previos maduros con
      >= ``umbralResenas`` reseñas; NaN si no hay.
    - ``dev_sin_historial``: indicador (cold start, sin previos maduros con calificación).
    - ``dev_n_juegos_total``: NO se permite (usa el futuro).
    Debe incluir una prueba que verifique que cambiar el pct_pos de un juego FUTURO no altera la
    variable de uno anterior.
    """
    raise NotImplementedError("Pendiente: Diana (S1-07)")


@bloqueVariables("pub_")
def variablesPublisher(df: pd.DataFrame, mesesMinimos: int = config.MESES_ANTIGUEDAD_HISTORIAL,
                       umbralResenas: int = config.UMBRAL_RESENAS) -> pd.DataFrame:
    """Mismas reglas que ``variablesDesarrollador`` para ``publishers`` (prefijo ``pub_``) más:

    - ``pub_es_autopublicado``: algún desarrollador es también publisher (booleano).
    - ``pub_n_publicados_previos``: juegos previos del publisher.
    Control del efecto "fama" (D-009). Issue: S1-08.
    """
    raise NotImplementedError("Pendiente: Diana (S1-08)")
