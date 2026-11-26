
| # | Hallazgo | Evidencia | Decisión para el pipeline |
|---|---|---|---|
| 1 | Cada EDA usó una descarga distinta | 145,257 a 151,023 filas; 62,178 a 67,929 juegos sin reseñas | Una versión congelada (150,643 filas, 24-nov-2026), verificada con `verificarVersion` |
| 2 | Filas a eliminar | 82 fechas inválidas, 2 precios de 107,500 USD (ambos de 2026), 1,555 no-juegos | `limpiarFechas`, `limpiarPrecios`, `quitarNoJuegos` |
| 3 | Muy pocos juegos tienen reseñas | 21 % del universo hasta 2024 sin reseñas; muestra de 28,709 con ≥50 | Umbral 50 (sensibilidad 30 y 100); declarar el sesgo de selección |
| 4 | El umbral reduce el ruido | Desv. de pct_pos: 0.238 (≥1) → 0.156 (≥50) | `UMBRAL_RESENAS = 50` |
| 5 | Objetivo asimétrico | Media 0.782, mediana 0.817, asimetría -1.06 | Reportar RMSE y MAE; objetivo `y_pct_pos`, secundario `y_bueno` |
| 6 | Wilson ≈ proporción cruda con ≥50 reseñas | Spearman 0.974 | No se usa Wilson como objetivo principal |
| 7 | Deriva temporal de la recepción | Media 0.712 (2014) → 0.834 (2024); sesgo del baseline en test +0.067 | Partición temporal; cortes 2021-11-01 y 2023-08-02; año y antigüedad **no** son variables |
| 8 | El formato de `genres`/`categories` es un artefacto | Diferencia global +0.065, dentro del año +0.006 | `parsers.aLista`; el formato no es variable |
| 9 | D-002 cubre la antigüedad mínima | 2025–2026 concentran los juegos de menos de 12 meses | No se agrega una regla de antigüedad adicional |
| 10 | Precio: relación no lineal con la recepción | Spearman log-precio vs dif_cohorte +0.044; gratis -0.008 vs su cohorte | `precio_log`, `precio_es_gratis`, `precio_rango`, `precio_pct_cohorte` |
| 11 | Mac y Linux se asocian con mejor recepción (posible proxy del esfuerzo del estudio) | Mac +0.052, Linux +0.053 (dif_cohorte, con − sin soporte) | Conservar mac y linux; descartar windows (constante) |
| 12 | Los géneros se distinguen moderadamente | Massively Multiplayer -0.108; Casual +0.010 | Multi-hot; marketing separado (D-005) |
| 13 | Las funciones del producto se asocian con la recepción | Mejor: Remote Play on TV +0.056; peor: Online Co-op -0.041 | Multi-hot de categorías con ≥1 %; excluir Trading Cards |
| 14 | Idiomas: asociación débil con la recepción | Spearman +0.011 vs dif_cohorte | `idi_n_idiomas`, `idi_n_audio` con reserva (Pre\*) |
| 15 | El historial del desarrollador es la señal más fuerte | Spearman 0.475 con regla de madurez (0.540 sin ella); cobertura 33% | `dev_pct_pos_previo` con 12 meses de madurez + indicador de cold start; reportar con y sin historial |
| 16 | Variables POST correlacionan con el objetivo | Spearman máximo 0.58 entre las variables con ≥10 % de cobertura | Excluir todas; solo `positive`/`negative` construyen el objetivo |
| 17 | Las variables Pre* cambian con la época y pueden acumular señal posterior | 4.4 idiomas medios en 2012 vs 7.1 en 2024; categorías 5.4 vs 3.6 | Auditoría por año, ablación con/sin Pre* en el Sprint 2, limitación declarada |
