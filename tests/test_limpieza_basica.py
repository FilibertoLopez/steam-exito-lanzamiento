import pandas as pd
import pytest

from steam_exito import config, contrato
from steam_exito.limpieza_basica import convertirTipos, limpiarFechas, limpiarPrecios, marcarSinDato
from tests.datos_mini import crearDfMini


@pytest.fixture
def dfTipos():
    return convertirTipos(crearDfMini())


def test_convertirTipos_no_quita_filas_ni_modifica_entrada():
    df = crearDfMini()
    copia = df.copy()
    salida = convertirTipos(df)
    assert len(salida) == len(df)
    pd.testing.assert_frame_equal(df, copia)


def test_convertirTipos_tipos(dfTipos):
    for c in ["mac", "linux", "windows"]:
        assert str(dfTipos[c].dtype) == "boolean"
    assert dfTipos.loc[dfTipos.app_id == 11, "mac"].isna().all()   # mac vacío -> <NA>
    assert str(dfTipos["achievements"].dtype) == "Int64"
    for c in ["price", "positive", "negative"]:
        assert pd.api.types.is_numeric_dtype(dfTipos[c])


def test_limpiarFechas_quita_invalidas(dfTipos):
    salida = limpiarFechas(dfTipos)
    assert pd.api.types.is_datetime64_any_dtype(salida["release_date"])
    assert 7 not in salida["app_id"].values          # "fecha-mala"
    assert 11 in salida["app_id"].values             # 2025: no se filtra por año
    assert len(salida) == 11


def test_limpiarFechas_quita_posteriores_a_fecha_max(dfTipos):
    df = dfTipos.copy()
    df.loc[df.app_id == 1, "release_date"] = "2099-01-01"
    salida = limpiarFechas(df)
    assert 1 not in salida["app_id"].values


def test_limpiarPrecios(dfTipos):
    salida = limpiarPrecios(dfTipos)
    assert 8 not in salida["app_id"].values          # 107,500 USD
    assert 12 in salida["app_id"].values             # precio nulo se conserva
    assert 5 in salida["app_id"].values              # gratis se conserva
    assert (salida["price"].dropna() <= config.PRECIO_MAX_VALIDO).all()


def test_limpiarPrecios_negativo_falla(dfTipos):
    df = dfTipos.copy()
    df.loc[0, "price"] = -1.0
    with pytest.raises(ValueError):
        limpiarPrecios(df)


def test_marcarSinDato(dfTipos):
    df = dfTipos.copy()
    df.loc[df.app_id == 2, "estimated_owners"] = "0 .. 0"
    df.loc[df.app_id == 3, "estimated_owners"] = "0 - 0"
    salida = marcarSinDato(df)
    assert len(salida) == len(df)
    for c in config.COLUMNAS_CERO_ES_NULO:
        assert not (salida[c] == 0).any()
    assert salida.loc[salida.app_id.isin([2, 3]), "estimated_owners"].isna().all()
    fila9 = salida.loc[salida.app_id == 9]
    assert fila9[["developers", "publishers", "genres"]].isna().all(axis=None)
    # Lo que NO se toca
    assert (salida["full_audio_languages"] == df["full_audio_languages"]).all()
    assert (salida.loc[salida.app_id == 6, ["positive", "negative"]] == 0).all(axis=None)
    assert (salida.loc[salida.app_id == 5, "price"] == 0).all()


def test_bitacora_registra_pasos():
    contrato.BITACORA.clear()
    df = marcarSinDato(limpiarPrecios(limpiarFechas(convertirTipos(crearDfMini()))))
    bitacora = contrato.resumenBitacora()
    assert list(bitacora["paso"]) == ["tipos", "fechas", "precios", "sin_dato"]
    quitadas = dict(zip(bitacora["paso"], bitacora["filas_antes"] - bitacora["filas_despues"]))
    assert quitadas == {"tipos": 0, "fechas": 1, "precios": 1, "sin_dato": 0}
    assert len(df) == 10
