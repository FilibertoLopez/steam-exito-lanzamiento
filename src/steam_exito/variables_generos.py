"""Géneros y categorías (D-005) y filtro de no-juegos. Responsable: Luis. Issues: S1-04, S1-05.

Usa SIEMPRE ``parsers.aLista`` para leer las columnas (maneja los dos formatos).
"""
import pandas as pd

from steam_exito.contrato import bloqueVariables, pasoLimpieza


@pasoLimpieza("no_juegos")
def quitarNoJuegos(df: pd.DataFrame) -> pd.DataFrame:
    """Elimina títulos que no son videojuegos (son ~1,555).

    Regla (validada en el EDA): normaliza géneros con ``config.MAPA_GENEROS_TRADUCIDOS``, IGNORA las
    etiquetas de marketing y de aviso, y elimina el juego si los géneros restantes existen y TODOS
    están en ``config.GENEROS_NO_JUEGO``. Juegos sin género (lista vacía) NO se eliminan. Issue: S1-04.
    """
    raise NotImplementedError("Pendiente: Luis (S1-04)")


@bloqueVariables("gen_")
def variablesGeneros(df: pd.DataFrame) -> pd.DataFrame:
    """Multi-hot de géneros, separando marketing de género (D-005).

    - ``gen_<Genero>`` para cada uno de ``config.GENEROS_JUEGO`` (0/1).
    - ``gen_mkt_Indie``, ``gen_mkt_EarlyAccess``, ``gen_mkt_FreeToPlay`` (``config.ETIQUETAS_MARKETING``).
    - ``gen_aviso_maduro``: algún valor de ``config.AVISO_CONTENIDO``.
    - ``gen_n_generos``: número de géneros de juego (sin marketing ni aviso).
    - ``gen_sin_dato``: lista de géneros vacía.
    Issue: S1-04.
    """
    raise NotImplementedError("Pendiente: Luis (S1-04)")


@bloqueVariables("cat_")
def variablesCategorias(df: pd.DataFrame, frecuenciaMinima: float = 0.01) -> pd.DataFrame:
    """Multi-hot de categorías de Steam que aparecen en >= ``frecuenciaMinima`` de los juegos.

    - ``cat_<nombre>`` por categoría frecuente (excluye ``config.CATEGORIAS_EXCLUIR``).
    - ``cat_n_otras``: número de categorías raras que se agruparon; ``cat_n_total``.
    - NO usar el formato original (texto o diccionario) como variable: es un artefacto del año.
    Issue: S1-05.
    """
    raise NotImplementedError("Pendiente: Luis (S1-05)")
