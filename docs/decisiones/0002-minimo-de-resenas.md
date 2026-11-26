---
id: 0002
estado: aceptada (valor por defecto; el valor final depende de S1-12)
fecha: 2026-11-25
sesiones: [2026-11-22, 2026-11-25]
acuerdos: [A-003, D-008, D-014, A-010]
---

# 0002 Mínimo de reseñas

## Contexto

Con pocas reseñas, la proporción de positivas es muy ruidosa. En la [sesión del 2026-11-22](../equipo/sesiones/2026-11-22-exploracion-de-datos.md) se propusieron umbrales de 5, 30, 50 y 100 reseñas y se acordó no ponderar por número de reseñas (D-008). La tabla de umbrales del [EDA §3](../03-analisis-exploratorio.md) (juegos hasta 2024):

| Umbral | Juegos | % del universo | Desv. de `pct_pos` |
|---:|---:|---:|---:|
| 1 | 75,799 | 79.0 | 0.238 |
| 10 | 52,663 | 54.9 | 0.180 |
| 30 | 35,378 | 36.9 | 0.162 |
| **50** | **28,708** | **29.9** | **0.156** |
| 100 | 21,424 | 22.3 | 0.148 |

La dispersión cae con rapidez hasta unas 50 reseñas; después mejora poco y la muestra se reduce.

## Opciones consideradas

1. 5 reseñas (propuesta de Alejandra el 2026-11-22): muestra grande, objetivo ruidoso.
2. 30 reseñas.
3. **50 reseñas** (mencionada por Luis el 2026-11-22; propuesta del EDA).
4. 100 reseñas: menos ruido, muestra más chica y más sesgada hacia juegos con tracción.

## Decisión

En la [sesión del 2026-11-25](../equipo/sesiones/2026-11-25-EDA-y-sprint-1.md) se fijó **50 reseñas como valor por defecto** (`config.UMBRAL_RESENAS = 50`, D-014) para que nadie quede bloqueado en el Sprint 1. La función de sensibilidad de S1-12 (Alejandra) compara 30 y 100 junto con los filtros de antigüedad; con esa tabla se confirma o se cambia el valor.

## Consecuencias

- La muestra describe juegos que lograron cierta tracción, no el catálogo completo; es una limitación que debe declararse en el reporte.
- El historial de desarrollador y publisher promedia la calidad solo entre juegos previos con al menos `config.UMBRAL_RESENAS` reseñas (D-011).
- Si S1-12 cambia el valor, basta con modificar `config.py`.
