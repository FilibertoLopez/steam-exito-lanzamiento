"""Pipeline de limpieza e ingeniería de variables (todo lo previo al modelo baseline).

    cargarSlim -> verificarVersion -> [pasos de limpieza] -> [bloques de variables + objetivo]
    -> tabla unificada -> filtrarMuestra -> particionTemporal -> data/processed/

Uso:
    from steam_exito.pipeline import correrPipeline
    r = correrPipeline()                          # falla si algún paso aún no está implementado
    r = correrPipeline(permitirPendientes=True)   # omite los pendientes (útil durante el sprint)
    r["muestra"], r["particion"], r["omitidos"]
"""
from collections import namedtuple

import pandas as pd

from steam_exito import carga, config, contrato, evaluacion, limpieza_basica, muestra
from steam_exito import variables_desarrollador as vd
from steam_exito import variables_ficha as vf
from steam_exito import variables_generos as vg
from steam_exito import variables_idiomas as vi
from steam_exito import variables_precio_fecha as vp

Paso = namedtuple("Paso", "nombre funcion responsable")

PASOS_LIMPIEZA = [
    Paso("tipos", limpieza_basica.convertirTipos, "Filiberto"),
    Paso("fechas", limpieza_basica.limpiarFechas, "Filiberto"),
    Paso("precios", limpieza_basica.limpiarPrecios, "Filiberto"),
    Paso("sin_dato", limpieza_basica.marcarSinDato, "Filiberto"),
    Paso("no_juegos", vg.quitarNoJuegos, "Luis"),
]

BLOQUES = [
    Paso("precio", vp.variablesPrecio, "Filiberto"),
    Paso("fecha", vp.variablesFecha, "Filiberto"),
    Paso("ficha", vf.variablesFicha, "Filiberto"),
    Paso("generos", vg.variablesGeneros, "Luis"),
    Paso("categorias", vg.variablesCategorias, "Luis"),
    Paso("idiomas", vi.variablesIdiomas, "Luis"),
    Paso("desarrollador", vd.variablesDesarrollador, "Diana"),
    Paso("publisher", vd.variablesPublisher, "Diana"),
    Paso("objetivo", muestra.construirObjetivo, "Alejandra"),
]


def _ejecutar(paso, args, permitirPendientes, omitidos):
    try:
        return paso.funcion(*args)
    except NotImplementedError:
        if not permitirPendientes:
            raise
        omitidos.append(f"{paso.nombre} ({paso.responsable})")
        return None


def ensamblar(base: pd.DataFrame, bloques: list) -> pd.DataFrame:
    """Une la tabla base (app_id, name, release_date) con los bloques por app_id."""
    tabla = base.set_index("app_id")
    for bloque in bloques:
        repetidas = set(tabla.columns) & set(bloque.columns)
        if repetidas:
            raise ValueError(f"Columnas repetidas entre bloques: {sorted(repetidas)}")
        tabla = tabla.join(bloque, how="left")
    return tabla.reset_index()


def correrPipeline(df: pd.DataFrame | None = None, permitirPendientes: bool = False,
                   guardar: bool = False, verificar: bool = True) -> dict:
    """Ejecuta todo el pipeline y devuelve ``tabla``, ``muestra``, ``particion`` y ``omitidos``."""
    contrato.BITACORA.clear()
    df = carga.cargarSlim() if df is None else df
    if verificar:
        carga.verificarVersion(df)
    omitidos: list = []

    for paso in PASOS_LIMPIEZA:
        salida = _ejecutar(paso, (df,), permitirPendientes, omitidos)
        df = df if salida is None else salida

    bloques = []
    for paso in BLOQUES:
        salida = _ejecutar(paso, (df,), permitirPendientes, omitidos)
        if salida is not None:
            bloques.append(salida)

    columnasBase = [c for c in config.COLUMNAS_BASE if c in df.columns]
    tabla = ensamblar(df[columnasBase], bloques)

    paso = Paso("muestra", muestra.filtrarMuestra, "Alejandra")
    salida = _ejecutar(paso, (tabla,), permitirPendientes, omitidos)
    seleccion = tabla if salida is None else salida

    paso = Paso("particion", evaluacion.particionTemporal, "Alejandra")
    particion = _ejecutar(paso, (seleccion,), permitirPendientes, omitidos)

    if guardar:
        carga.guardarProcesado(seleccion, "steam_modelo")
        if particion is not None:
            carga.guardarProcesado(particion.to_frame("conjunto"), "particion")
    return {"tabla": tabla, "muestra": seleccion, "particion": particion, "omitidos": omitidos,
            "bitacora": contrato.resumenBitacora()}


if __name__ == "__main__":  # python -m steam_exito.pipeline
    r = correrPipeline(permitirPendientes=True, guardar=True)
    print("Pendientes:", r["omitidos"] or "ninguno")
    print(r["bitacora"].to_string(index=False))
