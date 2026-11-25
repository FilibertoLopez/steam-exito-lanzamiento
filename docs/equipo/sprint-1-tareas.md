---
titulo: Sprint 1 — Limpieza e ingeniería de variables (hasta el baseline)
ubicacion: docs/equipo/sprint-1-tareas.md
periodo: 2026-11-25 a 2026-11-30
actualizado: 2026-11-25
---

# Sprint 1: limpieza e ingeniería de variables

**Cierre del sprint: lunes 30 de noviembre.** Entrega final del reporte y del repositorio: martes 8 de diciembre, 11:59 p. m.

Cada tarea está lista para pegarse como issue con la plantilla *Tarea* (área, responsable, acuerdo, entregable). Antes de empezar, lee [reglas-de-integracion.md](reglas-de-integracion.md).

## Calendario

| Fecha | Hito |
|---|---|
| **Mié 25 – jue 26** | Filiberto hace merge del esqueleto (`src/`, `tests/`, EDA, `config.py`), congela y comparte la versión de datos y crea los issues. Todos: leer reglas, crear rama, correr `pytest`. Cerrar las decisiones de la sección "Decisiones previas". |
| **Jue 26 – sáb 28** | Cada quien implementa sus funciones y sus pruebas en su rama. |
| **Dom 29** | PR abiertos y revisión cruzada. A más tardar a medianoche, todo con merge o con comentarios resueltos. |
| **Lun 30** | Integración de Filiberto: pipeline de punta a punta, notebooks 03 y 04, `acuerdos.md`. Borradores del reporte entregados. **Cierre del sprint.** |
| Mar 1 – mar 8 de dic. | Sprint 2: baseline, modelos, ajuste, interpretación; cierre del reporte, del repo y de la presentación. |

## Decisiones previas (cerrar el 26 de noviembre)

Con estos valores en `config.py` nadie queda bloqueado. Propuesta por defecto, basada en el EDA unificado.

| Parámetro | Propuesta | Respaldo |
|---|---|---|
| Umbral de reseñas | 50, con sensibilidad a 30 y 100 | Sesión del 22-nov; EDA §3.1 (la desviación baja de 0.238 a 0.156) |
| Periodo | Hasta 2024 (D-002); sin límite inferior (la sensibilidad desde 2019 la corre S1-12) | D-002 |
| Pesos de muestra | Ninguno | D-008 |
| Objetivo principal | `y_pct_pos`; secundario `y_bueno` (cuartil superior de la cohorte) | D-003; EDA §3.2 |
| Antigüedad mínima | No se agrega regla: D-002 la cubre | EDA §3.3 |
| Madurez del historial | 12 meses | EDA §6 |
| Particiones | 70/15/15 por fecha: cortes 2021-11-01 y 2023-08-02 | EDA §4 |
| Variables Pre\* | Entran con reserva (D-010) | EDA §8 |

## Acuerdos y decisiones a registrar en `acuerdos.md`

| ID | Texto |
|---|---|
| A-008 | Adoptar la versión congelada del 24-nov-2026 (151,023 filas) como única fuente; no volver a descargar de Kaggle (cierra A-005) |
| A-009 | Seguir las reglas de integración de `docs/equipo/reglas-de-integracion.md` |
| A-010 | Cerrar las decisiones 0001, 0002 y 0003 con los valores de la tabla anterior (Filiberto redacta las notas) |
| D-010 | Las variables Pre\* entran con reserva; se audita la deriva por año y se hace ablación con/sin Pre\* en el Sprint 2 |
| D-011 | El historial de desarrollador/publisher solo cuenta juegos con ≥12 meses de antigüedad y ≥ umbral de reseñas |
| D-012 | Se excluyen las variables POST como predictoras, incluyendo `metacritic_score` y `user_score` |
| D-013 | `dif_cohorte` y `pct_cohorte` solo se usan para análisis y objetivos secundarios; ni el año ni la antigüedad son variables |

