---
fecha: 2026-11-25
tema: Selección de variables y reparto de la limpieza (agenda)
hora: 18:00
asistentes: [Filiberto, Diana, Alejandra, Luis]
moderador: 
grabacion: 
codigo_grabacion: 
resumen_zoom: resumenes-zoom/2026-11-25-EDA-y-sprint-1.md
transcripcion: transcripciones/2026-11-25-EDA-y-sprint-1.txt
nota_sesion: 2026-11-25-EDA-y-sprint-1.md
---

# 2026-11-25 Selección de variables y reparto de la limpieza

Sesión por Zoom, 18:00 (hora de Ciudad de México), duración prevista: 75 minutos. **Estado: agenda preparada antes de la sesión. Lo que se trató, decidió y acordó está en la nota [2026-11-25 EDA unificado y plan del Sprint 1](2026-11-25-EDA-y-sprint-1.md).** Las tablas de abajo conservan las propuestas tal como se prepararon.

Antes de empezar: activar la grabación en la nube con transcripción, para poder subir después el resumen y la transcripción de Zoom. Definir quién modera y quién toma notas.

**Meta de la sesión:** que al terminar las decisiones que bloquean código estén cerradas, cada integrante tenga asignado su issue y A-008 en adelante queden registrados en [acuerdos.md](../acuerdos.md).

## Agenda

| Min | Punto | Resultado esperado |
|---|---|---|
| 0–5 | Moderador, notas, grabación | Roles definidos |
| 5–15 | Estado del repositorio (punto 0) | Quién repara `main` y cuándo |
| 15–25 | Versión de datos y revisión de acuerdos (puntos 1 y 2) | Archivo oficial y todos lo tienen |
| 25–50 | Selección de variables y decisiones que bloquean código (puntos 3 y 4) | Decisiones 0001 a 0003 cerradas |
| 50–60 | Reparto de la limpieza y carga de trabajo (punto 6) | Todos los issues con responsable |
| 60–68 | Temas sin cerrar, `por-clasificar/` y reglas de integración (puntos 5, 7 y 8) | Cada tema con dueño o aplazado |
| 68–75 | Sprint 2, reporte y próxima sesión (puntos 9 y 10) | Acuerdos leídos en voz alta |

### 0. Estado del repositorio

El esqueleto del pipeline, las reglas de integración y los 18 issues del Sprint 1 ya están en `main`. Todos los issues siguen abiertos y sin responsable asignado en GitHub; no hay PR abiertos.

El merge del PR #2 dejó mezcladas la versión de los datos del 19 de noviembre (150,199 filas) y la del 24 de noviembre (151,023 filas) en tres lugares:

| Archivo | Problema | Arreglo propuesto (A-011 y A-012) |
|---|---|---|
| `notebooks/02_eda.ipynb` | Celdas de dos versiones intercaladas; el archivo probablemente no abre | Restaurar desde el commit `96f8bec` y ejecutarlo con el archivo congelado (Alejandra) |
| `docs/03-analisis-exploratorio.md` | Encabezado duplicado, dos tablas de umbrales distintas, figuras que no existen | Versión reparada: EDA unificado más sección 13 con los análisis de los notebooks 02a a 02d (Alejandra) |
| Notebooks `02a` a `02d` y `notebooks/README.md` | Leen `steam_games.csv.gz` del 19-nov | Adaptarlos a `cargarSlim()` y volver a ejecutarlos (Filiberto) |

### 1. Versión de datos (A-005, propuesta A-008)

| Opción | Filas | Qué implica |
|---|---|---|
| **Versión del 2026-11-24 (propuesta)** | 151,023 × 33 | `config.py`, `data/README.md`, el pipeline y las cifras de aceptación (28,708 juegos) ya dependen de ella. Filiberto vuelve a ejecutar 02a a 02d y refresca las cifras del planteamiento. |
| Versión del 2026-11-19 | 150,199 × 42 | El planteamiento y 02a a 02d ya están calculados, pero hay que rehacer el hash, la verificación y las cifras de aceptación. |

- Confirmar que los cuatro pueden descargar el parquet congelado (dataset privado `steam-games-slim`) y que `verificarVersion()` pasa. Quien no lo logre se queda sin bloqueo solo si lo resuelve hoy.

### 2. Revisión de acuerdos con fecha límite 2026-11-25 (A-002 a A-007)

