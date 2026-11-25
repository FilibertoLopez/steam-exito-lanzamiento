"""Lectura robusta de columnas con listas guardadas como texto.

El dataset mezcla dos formatos en genres, categories, supported_languages, etc.:
    ["Indie", "Action"]                                   (lista de textos)
    [{"id": "23", "description": "Indie"}, ...]           (lista de objetos)
y, en supported_languages de ~28 mil juegos, una lista con UN solo texto (HTML o separado por comas):
    ["English<strong>*</strong>, French<br><strong>*</strong>languages with full audio support"]
Usa SIEMPRE ``aLista`` (o ``idiomasYAudio`` para idiomas); no dividas por comas a mano.
"""
import ast
import json
import re

import numpy as np
import pandas as pd

_VACIOS = {"", "[]", "{}", "none", "nan", "null", "n/a"}


def esVacio(valor) -> bool:
    """True si el valor es nulo, cadena en blanco, ``[]`` o ``{}``."""
    if valor is None:
        return True
    if isinstance(valor, (list, tuple, dict, set, np.ndarray)):
        return len(valor) == 0
    try:
        if pd.isna(valor):
            return True
    except (TypeError, ValueError):
        pass
    return str(valor).strip().lower() in _VACIOS


def _etiqueta(elemento) -> str:
    if isinstance(elemento, dict):
        for clave in ("description", "name", "label"):
            if clave in elemento:
                return str(elemento[clave]).strip()
        return ""
    return str(elemento).strip()


def _leerElementos(valor) -> list:
    """Elementos crudos de la celda (sin limpiar HTML ni duplicados)."""
    if esVacio(valor):
        return []
    if isinstance(valor, (list, tuple, set, np.ndarray)):
        return list(valor)
    if isinstance(valor, dict):
        return list(valor.keys())
    texto = str(valor)
    for lector in (json.loads, ast.literal_eval):
        try:
            resultado = lector(texto)
        except (ValueError, SyntaxError, TypeError):
            continue
        if isinstance(resultado, dict):
            return list(resultado.keys())
        if isinstance(resultado, (list, tuple)):
            return list(resultado)
        return [resultado]
    return re.sub(r"[\[\]'\"]", "", texto).split(",")


def _dividirHtml(texto: str) -> list:
    """Divide un texto HTML de idiomas en [(nombre, marcado_con_asterisco)], quitando el pie."""
    texto = re.split(r"<br\s*/?>", texto, maxsplit=1)[0]
    pares = []
    for parte in texto.split(","):
        nombre = re.sub(r"<[^>]+>", "", parte).replace("*", "").strip()
        if nombre:
            pares.append((nombre, "*" in parte))
    return pares


def aLista(valor) -> list:
    """Convierte una celda en lista de etiquetas (texto), sin vacíos ni duplicados.

    Soporta listas reales, JSON, repr de Python (comillas simples), listas de objetos y
    listas con un texto HTML (se divide por comas y se quitan las marcas).
    """
    etiquetas = []
    for elemento in _leerElementos(valor):
        texto = _etiqueta(elemento)
        if "<" in texto:
            etiquetas.extend(nombre for nombre, _ in _dividirHtml(texto))
        else:
            etiquetas.append(texto)
    return list(dict.fromkeys(e for e in etiquetas if e))


def idiomasYAudio(soportados, audioCompleto):
    """Unifica idiomas y doblaje de los formatos de supported_languages.

    Devuelve ``(idiomas, audio)``. En el formato HTML el doblaje completo va marcado con ``*`` y
    ``full_audio_languages`` viene nulo; en el otro formato se lee de ``full_audio_languages``.
    Un elemento con comas ("English, French") se divide en idiomas.
    ``audio`` es ``None`` cuando no se sabe (formato texto con ``full_audio_languages`` nulo).
    """
    pares, hayHtml = [], False
    for elemento in _leerElementos(soportados):
        texto = _etiqueta(elemento)
        if "<" in texto:
            hayHtml = True
            pares.extend(_dividirHtml(texto))
        else:
            pares.extend((p.strip(), False) for p in texto.split(",") if p.strip())
    idiomas = list(dict.fromkeys(n for n, _ in pares))
    if hayHtml:
        audio = list(dict.fromkeys(n for n, marcado in pares if marcado))
    elif audioCompleto is None or (not isinstance(audioCompleto, (list, tuple, np.ndarray)) and pd.isna(audioCompleto)):
        audio = None
    else:
        audio = aLista(audioCompleto)
    return idiomas, audio


def aBooleano(serie: pd.Series) -> pd.Series:
    """Convierte 'True'/'False'/1/0 (texto o número) a booleano anulable; vacíos -> <NA>."""
    mapa = {"true": True, "1": True, "1.0": True, "false": False, "0": False, "0.0": False}
    return serie.astype("string").str.strip().str.lower().map(mapa).astype("boolean")