## Resumen por integrante

| Integrante | Funciones de código | Reporte |
|---|---|---|
| **Filiberto** | S1-01 limpieza básica · S1-02 precio y fecha · S1-03 ficha · S1-14 integración y notebooks | §3 Introducción y contexto · §4 Formulación y objetivos |
| **Luis** | S1-04 géneros y no-juegos · S1-05 categorías · S1-06 idiomas | §5 Descripción de las fuentes de datos |
| **Diana** | S1-07 historial de desarrollador · S1-08 historial de publisher · S1-09 auditoría Pre\* | §6 Análisis exploratorio |
| **Alejandra** | S1-10 objetivo · S1-11 muestra · S1-12 sensibilidad · S1-13 partición temporal | §7 Preparación e ingeniería de variables |

Revisores: Alejandra revisa a Filiberto; Diana a Alejandra; Luis a Diana; Filiberto a Luis.

---

## Tareas de código

### S1-01 · Limpieza básica
- **Responsable:** Filiberto · **Área:** Datos y limpieza · **Rama:** `filiberto/s1-01-limpieza-basica` · **Archivo:** `limpieza_basica.py` · **Revisa:** Alejandra
- **Acuerdos:** D-004, A-005, diccionario de datos
- **Funciones:**
  - `convertirTipos(df)`: `mac`, `linux`, `windows` a booleano anulable (usa `parsers.aBooleano`); `achievements` a entero anulable; `price`, `positive`, `negative` numéricos.
  - `limpiarFechas(df)`: `release_date` a datetime; elimina las **82** fechas inválidas y las posteriores a `fecha_max_lanzamiento`. No filtra por año.
  - `limpiarPrecios(df)`: elimina `price > config.PRECIO_MAX_VALIDO` (**2** registros de 107,500 USD, ambos de 2026). Conserva precios nulos (juegos retirados) y el 0 (gratis).
  - `marcarSinDato(df)`: ceros que significan "sin dato" a NaN (`config.COLUMNAS_CERO_ES_NULO`), `estimated_owners` `0 - 0` y `0 .. 0` a NaN, listas vacías a NaN en `config.COLUMNAS_LISTA`. No tocar `full_audio_languages`.
- **Criterios de aceptación:** pruebas con `datos_mini`; sobre los datos reales, `limpiarFechas` quita 82 filas y `limpiarPrecios` quita 2; la bitácora lo registra.

### S1-02 · Variables de precio y de fecha
- **Responsable:** Filiberto · **Área:** Variables · **Archivo:** `variables_precio_fecha.py`
- **Funciones:** `variablesPrecio` (`precio_log`, `precio_es_gratis`, `precio_sin_dato`, `precio_rango`, `precio_pct_cohorte`) y `variablesFecha` (`fecha_mes`, `fecha_dia_semana`, `fecha_mes_sin`, `fecha_mes_cos`, `fecha_es_fin_de_semana`).
- **Reglas:** el precio es el actual (Pre\*), por eso se incluye el percentil dentro del año. **Prohibido** devolver año o antigüedad. `precio_log` y `precio_pct_cohorte` correlacionan ≈ 0.98: dejar documentado cuál se recomienda conservar.
- **Aceptación:** reproduce la tabla de precio del EDA §5.1 (rangos y medias).

### S1-03 · Variables de ficha
- **Responsable:** Filiberto · **Área:** Variables · **Archivo:** `variables_ficha.py`
- **Función:** `variablesFicha`: `ficha_mac`, `ficha_linux`, `ficha_n_plataformas`, `ficha_logros_log`, `ficha_tiene_logros`, `ficha_tiene_sitio`, `ficha_tiene_soporte_url`, `ficha_tiene_correo_soporte`, `ficha_aviso_adulto`.
- **Reglas:** NaN en mac/linux a False; sin `dlc_count` ni `metacritic_score`. Los indicadores salen de las columnas `has_*` del parquet.
- **Aceptación:** el 28.5 % de la muestra tiene soporte Mac y el 19.0 % Linux (EDA §5.2).

