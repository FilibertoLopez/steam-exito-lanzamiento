import tempfile
from pathlib import Path

import pandas as pd

from steam_exito.carga import _aIndicadores, cargarDesdeCsv, cargarSlim


def test_aIndicadores_convierte_texto():
    df = pd.DataFrame({"app_id": [1, 2, 3], "website": ["http://a", None, "  "], "notes": [None, "x", None]})
    r = _aIndicadores(df)
    assert r["has_website"].tolist() == [True, False, False]
    assert r["has_notes"].tolist() == [False, True, False]
    assert "website" not in r.columns and "notes" not in r.columns


def test_aIndicadores_no_toca_lo_ya_convertido():
    df = pd.DataFrame({"app_id": [1], "has_website": [True]})
    assert _aIndicadores(df)["has_website"].tolist() == [True]


def test_cargarDesdeCsv_descarta_pesadas_y_crea_indicadores():
    with tempfile.TemporaryDirectory() as d:
        ruta = Path(d) / "steam_games.csv"
        pd.DataFrame({"app_id": [1, 2], "name": ["a", "b"], "release_date": ["2020-01-01", "2021-02-02"],
                      "about_the_game": ["x" * 50, "y"], "website": ["http://a", None]}).to_csv(ruta, index=False)
        r = cargarDesdeCsv(ruta)
        assert "about_the_game" not in r.columns and "website" not in r.columns
        assert r["has_website"].tolist() == [True, False] and r["release_date"].tolist()[0] == "2020-01-01"


def test_cargarSlim_lee_csv_con_aviso():
    import warnings
    with tempfile.TemporaryDirectory() as d:
        pd.DataFrame({"app_id": [1], "release_date": ["2020-01-01"]}).to_csv(Path(d) / "steam_games.csv", index=False)
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            r = cargarSlim(d)
        assert len(r) == 1 and any("Kaggle" in str(x.message) for x in w)
