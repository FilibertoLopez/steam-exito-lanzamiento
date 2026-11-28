"""Pruebas de construirObjetivo (S1-10). Los valores esperados se calcularon a mano sobre
tests/datos_mini.py; la tabla de referencia está en el docstring de cada prueba."""
import numpy as np
import pandas as pd
import pytest

from steam_exito import config
from steam_exito.muestra import construirObjetivo
from tests.datos_mini import crearDfMini


@pytest.fixture(autouse=True)
def sin_agrupar(monkeypatch):
    """Los datos mini tienen 1 a 3 juegos por año: sin esto todos caerían en una sola cohorte.
    Se desactiva el agrupamiento (mínimo = 1) salvo en la prueba que lo ejercita."""
    monkeypatch.setattr(config, "COHORTE_MIN_JUEGOS", 1)


def _objetivo(umbral=50):
    return construirObjetivo(crearDfMini(), umbral=umbral)


def test_forma_y_prefijo():
    y = _objetivo()
    assert y.index.name == "app_id" and len(y) == 12
    assert list(y.columns) == ["y_n_resenas", "y_pct_pos", "y_wilson_inf", "y_pct_cohorte", "y_bueno"]


def test_proporcion_positiva():
    y = _objetivo()
    assert y.loc[2, "y_n_resenas"] == 100                       # 90 + 10
    assert y.loc[2, "y_pct_pos"] == pytest.approx(0.90)         # 90 / 100
    assert y.loc[5, "y_pct_pos"] == pytest.approx(500 / 600)


def test_sin_resenas_es_nan_no_cero():
    y = _objetivo()
    assert y.loc[6, "y_n_resenas"] == 0
    assert np.isnan(y.loc[6, "y_pct_pos"]) and np.isnan(y.loc[6, "y_wilson_inf"])
    assert np.isnan(y.loc[6, "y_pct_cohorte"]) and np.isnan(y.loc[6, "y_bueno"])


def test_wilson_penaliza_pocas_resenas():
    df = crearDfMini().iloc[:2].copy()
    df["positive"] = [3, 300]
    df["negative"] = [0, 0]
    y = construirObjetivo(df)
    assert y["y_pct_pos"].eq(1.0).all()
    assert y.iloc[0]["y_wilson_inf"] < y.iloc[1]["y_wilson_inf"] < 1.0
    assert y.iloc[0]["y_wilson_inf"] == pytest.approx(0.4385, abs=1e-3)   # 3 de 3, z = 1.96


def test_wilson_nunca_supera_la_proporcion():
    y = _objetivo().dropna(subset=["y_pct_pos"])
    assert (y["y_wilson_inf"] <= y["y_pct_pos"] + 1e-12).all()


def test_percentil_dentro_del_anio_solo_entre_elegibles():
    y = _objetivo(umbral=50)
    # 2024: juegos 9 (0.60), 8 (0.80) y 12 (0.90, exactamente 50 reseñas)
    assert y.loc[9, "y_pct_cohorte"] == pytest.approx(1 / 3)
    assert y.loc[8, "y_pct_cohorte"] == pytest.approx(2 / 3)
    assert y.loc[12, "y_pct_cohorte"] == pytest.approx(1.0)
    assert y.loc[12, "y_bueno"] == 1 and y.loc[8, "y_bueno"] == 0 and y.loc[9, "y_bueno"] == 0


def test_bajo_el_umbral_no_es_elegible():
    y = _objetivo(umbral=50)
    assert y.loc[11, "y_n_resenas"] == 6
    assert np.isnan(y.loc[11, "y_pct_cohorte"]) and np.isnan(y.loc[11, "y_bueno"])
    assert not np.isnan(y.loc[11, "y_pct_pos"])      # el objetivo en sí sí existe


def test_cambiar_el_umbral_cambia_los_elegibles():
    y = _objetivo(umbral=100)
    assert np.isnan(y.loc[12, "y_pct_cohorte"])      # 50 reseñas ya no alcanza
    assert y.loc[8, "y_pct_cohorte"] == pytest.approx(1.0)   # 2024 solo con 8 (0.80) y 9 (0.60)


def test_fecha_invalida_no_tiene_cohorte():
    y = _objetivo()
    assert np.isnan(y.loc[7, "y_pct_cohorte"]) and not np.isnan(y.loc[7, "y_pct_pos"])


def test_sin_fuga_entre_anios():
    """Cambiar un juego de otro año no altera el percentil de una cohorte (regla anti-fuga 5)."""
    base = _objetivo()
    df = crearDfMini()
    df.loc[df["app_id"] == 11, ["positive", "negative"]] = [5000, 5]     # juego de 2025
    cambiado = construirObjetivo(df)
    assert cambiado.loc[[8, 9, 12], "y_pct_cohorte"].equals(base.loc[[8, 9, 12], "y_pct_cohorte"])


def test_no_modifica_la_entrada():
    df = crearDfMini()
    copia = df.copy()
    construirObjetivo(df)
    pd.testing.assert_frame_equal(df, copia)


def test_acepta_fechas_ya_convertidas():
    df = crearDfMini()
    df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")
    pd.testing.assert_frame_equal(construirObjetivo(df), _objetivo())


def test_cohortes_pequenas_se_agrupan(monkeypatch):
    """Con mínimo = 3, solo 2024 (3 juegos) es cohorte propia; 2018-2023 forman una sola.
    Elegibles de esa cohorte: 1 (0.80), 2 (0.90), 3 (0.30), 4 (0.80), 5 (0.833), 10 (0.80)."""
    monkeypatch.setattr(config, "COHORTE_MIN_JUEGOS", 3)
    y = _objetivo(umbral=50)
    assert y.loc[3, "y_pct_cohorte"] == pytest.approx(1 / 6)                    # el peor
    assert y.loc[[1, 4, 10], "y_pct_cohorte"].eq(0.5).all()                     # empate: rango medio
    assert y.loc[5, "y_pct_cohorte"] == pytest.approx(5 / 6)
    assert y.loc[2, "y_pct_cohorte"] == pytest.approx(1.0)                      # el mejor
    assert y.loc[[2, 5], "y_bueno"].eq(1).all() and y.loc[[1, 3, 4, 10], "y_bueno"].eq(0).all()
    assert y.loc[8, "y_pct_cohorte"] == pytest.approx(2 / 3)                    # 2024 no cambia
