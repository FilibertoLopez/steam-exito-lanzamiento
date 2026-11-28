import numpy as np
import pandas as pd
import pytest

from steam_exito import config
from steam_exito.limpieza_basica import convertirTipos, limpiarFechas, limpiarPrecios, marcarSinDato
from steam_exito.variables_precio_fecha import variablesFecha, variablesPrecio
from tests.datos_mini import crearDfMini


@pytest.fixture
def dfLimpio():
    return marcarSinDato(limpiarPrecios(limpiarFechas(convertirTipos(crearDfMini()))))


def test_variablesPrecio_contrato(dfLimpio):
    salida = variablesPrecio(dfLimpio)
    assert salida.index.name == "app_id"
    assert list(salida.index) == list(dfLimpio["app_id"])
    assert set(salida.columns) == {"precio_log", "precio_es_gratis", "precio_sin_dato",
                                   "precio_rango", "precio_pct_cohorte"}


def test_variablesPrecio_no_modifica_entrada(dfLimpio):
    copia = dfLimpio.copy()
    variablesPrecio(dfLimpio)
    pd.testing.assert_frame_equal(dfLimpio, copia)


def test_variablesPrecio_valores(dfLimpio):
    salida = variablesPrecio(dfLimpio)
    pagado, gratis, sinPrecio = salida.loc[1], salida.loc[5], salida.loc[12]
    assert pagado["precio_rango"] == 2 and not pagado["precio_es_gratis"]
    assert pagado["precio_log"] == pytest.approx(np.log1p(9.99))
    assert gratis["precio_rango"] == 0 and gratis["precio_es_gratis"]
    assert sinPrecio["precio_sin_dato"] and not sinPrecio["precio_es_gratis"]
    assert pd.isna(sinPrecio["precio_rango"]) and pd.isna(sinPrecio["precio_log"])
    assert pd.isna(sinPrecio["precio_pct_cohorte"])


def test_precio_rango_limites(dfLimpio):
    df = dfLimpio.head(7).copy()
    df["price"] = [0.0, 0.01, 5.0, 5.01, 20.0, 40.0, 40.01]
    rangos = variablesPrecio(df)["precio_rango"].tolist()
    assert rangos == [0, 1, 1, 2, 3, 4, 5]
    assert len(config.CORTES_PRECIO) == 5


def test_precio_pct_cohorte_dentro_del_anio(dfLimpio):
    df = dfLimpio.copy()
    df.loc[df.app_id == 9, "price"] = 1.0          # 2024: 9 (1.00), 8 se eliminó, 12 sin precio
    df.loc[df.app_id == 4, "price"] = 500.0         # 2020: único juego de su año
    salida = variablesPrecio(df)
    assert salida.loc[4, "precio_pct_cohorte"] == 1.0
    assert salida["precio_pct_cohorte"].dropna().between(0, 1).all()
    # cambiar el precio de un juego de otro año no altera el percentil de 2020
    df.loc[df.app_id == 1, "price"] = 9999.0
    assert variablesPrecio(df).loc[4, "precio_pct_cohorte"] == 1.0


def test_variablesFecha_valores(dfLimpio):
    salida = variablesFecha(dfLimpio)
    assert salida.index.name == "app_id"
    assert salida.loc[1, "fecha_mes"] == 3 and salida.loc[1, "fecha_dia_semana"] == 3   # jueves 2018-03-01
    assert salida.loc[2, "fecha_es_fin_de_semana"]                                       # sábado 2019-06-15
    assert not salida.loc[1, "fecha_es_fin_de_semana"]
    enero = salida.loc[3]                                                                # 2021-01-20
    assert enero["fecha_mes_sin"] == pytest.approx(0.0) and enero["fecha_mes_cos"] == pytest.approx(1.0)


def test_variablesFecha_sin_anio_ni_antiguedad(dfLimpio):
    columnas = list(variablesFecha(dfLimpio).columns) + list(variablesPrecio(dfLimpio).columns)
    assert not [c for c in columnas if any(p in c for p in ("anio", "year", "antig", "edad"))]