| ID | Acuerdo | Status al 2026-11-25 | Propuesta |
|---|---|---|---|
| A-002 | Compartir los EDA individuales y propuestas de variables | Los cuatro EDA están en el repo (`por-clasificar/` y unificado en `02_eda`) | Cumplido |
| A-003 | Probar umbrales de reseñas y filtros de antigüedad | La tabla de umbrales está en el EDA; falta la sensibilidad con año mínimo | En curso: S1-12 (Alejandra), 2026-11-30 |
| A-004 | Variables derivadas de desarrolladores | Hay prototipo vectorizado en el EDA §6 | En curso: S1-07 y S1-08 (Diana), 2026-11-28 |
| A-005 | Fecha de corte fija de los datos | Ver punto 1 | Cumplido con A-008 |
| A-006 | Acordar variables y repartir la limpieza | Se atiende en esta sesión | Cerrar hoy |
| A-007 | Idiomas contra proporción de positivas | El EDA ya muestra asociación débil (Spearman ≈ 0.01 con `dif_cohorte`) | En curso: S1-06 (Luis), 2026-11-28 |

### 3. Selección de variables (A-006)

- Criterio: solo variables **disponibles antes del lanzamiento** (columna *Momento* de [02-diccionario-datos.md](../../02-diccionario-datos.md)).
- Propuesta de entrada, a partir del EDA unificado (sección 5 de [03-analisis-exploratorio.md](../../03-analisis-exploratorio.md)):

| Bloque (prefijo) | Variables | Observación del EDA |
|---|---|---|
| `precio_` | Log del precio, gratis, sin dato, rango, percentil dentro del año | Relación no lineal; Pre\*; `precio_log` y `precio_pct_cohorte` correlacionan 0.98 |
| `fecha_` | Mes, día de la semana, mes cíclico, fin de semana | Señal débil |
| `ficha_` | Mac, Linux, plataformas, logros, sitio web, soporte, aviso adulto | Mac y Linux +0.05 sobre su cohorte |
| `gen_` | Multi-hot de géneros, marketing aparte, número de géneros | Early Access y Free to Play se comportan distinto del género |
| `cat_` | Categorías con ≥1 % de los juegos (36) | Sin Steam Trading Cards |
| `idi_` | Número de idiomas, idiomas con audio, inglés, español, chino, ruso | Asociación débil |
| `dev_`, `pub_` | Juegos previos, calidad previa, sin historial, autopublicado | Señal más fuerte; cobertura de 33 % |
| `y_` | Objetivo y variantes | Única fuente de `positive` y `negative` |

- Descartadas como predictoras: todas las POST (incluidas `metacritic_score`, `user_score`), `dlc_count`, `tags`, el año y la antigüedad.

### 4. Decisiones que bloquean código

Un voto rápido por fila. Lo que no se cierre en cinco minutos se anota con responsable y hora límite.

| # | Decisión | Propuesta | Alternativa | Quién ejecuta |
|---|---|---|---|---|
| 1 | Variable objetivo (0001) | `y_pct_pos` principal; `y_bueno` (cuartil superior de la cohorte) secundaria; Wilson y percentil de cohorte como variantes | Percentil de cohorte como objetivo principal (más cercano al planteamiento) | Alejandra |
| 2 | Cómo se mide la mejora frente a la «tasa base de la cohorte» | Comparar contra la media del año anterior y reportar `dif_cohorte` | Predecir `dif_cohorte` | Alejandra |
| 3 | Objetivo de tracción (pregunta secundaria 3 del planteamiento) | Agregar `y_log_resenas` a S1-10 | Quitar la pregunta 3 | Alejandra |
| 4 | Mínimo de reseñas (0002) | 50, con sensibilidad a 30 y 100 | 30 | Cerrado en el EDA |
| 5 | Inicio del periodo (0003) | Sin límite inferior como principal; sensibilidad con todo, 2014 y 2019 | Empezar en 2014 | Alejandra |
| 6 | Partición | 70/15/15 temporal (cortes 2021-11-01 y 2023-08-02); partición agrupada por desarrollador en el Sprint 2 | Solo temporal | Alejandra |
| 7 | Historial del desarrollador (D-011) | 12 meses de madurez, todos los desarrolladores, indicador de «sin historial» | Sin regla de madurez (más correlación y más fuga) | Diana |
| 8 | Variables Pre\* (D-010) | Entran con reserva; ablación en el Sprint 2 | Excluirlas | Equipo |
| 9 | Metacritic y `dlc_count` | Excluidos (D-012) | Metacritic como indicador `has_*` | Equipo |
| 10 | Regla de 12 meses de antigüedad de la muestra | No se agrega: D-002 la cubre | Agregarla | Cerrado en el EDA |

### 5. Preguntas abiertas de la sesión anterior

