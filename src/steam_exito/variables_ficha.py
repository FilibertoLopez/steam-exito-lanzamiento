"""Variables de la ficha de la tienda: plataformas, logros, sitio y soporte. Responsable: Filiberto.

Issue: S1-03. Son Pre/Pre*: se leen de la tienda actual (D-010).
"""
import pandas as pd

from steam_exito.contrato import bloqueVariables


@bloqueVariables("ficha_")
def variablesFicha(df: pd.DataFrame) -> pd.DataFrame:
    """Columnas esperadas (índice app_id):

    - ``ficha_mac``, ``ficha_linux`` (booleanos; NaN -> False) y ``ficha_n_plataformas`` (1 a 3,
      contando Windows). ``windows`` casi no varía y no se devuelve por separado.
    - ``ficha_logros_log``: log1p(achievements) y ``ficha_tiene_logros``.
    - ``ficha_tiene_sitio``, ``ficha_tiene_soporte_url``, ``ficha_tiene_correo_soporte``,
      ``ficha_aviso_adulto`` (a partir de los indicadores ``has_*`` del parquet).
    NO incluir ``dlc_count`` (D-010: sigue al éxito) ni ``metacritic_score`` (POST).
    """
    raise NotImplementedError("Pendiente: Filiberto (S1-03)")
