import pandas as pd

from steam_exito import config
from steam_exito.carga import huellaAppId, verificarVersion


def test_huella_no_depende_del_orden():
    a = pd.DataFrame({"app_id": [3, 1, 2]})
    assert huellaAppId(a) == huellaAppId(a.iloc[::-1])


def test_version_incorrecta_falla():
    try:
        verificarVersion(pd.DataFrame({"app_id": [1, 2, 3]}))
    except ValueError:
        return
    raise AssertionError("debió fallar con datos de otra versión")


def test_config_coherente():
    assert config.UMBRAL_RESENAS in config.UMBRALES_SENSIBILIDAD
    assert set(config.GENEROS_JUEGO).isdisjoint(config.ETIQUETAS_MARKETING)
    assert "positive" in config.COLUMNAS_POST
