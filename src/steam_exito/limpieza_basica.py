"""Limpieza básica: tipos, fechas, precios y valores "sin dato". Responsable: Filiberto.

Son pasos ``df -> df`` (decorador ``pasoLimpieza``). Se ejecutan en este orden por el pipeline:
convertirTipos -> limpiarFechas -> limpiarPrecios -> marcarSinDato.
"""
import pandas as pd

from steam_exito.contrato import pasoLimpieza


@pasoLimpieza("tipos")
def convertirTipos(df: pd.DataFrame) -> pd.DataFrame:
    """Asigna los tipos correctos sin quitar filas.

    - ``mac``, ``linux``, ``windows``: booleano anulable (usa ``parsers.aBooleano``); los 14 vacíos
      quedan como <NA>.
    - ``achievements``: entero anulable (viene como decimal).
    - ``price``, ``positive``, ``negative``: numéricos.
    Issue: S1-01.
    """
    raise NotImplementedError("Pendiente: Filiberto (S1-01)")


@pasoLimpieza("fechas")
def limpiarFechas(df: pd.DataFrame) -> pd.DataFrame:
    """Convierte ``release_date`` a datetime y elimina las filas con fecha inválida (82).

    También elimina fechas posteriores a ``config.VERSION_DATOS['fecha_max_lanzamiento']``.
    NO filtra por año: el filtro D-002 lo aplica ``muestra.filtrarMuestra``. Issue: S1-01.
    """
    raise NotImplementedError("Pendiente: Filiberto (S1-01)")


@pasoLimpieza("precios")
def limpiarPrecios(df: pd.DataFrame) -> pd.DataFrame:
    """Elimina los registros con precio atípico (D-004: ``price > config.PRECIO_MAX_VALIDO``; son 2).

    Reglas: precio negativo -> error; precio nulo se conserva (juegos retirados,
    ``price_status == 'unavailable'``); ``price == 0`` es gratis y es un valor real. Issue: S1-01.
    """
    raise NotImplementedError("Pendiente: Filiberto (S1-01)")


@pasoLimpieza("sin_dato")
def marcarSinDato(df: pd.DataFrame) -> pd.DataFrame:
    """Convierte a nulo los valores que significan "sin dato" (docs/02-diccionario-datos.md).

    - ``config.COLUMNAS_CERO_ES_NULO``: 0 -> NaN.
    - ``estimated_owners``: '0 - 0' y '0 .. 0' -> NaN.
    - ``config.COLUMNAS_LISTA``: '[]', '' y espacios -> NaN (``parsers.esVacio``).
    - NO tocar ``full_audio_languages`` ([] = sin doblaje es un valor real) ni ``positive``/
      ``negative``/``achievements``/``price`` (el 0 es real).
    Devuelve las mismas filas. Issue: S1-01.
    """
    raise NotImplementedError("Pendiente: Filiberto (S1-01)")
