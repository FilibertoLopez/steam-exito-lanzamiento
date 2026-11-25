"""Contrato de integración: decoradores que validan lo que entrega cada función.

Hay dos tipos de función en el pipeline:

1. **Paso de limpieza** (``@pasoLimpieza``): recibe un DataFrame con columna ``app_id`` y devuelve
   otro DataFrame (mismas filas o menos). Puede cambiar tipos y valores, no inventar filas.
2. **Bloque de variables** (``@bloqueVariables``): recibe el DataFrame limpio y devuelve un
   DataFrame **indexado por app_id**, con una fila por juego y columnas que empiezan con el
   prefijo del bloque (``dev_``, ``gen_``, ...), numéricas o booleanas, sin infinitos.

Si una función incumple el contrato, falla con un mensaje claro en el propio PR, no en la integración.
"""
import functools

import numpy as np
import pandas as pd

from steam_exito import config

BITACORA: list = []


def resumenBitacora() -> pd.DataFrame:
    """Tabla con filas antes/después de cada paso ejecutado (sirve para el reporte)."""
    return pd.DataFrame(BITACORA)


def pasoLimpieza(nombre: str):
    """Decorador para funciones ``df -> df`` de limpieza o filtrado."""
    def decorador(funcion):
        @functools.wraps(funcion)
        def envoltura(df, *args, **kwargs):
            antes = len(df)
            salida = funcion(df, *args, **kwargs)
            if not isinstance(salida, pd.DataFrame):
                raise TypeError(f"{funcion.__name__}: debe devolver un DataFrame")
            if "app_id" not in salida.columns:
                raise ValueError(f"{funcion.__name__}: la salida debe conservar la columna app_id")
            if not salida["app_id"].is_unique:
                raise ValueError(f"{funcion.__name__}: app_id duplicado en la salida")
            if len(salida) > antes:
                raise ValueError(f"{funcion.__name__}: un paso de limpieza no puede agregar filas")
            BITACORA.append({"paso": nombre, "funcion": funcion.__name__,
                             "filas_antes": antes, "filas_despues": len(salida)})
            return salida
        envoltura.nombrePaso = nombre
        return envoltura
    return decorador


def validarBloque(entrada: pd.DataFrame, salida, prefijo: str, nombre: str,
                  permitirPost: bool = False) -> pd.DataFrame:
    """Valida un bloque de variables y lo devuelve alineado con ``entrada['app_id']``."""
    if not isinstance(salida, pd.DataFrame):
        raise TypeError(f"{nombre}: debe devolver un DataFrame")
    if salida.index.name != "app_id":
        raise ValueError(f"{nombre}: el índice debe llamarse 'app_id' (usa set_index('app_id'))")
    if not salida.index.is_unique:
        raise ValueError(f"{nombre}: app_id duplicado en el índice")
    if set(salida.index) != set(entrada["app_id"]):
        raise ValueError(f"{nombre}: debe devolver exactamente un renglón por juego de la entrada")
    if salida.columns.duplicated().any():
        raise ValueError(f"{nombre}: columnas duplicadas")
    malas = [c for c in salida.columns if not str(c).startswith(prefijo)]
    if malas:
        raise ValueError(f"{nombre}: todas las columnas deben empezar con '{prefijo}'. Incumplen: {malas}")
    if not permitirPost:
        fuga = [c for c in salida.columns if str(c)[len(prefijo):] in config.COLUMNAS_POST]
        if fuga:
            raise ValueError(f"{nombre}: columnas con nombre de variable POST-lanzamiento: {fuga}")
    for c in salida.columns:
        tipo = salida[c].dtype
        if not (pd.api.types.is_numeric_dtype(tipo) or pd.api.types.is_bool_dtype(tipo)):
            raise TypeError(f"{nombre}: la columna {c} debe ser numérica o booleana (es {tipo}). "
                            "Codifica las categorías antes de entregarlas.")
    numericas = salida.select_dtypes("number")
    if np.isinf(numericas.to_numpy(dtype=float, na_value=np.nan)).any():
        raise ValueError(f"{nombre}: hay valores infinitos")
    return salida.reindex(entrada["app_id"].to_numpy())


def bloqueVariables(prefijo: str, permitirPost: bool = False):
    """Decorador para funciones ``df -> DataFrame indexado por app_id`` con columnas ``prefijo*``."""
    def decorador(funcion):
        @functools.wraps(funcion)
        def envoltura(df, *args, **kwargs):
            salida = funcion(df, *args, **kwargs)
            salida = validarBloque(df, salida, prefijo, funcion.__name__, permitirPost)
            BITACORA.append({"paso": f"bloque {prefijo}", "funcion": funcion.__name__,
                             "filas_antes": len(df), "filas_despues": len(salida),
                             "columnas": salida.shape[1]})
            return salida
        envoltura.prefijo = prefijo
        return envoltura
    return decorador
