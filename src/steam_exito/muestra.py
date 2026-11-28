"""Variable objetivo y definición de la muestra. Responsable: Alejandra. Issues: S1-10 a S1-12."""
import numpy as np
import pandas as pd

from steam_exito import config
from steam_exito.contrato import bloqueVariables, pasoLimpieza


def _agruparCohortes(anio: pd.Series) -> pd.Series:
    """Agrupa los años iniciales con pocos juegos en una sola cohorte "<= año" (como el EDA 02b).

    Un año es "pequeño" si tiene menos de ``config.COHORTE_MIN_JUEGOS`` juegos. Se agrupan todos los
    años anteriores al primer año que sí alcanza el mínimo; la cohorte agrupada se etiqueta con el
    año previo a ese (con los datos congelados, 2008 = "<= 2008"). Las fechas inválidas (NaN) no
    pertenecen a ninguna cohorte. Solo cuenta juegos por año: no usa ningún valor del objetivo.
    """
    conteo = anio.value_counts().sort_index()
    grandes = conteo[conteo >= config.COHORTE_MIN_JUEGOS]
    if grandes.empty:                              # ningún año alcanza el mínimo: una sola cohorte
        return anio.where(anio.isna(), anio.max())
    primerGrande = grandes.index.min()
    return anio.where(anio >= primerGrande, primerGrande - 1).where(anio.notna())


@bloqueVariables("y_", permitirPost=True)
def construirObjetivo(df: pd.DataFrame, umbral: int = config.UMBRAL_RESENAS) -> pd.DataFrame:
    """Calcula TODAS las variantes del objetivo (decisión 0001 abierta). Índice app_id.

    - ``y_n_resenas``: positive + negative.
    - ``y_pct_pos``: positive / (positive + negative); NaN si no hay reseñas (nunca 0).
    - ``y_wilson_inf``: límite inferior del intervalo de Wilson al 95 % (``config.Z_WILSON``).
    - ``y_pct_cohorte``: percentil (0-1) de ``y_pct_pos`` dentro de su cohorte de lanzamiento (el año,
      con los años pequeños agrupados; ver ``_agruparCohortes``), calculado solo entre juegos con
      >= ``umbral`` reseñas.
    - ``y_bueno``: 1 si está en el cuartil superior de su cohorte (percentil > ``config.CUANTIL_BUENO``),
      0 si no; NaN si no elegible.
    Es el ÚNICO bloque que puede usar positive/negative. Un juego sin fecha válida no tiene cohorte.
    El año se usa solo para agrupar; nunca se devuelve como variable. Issue: S1-10.
    """
    indice = pd.Index(df["app_id"].to_numpy(), name="app_id")
    positivas = pd.Series(pd.to_numeric(df["positive"], errors="coerce").to_numpy(dtype=float), index=indice)
    negativas = pd.Series(pd.to_numeric(df["negative"], errors="coerce").to_numpy(dtype=float), index=indice)
    anio = pd.Series(pd.to_datetime(df["release_date"], errors="coerce").dt.year.to_numpy(dtype=float),
                     index=indice)

    nResenas = positivas + negativas
    n = nResenas.where(nResenas > 0)              # denominador: NaN si no hay reseñas
    pctPos = positivas / n

    # Límite inferior de Wilson: penaliza las proporciones calculadas con pocas reseñas.
    z2 = config.Z_WILSON ** 2
    centro = pctPos + z2 / (2 * n)
    margen = config.Z_WILSON * np.sqrt(pctPos * (1 - pctPos) / n + z2 / (4 * n ** 2))
    wilsonInf = (centro - margen) / (1 + z2 / n)

    # Percentil dentro de la cohorte, solo entre juegos elegibles (>= umbral reseñas).
    cohorte = _agruparCohortes(anio)
    elegible = (nResenas >= umbral) & pctPos.notna() & cohorte.notna()
    pctCohorte = pctPos.where(elegible).groupby(cohorte).rank(pct=True)
    bueno = (pctCohorte > config.CUANTIL_BUENO).astype(float).where(pctCohorte.notna())

    return pd.DataFrame({
        "y_n_resenas": nResenas,
        "y_pct_pos": pctPos,
        "y_wilson_inf": wilsonInf,
        "y_pct_cohorte": pctCohorte,
        "y_bueno": bueno,
    })


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
