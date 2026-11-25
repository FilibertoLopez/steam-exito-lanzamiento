"""Idiomas de un juego como columnas booleanas de los 10 idiomas más hablados del mundo.

Acuerdo A-007 y tema pendiente del 2026-11-22: usar los idiomas como estimación del mercado potencial.

Fuente de los idiomas y hablantes: Ethnologue, 29.ª edición (2026), «What are the top 200 most spoken
languages?», https://www.ethnologue.com/guides/ethnologue200 (hablantes totales: primera + segunda lengua).
Ethnologue publica inglés y chino mandarín redondeados (1.5 mil millones y 1.2 mil millones); se usan así.

Uso como módulo::

    from steam_exito.idiomas_top10 import transformarIdiomas
    idiomasDf = transformarIdiomas(gamesDf)          # indexado por app_id

Uso como programa (escribe un CSV con app_id y las columnas nuevas)::

    python -m steam_exito.idiomas_top10 --entrada data/raw/steam_games.csv \
        --salida data/processed/idiomas_top10.csv

Columnas que produce (prefijo ``idi_``, compatibles con la especificación de S1-06):

- ``idi_tiene_<idioma>`` (bool): el juego declara ese idioma en ``supported_languages``.
- ``idi_n_top10`` (int): cuántos de los 10 idiomas tiene.
- ``idi_mercado_millones`` (float): suma de hablantes de esos idiomas, en millones. Es una cota superior
  del mercado: una persona bilingüe se cuenta dos veces.
- ``idi_n_otros`` (int): idiomas que tiene fuera del top 10 (sirve como control del esfuerzo de localización).
- ``idi_sin_dato`` (bool): ``supported_languages`` vacío.
"""
from __future__ import annotations

import argparse
import html
import re
import sys
from pathlib import Path

import pandas as pd

try:  # dentro del paquete
    from steam_exito import parsers
except ImportError:  # ejecución directa del archivo
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from steam_exito import parsers

# Ethnologue 2026 (29.ª ed.): hablantes totales en millones. El ruso (210.3 M) quedó en el lugar 11.
TOP10_IDIOMAS = {
    'ingles':     {'nombre': 'Inglés',          'hablantes': 1500.0},
    'chino':      {'nombre': 'Chino mandarín',  'hablantes': 1200.0},
    'hindi':      {'nombre': 'Hindi',           'hablantes': 611.2},
    'espanol':    {'nombre': 'Español',         'hablantes': 561.3},
    'arabe':      {'nombre': 'Árabe estándar',  'hablantes': 334.9},
    'frances':    {'nombre': 'Francés',         'hablantes': 333.5},
    'bengali':    {'nombre': 'Bengalí',         'hablantes': 274.4},
    'portugues':  {'nombre': 'Portugués',       'hablantes': 269.4},
    'indonesio':  {'nombre': 'Indonesio',       'hablantes': 254.8},
    'urdu':       {'nombre': 'Urdu',            'hablantes': 246.0},
}

# Nombre de Steam (y variantes traducidas que aparecen en los datos) -> clave del idioma.
# Se compara contra el nombre normalizado (minúsculas, sin acentos, sin paréntesis ni variante regional).
# Chino: Steam distingue «Simplified Chinese» y «Traditional Chinese»; los dos cuentan como chino,
# porque Ethnologue mide el idioma hablado (mandarín) y no el sistema de escritura.
_PATRONES = {
    'ingles':    r'^(english|ingles|anglais|englisch|inglese|angielski|英语|英語)$',
    'chino':     r'^((simplified|traditional) chinese|chinese|chino( simplificado| tradicional)?|chinois( simplifie| traditionnel)?'
                 r'|chineza( simplificata| traditionala)?|chinesisch|简体中文|繁體中文|繁体中文|中文|中国語.*)$',
    'hindi':     r'^(hindi|हिन्दी|हिंदी)$',
    'espanol':   r'^(spanish|espanol|espagnol|spanisch|spagnolo|hiszpanski|スペイン語)$',
    'arabe':     r'^(arabic|arabe|arabisch|arabo|العربية)$',
    'frances':   r'^(french|frances|francais|franzosisch|francese|francuski)$',
    'bengali':   r'^(bangla|bengali|bengalí|বাংলা)$',
    'portugues': r'^(portuguese|portugues|portugais|portugiesisch|portoghese|portugalski)$',
    'indonesio': r'^(indonesian|indonesio|indonesien|bahasa indonesia|indonesisch)$',
    'urdu':      r'^(urdu|اردو)$',
}
_PATRONES = {clave: re.compile(patron) for clave, patron in _PATRONES.items()}

_ACENTOS = str.maketrans('áàâäãéèêëíìîïóòôöõúùûüçñăâîșşțţ', 'aaaaaeeeeiiiiooooouuuucnaaisstt')


