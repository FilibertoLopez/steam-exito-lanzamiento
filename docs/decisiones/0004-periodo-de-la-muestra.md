---
id: 0004
estado: propuesta (valor de trabajo en config.py; la decisión final depende de S1-12)
fecha: 2026-11-25
sesiones: [2026-11-22, 2026-11-25]
acuerdos: [D-002, D-021, D-022, A-003, A-010]
---

# 0004 Periodo de la muestra

## Contexto

En la [sesión del 2026-11-22](../equipo/sesiones/2026-11-22-exploracion-de-datos.md) se propuso excluir los juegos lanzados en 2025 y 2026 porque aún no acumulan historial de reseñas (D-002), y se discutió desde qué año empezar (2010, 2015, 2019 o sin límite inferior). En la [sesión del 2026-11-25](../equipo/sesiones/2026-11-25-EDA-y-sprint-1.md) Filiberto señaló que D-002 «todavía no» se decide; ambas preguntas quedaron abiertas en el [registro de sesiones](../equipo/sesiones/README.md#preguntas-abiertas-pendientes).

Evidencia del [EDA §3](../03-analisis-exploratorio.md):

- La oferta crece de 2,461 lanzamientos en 2015 a 19,748 en 2024, pero la proporción que llega a 50 reseñas cae de 77 % a 16 %.
- Excluir 2025–2026 elimina casi todos los juegos con menos de 12 meses en la tienda; el 79 % de la muestra tiene 4 años o más.

## Opciones consideradas

**Año final**

1. **Hasta 2024** (D-002): excluye los juegos con menos de un año de reseñas.
2. Incluir 2025: más juegos recientes, pero con historial incompleto.

**Año inicial**

1. **Sin límite inferior** (todo el historial): muestra más grande; los años viejos son pocos y caen casi todos en train.
2. Desde 2019: épocas más parecidas a hoy (formatos de la tienda, volumen de lanzamientos), muestra más chica.
3. Desde 2010 o 2015.

## Propuesta de trabajo

El plan del [Sprint 1](../equipo/sprint-1-tareas.md#decisiones-previas-cerrar-el-26-de-noviembre), aprobado el 2026-11-25, fija **valores por defecto** para que nadie quede bloqueado (D-022), sin cerrar la decisión:

| Parámetro | Valor por defecto | En `config.py` |
|---|---|---|
| Año final | 2024 | `ANIO_MAX = 2024` |
| Año inicial | Sin límite | `ANIO_MIN = None` |
| Sensibilidad | Desde 2019 | `ANIO_MIN_SENSIBILIDAD = 2019` |
| Antigüedad mínima | No se agrega regla: el año final la cubre (D-021) | — |

El filtro lo aplica `muestra.filtrarMuestra` (S1-11), no la limpieza: `limpiarFechas` solo quita fechas inválidas o posteriores a la fecha de corte de los datos.

## Decisión

_Pendiente._ Se decide con la tabla de `muestra.sensibilidadMuestra` (S1-12, Alejandra: umbral 30/50/100 × año mínimo todo/2019, en `reports/metrics/03_sensibilidad_muestra.csv`), prevista para la sesión del 2026-11-30.

## Consecuencias

- Con los valores por defecto, la muestra es de 28,708 juegos (≥ 50 reseñas); es la cifra de aceptación del Sprint 1.
- Ni el año ni la antigüedad son variables del modelo (D-013): solo se usan para filtrar, formar cohortes y particionar ([0003](0003-particion-temporal.md)).
- Si la decisión final cambia los años, basta con modificar `config.py`; la partición y las cifras se recalculan.
