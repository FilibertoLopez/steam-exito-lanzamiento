---
id: 0003
estado: aceptada
fecha: 2026-11-25
sesiones: [2026-11-22, 2026-11-25]
acuerdos: [D-020, A-010]
---

# 0003 Partición temporal

## Contexto

La media de la proporción de reseñas positivas por año de lanzamiento sube de 0.713 (2014) a 0.834 (2024) ([EDA §4](../03-analisis-exploratorio.md), Figura 6). Una partición aleatoria mezclaría épocas y sobreestimaría el desempeño: el modelo vería juegos «del futuro» al entrenar. El planteamiento pide simular la predicción de lanzamientos nuevos, así que el conjunto de prueba debe ser posterior al de entrenamiento.

El periodo de la muestra (años de inicio y fin) se trata aparte, en [0004](0004-periodo-de-la-muestra.md); la partición se aplica sobre la muestra que resulte de esa decisión.

## Opciones consideradas

1. **Temporal 70/15/15 por fecha de lanzamiento** (propuesta del EDA §4).
2. Aleatoria estratificada: más sencilla, pero con fuga temporal por la deriva de `pct_pos`.
3. Agrupada por desarrollador (ningún desarrollador en dos conjuntos): evita que el modelo memorice estudios; se deja como prueba de robustez del Sprint 2 (A-014).

## Decisión

Partición **temporal 70/15/15 por fecha de lanzamiento**, aprobada en la [sesión del 2026-11-25](../equipo/sesiones/2026-11-25-EDA-y-sprint-1.md) junto con el plan del [Sprint 1](../equipo/sprint-1-tareas.md#decisiones-previas-cerrar-el-26-de-noviembre) (D-020):

| Conjunto | Juegos | Desde | Hasta | Media de `pct_pos` |
|---|---:|---|---|---:|
| Train | 20,098 | 1997-06-30 | 2021-11-01 | 0.764 |
| Valid | 4,311 | 2021-11-02 | 2023-08-02 | 0.815 |
| Test | 4,299 | 2023-08-03 | 2024-12-31 | 0.831 |

Cifras con la muestra por defecto (≥ 50 reseñas, hasta 2024: 28,708 juegos). Las fracciones viven en `config.FRACCION_TRAIN` y `config.FRACCION_VALID`; los cortes se calculan por cuantiles de fecha y **nunca parten un mismo día** entre dos conjuntos. La implementa `evaluacion.particionTemporal` (S1-13, Alejandra), que guarda las fechas de corte en `reports/metrics/`.

## Consecuencias

- Referencia mínima: predecir la media del train en el test da RMSE = 0.150 con un sesgo de +0.067 (desviación del test: 0.135). Todo modelo debe superarla y el sesgo debe reportarse.
- La «tasa base de la cohorte» (hipótesis nula) se evalúa con la media del año anterior, no con la del propio año.
- Si cambian el umbral (0002) o el periodo (0004), los cortes se recalculan solos; solo cambian las cifras de la tabla.
- La partición agrupada por desarrollador se evalúa en el Sprint 2 como prueba de robustez.