### S1-04 · Géneros y filtro de no-juegos
- **Responsable:** Luis · **Área:** Datos y limpieza / Variables · **Rama:** `luis/s1-04-generos` · **Archivo:** `variables_generos.py` · **Revisa:** Filiberto
- **Acuerdos:** D-005
- **Funciones:**
  - `quitarNoJuegos(df)`: mapea variantes traducidas, **ignora** marketing y aviso, y elimina el juego si los géneros restantes existen y todos están en `config.GENEROS_NO_JUEGO`. Debe quitar **1,555** juegos con los datos congelados (la regla ya está validada en el EDA §2.2). Lo que no tiene género no se elimina.
  - `variablesGeneros(df)`: multi-hot de `config.GENEROS_JUEGO`, `gen_mkt_Indie`, `gen_mkt_EarlyAccess`, `gen_mkt_FreeToPlay`, `gen_aviso_maduro`, `gen_n_generos`, `gen_sin_dato`.
- **Aceptación:** 33 géneros distintos tras normalizar; los porcentajes coinciden con la Figura 9 del EDA.

### S1-05 · Categorías de Steam
- **Responsable:** Luis · **Archivo:** `variables_generos.py`
- **Función:** `variablesCategorias(df, frecuenciaMinima=0.01)`: multi-hot de las categorías con ≥1 % de los juegos (36 con los datos congelados), `cat_n_otras`, `cat_n_total`. Excluye `config.CATEGORIAS_EXCLUIR` (Steam Trading Cards).
- **Reglas:** el formato original (texto u objeto) **no** es variable (EDA §2.3). La lista de categorías frecuentes se decide con el universo completo, no por juego.

### S1-06 · Idiomas (incluye A-007)
- **Responsable:** Luis · **Área:** Variables · **Archivo:** `variables_idiomas.py`
- **Función:** `variablesIdiomas(df)`: `idi_n_idiomas`, `idi_n_audio` (NaN si no se sabe), `idi_tiene_ingles`, `idi_tiene_espanol`, `idi_tiene_chino`, `idi_tiene_ruso`, `idi_sin_dato`.
- **Reglas:** usa `parsers.idiomasYAudio` (ya resuelve el formato HTML y los elementos con comas; 28,319 celdas lo necesitan). Cuenta idioma base (lo anterior a « - »). **Pendiente tuyo:** normalizar nombres traducidos o con saltos de línea que aún aparecen (p. ej. "Inglés", "Japonais"): hoy quedan 143 idiomas base, la lista real es de ~100.
- **Entregable adicional (A-007):** gráfica de dispersión idiomas vs. proporción positiva en `reports/figures/`. El EDA ya muestra una asociación débil (Spearman ≈ 0.01 contra `dif_cohorte`); confirma o corrige con tu limpieza más fina.

### S1-07 · Historial del desarrollador
- **Responsable:** Diana · **Área:** Variables · **Rama:** `diana/s1-07-historial-dev` · **Archivo:** `variables_desarrollador.py` · **Revisa:** Luis
- **Acuerdos:** A-004, D-006, D-009
- **Función:** `variablesDesarrollador(df, mesesMinimos, umbralResenas)`: `dev_n_previos`, `dev_n_previos_maduros`, `dev_pct_pos_previo`, `dev_sin_historial`.
- **Reglas:** ver §5 de las reglas de integración. Agrega **todos** los desarrolladores del juego (no solo el primero). El EDA §6 trae un prototipo vectorizado (`historialPrevio`) que puedes adaptar: no re-implementes con `apply` fila por fila.
- **Pruebas obligatorias:** (1) cambiar el `pct_pos` de un juego **futuro** no altera la variable de uno anterior; (2) dos juegos del mismo día no se cuentan entre sí; (3) un juego a menos de 12 meses del siguiente no cuenta como historial maduro.
- **Aceptación:** con los datos reales, `dev_pct_pos_previo` tiene Spearman ≈ 0.48 con `pct_pos` y cobertura de ≈ 33 % de la muestra (EDA §6).

