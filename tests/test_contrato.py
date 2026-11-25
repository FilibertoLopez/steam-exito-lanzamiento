import pandas as pd

from steam_exito.contrato import bloqueVariables, pasoLimpieza
from tests.datos_mini import crearDfMini


def _falla(funcion, *args):
    try:
        funcion(*args)
    except (ValueError, TypeError):
        return True
    return False


def test_bloque_valido():
    @bloqueVariables("t_")
    def ok(df):
        return pd.DataFrame({"t_x": range(len(df))}, index=pd.Index(df["app_id"].values[::-1], name="app_id"))
    df = crearDfMini()
    salida = ok(df)
    assert list(salida.index) == list(df["app_id"])  # reordenado a la entrada


def test_bloque_prefijo_incorrecto():
    @bloqueVariables("t_")
    def mal(df):
        return pd.DataFrame({"x": 1}, index=pd.Index(df["app_id"], name="app_id"))
    assert _falla(mal, crearDfMini())


def test_bloque_sin_indice_app_id():
    @bloqueVariables("t_")
    def mal(df):
        return pd.DataFrame({"t_x": 1}, index=df["app_id"].values)
    assert _falla(mal, crearDfMini())


def test_bloque_con_variable_post():
    @bloqueVariables("t_")
    def mal(df):
        return pd.DataFrame({"t_positive": 1}, index=pd.Index(df["app_id"], name="app_id"))
    assert _falla(mal, crearDfMini())


def test_bloque_texto_no_permitido():
    @bloqueVariables("t_")
    def mal(df):
        return pd.DataFrame({"t_x": "a"}, index=pd.Index(df["app_id"], name="app_id"))
    assert _falla(mal, crearDfMini())


def test_bloque_faltan_filas():
    @bloqueVariables("t_")
    def mal(df):
        return pd.DataFrame({"t_x": 1}, index=pd.Index(df["app_id"][:3], name="app_id"))
    assert _falla(mal, crearDfMini())


def test_bloque_objetivo_permite_post():
    @bloqueVariables("y_", permitirPost=True)
    def ok(df):
        return pd.DataFrame({"y_positive": df["positive"].values}, index=pd.Index(df["app_id"], name="app_id"))
    assert len(ok(crearDfMini())) == 12


def test_paso_no_puede_agregar_filas():
    @pasoLimpieza("x")
    def mal(df):
        return pd.concat([df, df]).assign(app_id=lambda d: range(len(d)))
    assert _falla(mal, crearDfMini())


def test_paso_exige_app_id_unico():
    @pasoLimpieza("x")
    def mal(df):
        return df.assign(app_id=1)
    assert _falla(mal, crearDfMini())
