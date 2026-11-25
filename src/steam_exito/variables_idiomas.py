"""Idiomas. Responsable: Luis. Issue: S1-06 (incluye el acuerdo A-007)."""
import pandas as pd

from steam_exito.contrato import bloqueVariables


@bloqueVariables("idi_")
def variablesIdiomas(df: pd.DataFrame) -> pd.DataFrame:
    """Columnas esperadas. Usa ``parsers.idiomasYAudio`` (resuelve los formatos HTML y de texto):

    - ``idi_n_idiomas``: idiomas base distintos (lo anterior a ' - ': 'Portuguese - Brazil' = 'Portuguese').
    - ``idi_n_audio``: idiomas con doblaje completo; NaN si no se sabe (``audio is None``).
    - ``idi_tiene_ingles``, ``idi_tiene_espanol``, ``idi_tiene_chino``, ``idi_tiene_ruso``.
    - ``idi_sin_dato``: ``supported_languages`` vacío (relleno 0 idiomas + este indicador).
    Se entrega con el análisis de dispersión idiomas vs. proporción positiva (A-007); el EDA ya indica
    una asociación débil una vez descontada la cohorte.
    """
    raise NotImplementedError("Pendiente: Luis (S1-06)")