### S1-08 · Historial del publisher
- **Responsable:** Diana · **Archivo:** `variables_desarrollador.py`
- **Función:** `variablesPublisher(...)`: mismas reglas con prefijo `pub_` más `pub_es_autopublicado` y `pub_n_publicados_previos`.
- **Aceptación:** Spearman ≈ 0.45; ≈ 63 % de los juegos están autopublicados.

### S1-09 · Auditoría de variables Pre\*
- **Responsable:** Diana · **Área:** EDA · **Archivo:** `auditoria.py`
- **Función:** `auditarPreEstrella(df)`: tabla por año con precio mediano, % gratis, # idiomas, # idiomas con audio, # categorías, % con logros, % con sitio web, % con correo de soporte.
- **Entregable:** la tabla en `reports/metrics/` y la figura (el prototipo está en EDA §8). Redacta en el reporte el párrafo de limitaciones: las categorías, logros y sitio web son más frecuentes en los juegos viejos; los idiomas y los juegos gratuitos aumentan en los recientes.

### S1-10 · Variable objetivo
- **Responsable:** Alejandra · **Área:** Variables · **Rama:** `alejandra/s1-10-objetivo` · **Archivo:** `muestra.py` · **Revisa:** Diana
- **Acuerdos:** D-003, decisión 0001
- **Función:** `construirObjetivo(df, umbral)`: `y_n_resenas`, `y_pct_pos`, `y_wilson_inf`, `y_pct_cohorte`, `y_bueno`.
- **Reglas:** es el único bloque que puede usar `positive` y `negative`. El percentil de cohorte se calcula solo entre juegos con ≥ umbral reseñas, dentro de cada año. `y_pct_pos` es NaN (no 0) si no hay reseñas.
- **Aceptación:** `y_pct_pos` y `y_wilson_inf` con Spearman ≈ 0.97 en la muestra; `y_bueno` ≈ 25 %.

### S1-11 · Filtro de muestra
- **Responsable:** Alejandra · **Archivo:** `muestra.py`
- **Función:** `filtrarMuestra(df, umbral, anioMax, anioMin)`.
- **Aceptación:** con los valores por defecto devuelve **28,708** juegos (del universo de 95,904 hasta 2024); con umbral 30 devuelve 35,378 y con 100 devuelve 21,424.

### S1-12 · Sensibilidad de la muestra (A-003)
- **Responsable:** Alejandra · **Archivo:** `muestra.py`
- **Función:** `sensibilidadMuestra(df)`: para cada umbral (30/50/100) × año mínimo (todo/2019): # juegos, media y desviación de `y_pct_pos`, % del universo.
- **Entregable:** `reports/metrics/03_sensibilidad_muestra.csv` y una figura. Cierra el acuerdo A-003.

### S1-13 · Partición temporal
- **Responsable:** Alejandra · **Archivo:** `evaluacion.py`
- **Función:** `particionTemporal(df, fraccionTrain, fraccionValid)`: Serie `train/valid/test` indexada por `app_id`, cortando por fecha (nunca partiendo un mismo día).
- **Aceptación:** cortes ≈ 2021-11-01 y 2023-08-02; ≈ 20,098 / 4,311 / 4,299 juegos. Guarda las fechas de corte en `reports/metrics/`.

### S1-14 · Integración y notebooks
- **Responsable:** Filiberto · **Área:** Datos y limpieza · **Fecha:** lunes 30
- **Entregables:** `pipeline.py` corriendo sin pendientes; `notebooks/03_limpieza.ipynb` (embudo de filas, antes y después, figuras de calidad) y `04_ingenieria_variables.ipynb` (tablas de columnas por bloque, correlaciones del resultado); `data/README.md` completo; `acuerdos.md` actualizado; notas de decisión 0001–0004 redactadas.
- **Pruebas de aceptación del sprint:** ver §9 de las reglas de integración.

