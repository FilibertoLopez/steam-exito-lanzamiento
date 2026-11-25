import pandas as pd

from steam_exito.parsers import aBooleano, aLista, esVacio, idiomasYAudio


def test_aLista_dos_formatos():
    assert aLista('["Indie", "Action"]') == ["Indie", "Action"]
    assert aLista('[{"id": "23", "description": "Indie"}]') == ["Indie"]
    assert aLista("[{'id': 1, 'description': 'Single-player'}]") == ["Single-player"]


def test_aLista_vacios_y_duplicados():
    assert aLista(None) == []
    assert aLista("[]") == []
    assert aLista(float("nan")) == []
    assert aLista('["A", "A", " "]') == ["A"]


def test_aLista_html():
    assert aLista("English<strong>*</strong>, French") == ["English", "French"]


def test_aLista_html_con_pie_de_audio():
    celda = '["English<strong>*</strong>, French<br><strong>*</strong>languages with full audio support"]'
    assert aLista(celda) == ["English", "French"]


def test_idiomasYAudio_formato_html():
    celda = '["English<strong>*</strong>, Spanish - Spain, French<strong>*</strong><br><strong>*</strong>languages with full audio support"]'
    idiomas, audio = idiomasYAudio(celda, None)
    assert idiomas == ["English", "Spanish - Spain", "French"] and audio == ["English", "French"]


def test_idiomasYAudio_formato_texto():
    assert idiomasYAudio('["English", "French"]', '["English"]') == (["English", "French"], ["English"])
    assert idiomasYAudio('["English"]', "[]") == (["English"], [])
    assert idiomasYAudio('["English"]', None) == (["English"], None)


def test_idiomasYAudio_un_elemento_con_comas():
    assert idiomasYAudio('["English, French, German"]', None)[0] == ["English", "French", "German"]


def test_esVacio():
    assert esVacio("  ") and esVacio("[]") and esVacio(None)
    assert not esVacio('["x"]') and not esVacio(0)


def test_aBooleano():
    r = aBooleano(pd.Series(["True", "False", None]))
    assert r.tolist()[:2] == [True, False] and r.isna().tolist() == [False, False, True]