def normalizarIdioma(nombre: str) -> str:
    """Limpia un nombre de idioma de Steam: HTML escapado, marcas, variante regional y acentos.

    'Spanish - Latin America' -> 'spanish'; 'Portugais du Brésil' -> 'portugais';
    'English&amp;lt;strong&amp;gt;*' -> 'english'; 'Traditional Chinese (text only)' -> 'traditional chinese'.
    """
    texto = str(nombre)
    for _ in range(6):  # hay celdas con el HTML escapado varias veces
        nuevo = html.unescape(texto)
        if nuevo == texto:
            break
        texto = nuevo
    texto = re.sub(r'<[^>]+>', '', texto)
    texto = re.sub(r'b\*/b|\*', '', texto)                      # restos de <b>*</b>
    texto = re.sub(r'languages? with full audio support', '', texto, flags=re.I)
    texto = re.sub(r'\(.*?\)', '', texto)                             # «(full audio)», «(text only)»
    texto = re.split(r'\s+-\s+|\s+du\s+|\s+do\s+|\s+de\s+', texto)[0]  # variante regional
    texto = texto.strip().lower().translate(_ACENTOS)
    return re.sub(r'\s+', ' ', texto)


def idiomasDeCelda(soportados) -> list[str]:
    """Nombres de idioma de una celda de supported_languages (JSON, HTML o con saltos de línea)."""
    idiomas, _ = parsers.idiomasYAudio(soportados, None)
    nombres = []
    for idioma in idiomas:
        nombres.extend(p for p in re.split(r'[\r\n]+', idioma) if p.strip())  # «English\r\nRussian\r\n...»
    return nombres


def clasificarIdiomas(nombres: list[str]) -> tuple[set[str], int]:
    """Devuelve (claves del top 10 presentes, número de otros idiomas distintos)."""
    presentes, otros = set(), set()
    for nombre in nombres:
        normal = normalizarIdioma(nombre)
        if not normal or normal.startswith('#lang'):
            continue
        clave = next((c for c, patron in _PATRONES.items() if patron.match(normal)), None)
        if clave:
            presentes.add(clave)
        else:
            otros.add(normal)
    return presentes, len(otros)


def transformarIdiomas(df: pd.DataFrame, columna: str = 'supported_languages') -> pd.DataFrame:
    """Convierte ``supported_languages`` en columnas booleanas del top 10 y medidas de mercado.

    Recibe un DataFrame con ``app_id`` y ``columna``; devuelve un DataFrame indexado por ``app_id``
    con una fila por juego de la entrada.
    """
    if 'app_id' not in df.columns or columna not in df.columns:
        raise KeyError(f'Se necesitan las columnas app_id y {columna}')
    filas = []
    for valor in df[columna]:
        sinDato = parsers.esVacio(valor)
        presentes, nOtros = clasificarIdiomas(idiomasDeCelda(valor)) if not sinDato else (set(), 0)
        fila = {f'idi_tiene_{clave}': clave in presentes for clave in TOP10_IDIOMAS}
        fila['idi_n_top10'] = len(presentes)
        fila['idi_mercado_millones'] = sum(TOP10_IDIOMAS[c]['hablantes'] for c in presentes)
        fila['idi_n_otros'] = nOtros
        fila['idi_sin_dato'] = sinDato
        filas.append(fila)
    salida = pd.DataFrame(filas, index=pd.Index(df['app_id'].to_numpy(), name='app_id'))
    boolCols = [c for c in salida.columns if c.startswith('idi_tiene_')] + ['idi_sin_dato']
    salida[boolCols] = salida[boolCols].astype(bool)
    return salida


def tablaIdiomas() -> pd.DataFrame:
    """Tabla de referencia de los 10 idiomas (clave, nombre, hablantes en millones, columna)."""
    return pd.DataFrame([{'clave': c, 'idioma': v['nombre'], 'hablantesMillones': v['hablantes'],
                          'columna': f'idi_tiene_{c}'} for c, v in TOP10_IDIOMAS.items()])


def _main(argv=None) -> None:
    lector = argparse.ArgumentParser(description='Columnas booleanas de los 10 idiomas más hablados (Ethnologue 2026).')
    lector.add_argument('--entrada', required=True, help='steam_games.csv o .csv.gz')
    lector.add_argument('--salida', required=True, help='CSV de salida (app_id + columnas idi_)')
    args = lector.parse_args(argv)
    gamesDf = pd.read_csv(args.entrada, usecols=['app_id', 'supported_languages'],
                          keep_default_na=False, na_values=[''], low_memory=False)
    idiomasDf = transformarIdiomas(gamesDf)
    Path(args.salida).parent.mkdir(parents=True, exist_ok=True)
    idiomasDf.to_csv(args.salida)
    print(f'{len(idiomasDf):,} juegos -> {args.salida}')
    print(idiomasDf.filter(like='idi_tiene_').mean().mul(100).round(1).rename('% de juegos').to_string())


if __name__ == '__main__':
    _main()