---

## Tareas de reporte (borradores, entrega el lunes 30)

La estructura del reporte sigue la §4.1.1 de los lineamientos. Cada sección debe ser autocontenida, con tablas y figuras numeradas, tituladas y **explicadas**. Material de apoyo: `notebooks/02_eda.ipynb` y `docs/03-analisis-exploratorio.md` (borrador), `docs/01-planteamiento.md` y `docs/02-diccionario-datos.md`.

| ID | Sección | Responsable | Fuente principal | Notas |
|---|---|---|---|---|
| S1-R1 | §3 Introducción y contexto · §4 Formulación y objetivos | Filiberto | `docs/01-planteamiento.md` | Contexto, relevancia, objetivo general y específicos, preguntas, **justificación del uso de ML** y referencias. Incluir las hipótesis H1–H6 y qué dice el EDA de cada una. |
| S1-R2 | §5 Descripción de las fuentes de datos | Luis | `docs/02-diccionario-datos.md` | Fuente, versión congelada, tabla de variables por momento (Pre/Pre\*/Post) y rol, y el problema de las descargas distintas. |
| S1-R3 | §6 Análisis exploratorio | Diana | `docs/03-analisis-exploratorio.md` | Adaptar el borrador al formato del reporte: texto corrido, figuras numeradas (1 a 15) con interpretación, y la tabla de hallazgos. No pegar capturas sin explicar. |
| S1-R4 | §7 Preparación e ingeniería de variables | Alejandra | `docs/04` y `docs/05` | Esqueleto con qué se limpia, por qué, cuántas filas se quitan en cada paso (embudo) y cada bloque de variables con su justificación. Se completa conforme entra el código. |

**Criterios de calidad** (lineamientos §4.1.2): redacción formal, argumentación técnica, citas de fuentes y metodologías, interpretación en el contexto del problema, coherencia entre objetivos, metodología, resultados y conclusiones.

---

## Plantilla para crear los issues

Usa la plantilla *Tarea* del repositorio. Ejemplo para S1-07:

```
Título: [S1-07] Historial del desarrollador sin fuga
Área: Variables
Responsable: Diana
Acuerdo relacionado: A-004
Descripción: Implementar variablesDesarrollador en src/steam_exito/variables_desarrollador.py
siguiendo la especificación del docstring y las reglas de integración (§3.2 y §5).
Entregable esperado: función + pruebas en tests/test_variables_desarrollador.py;
PR a main revisado por Luis; pipeline sin "desarrollador" en pendientes.
Etiquetas: tipo: tarea, resp: Diana, status: pendiente
```

## Seguimiento

| Tarea | Responsable | Rama | PR | Revisor | Status |
|---|---|---|---|---|---|
| S1-01 | Filiberto | | | Alejandra | Pendiente |
| S1-02 | Filiberto | | | Alejandra | Pendiente |
| S1-03 | Filiberto | | | Alejandra | Pendiente |
| S1-04 | Luis | | | Filiberto | Pendiente |
| S1-05 | Luis | | | Filiberto | Pendiente |
| S1-06 | Luis | | | Filiberto | Pendiente |
| S1-07 | Diana | | | Luis | Pendiente |
| S1-08 | Diana | | | Luis | Pendiente |
| S1-09 | Diana | | | Luis | Pendiente |
| S1-10 | Alejandra | | | Diana | Pendiente |
| S1-11 | Alejandra | | | Diana | Pendiente |
| S1-12 | Alejandra | | | Diana | Pendiente |
| S1-13 | Alejandra | | | Diana | Pendiente |
| S1-14 | Filiberto | | | Alejandra | Pendiente |
| S1-R1 a S1-R4 | ver tabla de reporte | | | cruzada | Pendiente |