| Pregunta | Se relaciona con | Propuesta |
|---|---|---|
| Umbral mínimo de reseñas: ¿30, 50 o 100? (también se mencionó 5) | A-003, decisión [0002](../../decisiones/0002-minimo-de-resenas.md) | 50; sensibilidad a 30 y 100 (decisión 4 arriba) |
| ¿La plataforma diferencia, si casi todos los juegos son para Windows? | Propuesta de Luis | Sí: Mac y Linux se asocian con mejor recepción (+0.05); Windows se descarta por ser constante |
| Inicio del periodo: ¿desde 2019, 2018, 2020 o todo el historial? | D-002, decisión [0003](../../decisiones/0003-particion-temporal.md) | Decisión 5 arriba |

### 6. Temas sin cerrar del 2026-11-22

Propuestos o discutidos en la [transcripción](transcripciones/2026-11-22-exploracion-de-datos.txt) sin llegar a acuerdo:

| Hora | Tema | Propuso | Propuesta |
|---|---|---|---|
| 12:52–12:53 | Comparar juegos dentro de su cohorte, o una métrica que combine reseñas y antigüedad | Filiberto | Resuelto: percentil por cohorte y `dif_cohorte` (D-013) |
| 13:02 | Early Access como variable propia | Luis | Resuelto: `gen_mkt_EarlyAccess` (D-005) |
| 13:08–13:09 | Idiomas como mercado potencial (número de hablantes) | Filiberto | Extensión opcional; fuera del Sprint 1 |
| 13:18 | Reportar como hallazgo la menor significancia en desarrolladores novatos | Alejandra | Sprint 2, en la interpretación (Diana: subgrupo `dev_sin_historial`) |
| 13:24 | Unificar el formato de categorías (texto y diccionario hacia 2019) | Alejandra | Resuelto: `parsers.aLista`; el formato no es variable |
| 13:40 | ¿Excluir a los desarrolladores más famosos del modelo? | Filiberto | Análisis de sensibilidad en el Sprint 2 |

### 7. Reparto de la limpieza y de las variables (A-006)

Un responsable por bloque; cada bloque tiene su issue y su archivo en `src/steam_exito/`.

| Bloque | Incluye | Issue | Responsable propuesto | Revisa |
|---|---|---|---|---|
| Fechas | 82 fechas inválidas; filtro de años según D-002 | S1-01 | Filiberto | Alejandra |
| Precios | Precio de 107,500 dólares (D-004); gratuitos y retirados | S1-01, S1-02 | Filiberto | Alejandra |
| Faltantes y listas vacías | `[]` y cadenas vacías como «sin dato» | S1-01 | Filiberto | Alejandra |
| Ficha | Plataformas, logros, sitio y soporte | S1-03 | Filiberto | Alejandra |
| Géneros y categorías | Separar marketing (D-005); quitar no-juegos; unificar formato | S1-04, S1-05 | Luis | Filiberto |
| Idiomas | Limpieza de HTML, conteo y resultado de A-007 | S1-06 | Luis | Filiberto |
| Desarrolladores y publishers | Variables derivadas (A-004, D-006, D-009, D-011) | S1-07, S1-08 | Diana | Luis |
| Auditoría Pre\* | Tabla por año | S1-09 | Diana | Luis |
| Reseñas y muestra | Objetivo, umbral y sensibilidad (A-003, D-008) | S1-10, S1-11, S1-12 | Alejandra | Diana |
| Partición | Temporal 70/15/15 | S1-13 | Alejandra | Diana |
| Integración | `pipeline.py`, notebooks 03 y 04 | S1-14 | Filiberto | Alejandra |
| Reporte | §3 y §4: Filiberto · §5: Luis · §6: Diana · §7: Alejandra | S1-R1 a S1-R4 | Cada quien | Revisión cruzada |

**Carga de trabajo:** Filiberto concentra 4 tareas de código, la sección del reporte S1-R1, las notas de decisión y la actualización de los notebooks 02a a 02d. Preguntar si conviene mover S1-03 (ficha) a otra persona.

**Calendario:** jue 26 a sáb 28 implementación; dom 29 PR y revisión cruzada; lun 30 integración y cierre del Sprint 1; 1 al 8 de diciembre Sprint 2 (entrega del reporte y del repositorio el martes 8, 11:59 p. m.).

### 8. Clasificación de `por-clasificar/` y reglas de integración

