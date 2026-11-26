---
id: 0001
estado: aceptada
fecha: 2026-11-25
sesiones: [2026-11-22, 2026-11-25]
acuerdos: [D-003, D-013, A-010]
---

# 0001 Variable objetivo

## Contexto

El proyecto busca qué factores conocidos antes del lanzamiento se asocian con el éxito de un juego en Steam. En la [sesión del 2026-11-22](../equipo/sesiones/2026-11-22-exploracion-de-datos.md) se descartaron como objetivo el precio y los propietarios estimados (D-003). El número de reseñas depende de la antigüedad del juego (sesgo de exposición), mientras que la proporción de reseñas positivas es comparable entre juegos de distintas edades ([EDA §3 y §13.6](../03-analisis-exploratorio.md)).

## Opciones consideradas

1. **Proporción de reseñas positivas** `pct_pos = positive / (positive + negative)`.
2. Límite inferior de Wilson de esa proporción (casi idéntico a `pct_pos` con ≥ 50 reseñas: Spearman 0.974).
3. Percentil de `pct_pos` dentro de la cohorte de lanzamiento (elimina la tendencia temporal por construcción).
4. Volumen de reseñas (tracción), descartado como objetivo principal por el sesgo de antigüedad.

## Decisión

Objetivo principal: **proporción de reseñas positivas** (`y_pct_pos`), confirmada en la [sesión del 2026-11-25](../equipo/sesiones/2026-11-25-EDA-y-sprint-1.md). Como variantes se construyen el límite de Wilson, el percentil por cohorte y la etiqueta de cuartil superior de la cohorte (`y_bueno`) como objetivo de clasificación secundario (S1-10). `dif_cohorte` y los percentiles por cohorte solo se usan para análisis y objetivos secundarios (D-013).

## Consecuencias

- Solo el bloque `y_` puede usar `positive` y `negative` (D-012).
- La muestra depende del umbral mínimo de reseñas ([0002](0002-minimo-de-resenas.md)).
- La distribución es asimétrica a la izquierda (media 0.782, mediana 0.817): reportar MAE además de RMSE.
