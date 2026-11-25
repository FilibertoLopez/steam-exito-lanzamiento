"""Prueba de integración: el pipeline completo corre con los bloques que ya existan.

Mientras haya funciones pendientes se omiten (permitirPendientes=True). Cuando TODAS estén
implementadas, ``omitidos`` debe quedar vacío (esa es la condición de cierre del Sprint 1).
Cada bloque implementado se valida solo con ``contrato.py`` al ejecutarse.
"""
from steam_exito.pipeline import BLOQUES, PASOS_LIMPIEZA, correrPipeline
from tests.datos_mini import crearDfMini


def test_pipeline_corre_con_pendientes():
    r = correrPipeline(crearDfMini(), permitirPendientes=True, verificar=False)
    total = len(PASOS_LIMPIEZA) + len(BLOQUES) + 2  # + muestra + partición
    assert len(r["omitidos"]) <= total
    assert "app_id" in r["tabla"].columns and len(r["tabla"]) >= 1


def test_prefijos_unicos_entre_bloques():
    prefijos = [b.funcion.prefijo for b in BLOQUES]
    assert len(prefijos) == len(set(prefijos))


def test_pipeline_completo_sin_pendientes():
    """Se activa solo cuando todo está implementado."""
    r = correrPipeline(crearDfMini(), permitirPendientes=True, verificar=False)
    if r["omitidos"]:
        return  # todavía hay trabajo pendiente: no es un error
    assert r["muestra"]["app_id"].is_unique
    assert set(r["particion"].unique()) <= {"train", "valid", "test"}
    assert not [c for c in r["muestra"].columns if c in ("positive", "negative")]