| Archivo | Destino propuesto |
|---|---|
| `filiberto/01-planteamiento.md` y `02-diccionario-datos.md` | Ya están en `docs/`; eliminar las copias de `por-clasificar/` |
| `diana/2026-11-24-eda-steam.ipynb` y `.docx` | Integrados en `02_eda` y `docs/03`; conservar el notebook en `notebooks/borradores/` hasta el 8 de diciembre |
| `luis/2026-11-23-eda-steam-v1.ipynb` y `.docx` | Igual que Diana |
| `alejandra/ml-steam-eda.ipynb` | Igual que Diana |

Los `.docx` pesan 131 bytes en el repo, es decir, son punteros de Git LFS; hay que hacer `git lfs pull` para abrirlos.

Reglas de integración (repaso de cinco minutos, detalle en [reglas-de-integracion.md](../reglas-de-integracion.md)): un dueño por archivo, no cambiar nombre, parámetros ni prefijos, sin fuga, `pytest` en verde y revisor cruzado antes del merge.

### 9. Sprint 2 y reporte

- **Plan del Sprint 2** (A-014): baseline (regresión regularizada y la media del año anterior), Random Forest y XGBoost; métricas RMSE, MAE y R²; ablación con y sin Pre\* y con y sin historial del desarrollador; partición agrupada por desarrollador; interpretación; cierre del reporte y presentación. Alejandra trae una propuesta de reparto el lunes 30.
- **Reporte** (A-013): dónde se ensambla, cómo se numeran las figuras, estilo de citas y `references/referencias.bib` (hoy vacío).
- **Presentación:** 20 minutos (15 de exposición y 5 de preguntas), todos participan; la fecha la fija el ITAM.

### 10. Siguiente sesión

- Propuesta: lunes 30 de noviembre, cierre del Sprint 1 e inicio del Sprint 2. Chequeo asíncrono el viernes 27.

## Avances por integrante

| Integrante | Avance desde la sesión anterior | Bloqueos |
|---|---|---|
| Filiberto | Planteamiento y diccionario en `docs/`; notebooks 02 y 02a a 02d; merge de los PR #1 y #2 | Versión de datos de los notebooks 02a a 02d |
| Diana | EDA con historial previo del desarrollador y control de fuga | |
| Alejandra | EDA unificado, esqueleto del pipeline, reglas de integración, 18 issues del Sprint 1 | Reparar el merge del EDA |
| Luis | EDA con análisis de desarrolladores e idiomas | |

## Discusión y decisiones

*(se completa durante la sesión)*

## Acuerdos

Copiar a [acuerdos.md](../acuerdos.md) con su ID (el siguiente libre es A-017; decisiones, D-014). Los acuerdos A-008 a A-016 y las decisiones D-010 a D-013 ya están redactados como propuesta en `acuerdos.md`; en la sesión se confirman, se editan o se cancelan.

| ID | Acuerdo | Responsable | Fecha límite |
|---|---|---|---|
| A-008 | Adoptar la versión congelada del 2026-11-24 y compartir el dataset privado | Alejandra | 2026-11-26 |
| A-009 | Seguir las reglas de integración | Todos | 2026-11-26 |
| A-010 | Cerrar las decisiones 0001 a 0004 | Filiberto | 2026-11-30 |
| A-011 | Reparar `main` (EDA unificado y `docs/03`) | Alejandra | 2026-11-26 |
| A-012 | Adaptar notebooks 02a a 02d y planteamiento a la versión congelada | Filiberto | 2026-11-29 |
| A-013 | Formato del reporte y referencias | Alejandra | 2026-11-27 |
| A-014 | Plan del Sprint 2 | Todos | 2026-11-30 |
| A-015 | Asignar responsables en los issues y corregir el estado del #20 | Alejandra | 2026-11-25 |
| A-016 | Subir resumen, transcripción y grabación de cada sesión | Luis | 2026-11-26 |

## Revisión de acuerdos anteriores

| ID | Status nuevo | Comentario |
|---|---|---|
| A-002 | Cumplido | EDA integrados en `02_eda` y `docs/03` |
| A-003 | En curso | Se cierra con S1-12 |
| A-004 | En curso | S1-07 y S1-08 |
| A-005 | Cumplido | Con A-008 |
| A-006 | En curso | Se cierra en esta sesión |
| A-007 | En curso | S1-06 |

## Revisión de por-clasificar

| Archivo | Decisión (mover a… / eliminar) |
|---|---|
| `filiberto/*` | Eliminar (ya está en `docs/`) |
| `diana/*`, `luis/*`, `alejandra/*` | Mover a `notebooks/borradores/` o eliminar después del 8 de diciembre |

## Próxima sesión

- **Fecha:** 
- **Temas:** 
