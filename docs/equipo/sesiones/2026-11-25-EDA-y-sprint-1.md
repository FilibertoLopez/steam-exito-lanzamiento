---
fecha: 2026-11-25
tema: EDA unificado y plan del Sprint 1
hora: 18:08–18:52
asistentes: [Filiberto, Diana, Alejandra, Luis]
moderador: Filiberto
grabacion: 
codigo_grabacion: 
resumen_zoom: resumenes-zoom/2026-11-25-EDA-y-sprint-1.md
transcripcion: transcripciones/2026-11-25-EDA-y-sprint-1.txt
agenda: 2026-11-25-variables-y-limpieza.md
---

# 2026-11-25 EDA unificado y plan del Sprint 1

Sesión por Zoom de 18:08 a 18:52 (≈ 45 min). Asistieron los cuatro integrantes; Alejandra se conectó a las 18:08 y Diana a las 18:14. Fuentes: [resumen de Zoom](resumenes-zoom/2026-11-25-EDA-y-sprint-1.md) y [transcripción](transcripciones/2026-11-25-EDA-y-sprint-1.txt). La agenda preparada está en [2026-11-25-variables-y-limpieza](2026-11-25-variables-y-limpieza.md); la sesión no la siguió punto por punto, sino que se centró en el recorrido del repositorio y en el plan del Sprint 1.

> La transcripción empieza a las 17:44, antes de la sesión, y hasta las 18:08 contiene audio ambiental del micrófono de Filiberto. Se conserva tal cual la generó Zoom.

## Agenda (como ocurrió)

1. **Recorrido del repositorio** (Filiberto, 18:15–18:29): `README`, `docs/` (índice, decisiones), `src/`, `data/`, `reports/`, `references/`, `R/`, `por-clasificar/`, acuerdos y registro de sesiones.
2. **Plan del Sprint 1** (Alejandra, 18:32–18:40): [sprint-1-tareas.md](../sprint-1-tareas.md), [reglas de integración](../reglas-de-integracion.md), configuración común y datos congelados.
3. **EDA unificado y reportes** (Alejandra, 18:40–18:47): `notebooks/02_eda.ipynb`, [03-analisis-exploratorio.md](../../03-analisis-exploratorio.md), `reports/figures/` y `reports/metrics/`.
4. **Issues de GitHub y acuerdos** (Alejandra, 18:42–18:49).
5. **Fecha de la siguiente sesión** (18:49–18:52).

## Avances por integrante

| Integrante | Avance desde la sesión anterior | Bloqueos |
|---|---|---|
| Filiberto | Estructura del repositorio, acuerdos y registro de sesiones; notebooks 02a a 02f (antigüedad, percentiles por cohorte, género y categoría, top 100, umbral y filtros de años) e idiomas (PR #1 y #21). | Los notebooks 02a a 02d usan otra versión de los datos (A-012). |
| Diana | EDA con historial previo del desarrollador, integrado en el EDA unificado. | — |
| Alejandra | EDA unificado de los cuatro integrantes; esqueleto del pipeline (`src/steam_exito/`, `tests/`, `config.py`); reglas de integración; plan del Sprint 1 con 18 issues; acuerdos A-008 a A-016 y decisiones D-010 a D-013 propuestos. Durante la sesión reparaba el merge del EDA en la rama `alejandra/arreglar-merge-eda`. | Merge del EDA (resuelto con el PR #22 al terminar la sesión). |
| Luis | EDA de desarrolladores e idiomas, integrado en el EDA unificado. Pidió paciencia con el flujo de ramas y PR de Git. | — |

## Discusión

### Recorrido del repositorio (Filiberto)

- `docs/` reúne lo que se presentará al profesor: planteamiento, diccionario, EDA, ingeniería y selección de variables, modelos, evaluación y conclusiones, además de las notas de decisión.
- La presentación final sería tipo PowerPoint, con unos 15 minutos de exposición y 5 de preguntas (según lo que Filiberto recuerda de lo que dijo el profesor).
- `src/steam_exito/` contiene las funciones reutilizables de limpieza para todo el equipo.
- `data/`: Filiberto no había subido los datos (≈ 1 GB) y propuso valorar un juego de datos más pequeño. Quedó resuelto con el parquet *slim* en 8 partes que Alejandra subió a `data/raw/` (PR #23).
- `reports/`: Alejandra explicó que ahí guardó las figuras y tablas del EDA unificado (`figures/`, `metrics/`).
- `references/articulos/`: Filiberto tiene uno o dos artículos sobre la industria de videojuegos, todavía sin subir, útiles para la presentación.
- `R/`: Filiberto dejó de usar R; quien quiera usarlo puede poner ahí su código, pero el estándar es Python.
- Al repasar las decisiones, Filiberto señaló que **D-002** (excluir 2025 y 2026) «todavía no lo decidimos» y que con **D-009** «habría que ver si lo usamos o no». Ambas quedan como preguntas abiertas.
- Filiberto se comprometió a llenar el registro de sesiones después de cada sesión.

### Plan del Sprint 1 (Alejandra)

- **Alcance:** dejar todo listo para correr el primer modelo (carga, limpieza e ingeniería de variables). El Sprint 2 cubre el baseline, el ajuste de modelos y la interpretación.
- **Calendario:** tareas terminadas el **domingo 29**; reunión de cierre e integración el **lunes 30**.
- **Pipeline modular:** cada función recibe un insumo definido y devuelve una salida estándar. Hay dos tipos de funciones: pasos de limpieza y bloques de variables. Filiberto es el dueño del pipeline (`pipeline.py`).
- **Reglas de integración:** cada quien trabaja en su propio archivo y nadie edita el de otro; funciones puras; nombres en lowerCamelCase; semilla común; reglas antifuga; al menos una prueba por función con el mini-dataset sintético (`tests/datos_mini.py`); rama propia, `pytest` en verde y PR a `main`.
- **Revisión cruzada:** un revisor por persona, según la tabla de [reglas-de-integracion.md](../reglas-de-integracion.md) (ver la nota sobre el resumen de Zoom más abajo).
- **Datos:** se usa la descarga de Alejandra del 2026-11-24 como versión congelada, en `data/raw/` por ser los datos tal como se descargaron; los datos limpios irán a otro directorio. Filiberto estuvo de acuerdo en no usar la del 19-nov.
- **Umbral de reseñas:** 50 por defecto en `config.py`; la función de sensibilidad de Alejandra (S1-12) generará la tabla para decidir el umbral y la antigüedad.
- **Dependencias:** hay dependencias menores (`config`, `parsers`, `contrato`), ya en `main`. El filtro de no-juegos de Luis (S1-04) no bloquea a los demás.

### EDA unificado (Alejandra)

- `docs/03-analisis-exploratorio.md` resume el EDA unificado de los cuatro integrantes y conserva los hallazgos de cada EDA individual.
- Idiomas contra proporción de reseñas positivas: correlación de 0.01, una asociación débil (A-007).
- Las variables marcadas con asterisco (Pre\*), como el precio, son anteriores al lanzamiento, pero el valor guardado es el de la tienda el día de la descarga. Es una debilidad conocida que se explicará en el reporte (D-010).
- **El EDA se da por cerrado**, con la fecha de corte de los datos actualizada.
- Los notebooks 02a a 02d de Filiberto usan una versión distinta de los datos; Alejandra los dejó marcados para corregir (A-012). No bloquean el sprint.
- El formato del reporte oficial se verá después (A-013).

### Issues de GitHub

- Cada tarea del Sprint 1 es un issue con etiqueta de responsable (`resp: …`, color azul); para ver las propias, filtrar por *Labels*.
- El detalle de cada tarea (qué desarrollar, cómo integrarlo, dónde consultar) está en [sprint-1-tareas.md](../sprint-1-tareas.md).
- Los issues sirven para dar seguimiento a las tareas y para reportar errores.

## Decisiones

Registradas en [acuerdos.md](../acuerdos.md#decisiones-vigentes):

- **Se confirman** los acuerdos A-008 a A-016 y las decisiones D-010 a D-013 que Alejandra propuso; se presentaron y nadie se opuso. A-016 cambia de responsable: Filiberto.
- **D-014** Umbral mínimo de 50 reseñas por defecto; el valor final sale de la sensibilidad (S1-12).
- **D-015** Semilla única para todo el equipo (`config.SEMILLA`).
- **D-016** Python como lenguaje del proyecto; R solo si alguien lo necesita para su trabajo individual.
- **D-017** Nomenclatura lowerCamelCase para funciones y variables de código.
- **D-018** Seguimiento de tareas con GitHub Issues y etiquetas de responsable.
- **D-019** El EDA queda cerrado; las correcciones de los notebooks 02a a 02d no bloquean el Sprint 1.

Se mantienen sin cambio D-007 (sin procesamiento de lenguaje natural), D-008 (sin ponderar por número de reseñas), D-005 (etiquetas de marketing aparte) y D-004 (registro de precio atípico eliminado).

## Acuerdos

Copiados a [acuerdos.md](../acuerdos.md).

| ID | Acuerdo | Responsable | Fecha límite |
|---|---|---|---|
| A-017 | Terminar las funciones asignadas del Sprint 1, con sus pruebas, y abrir el PR | Todos | 2026-11-29 |
| A-018 | Revisar el PR del compañero asignado según la revisión cruzada | Todos | 2026-11-30 |
| A-019 | Enviar la invitación de Zoom para el lunes 30 a las 21:05 | Filiberto | 2026-11-29 |
| A-020 | Subir el dataset congelado del 24-nov a `data/raw/` | Alejandra | 2026-11-25 |

## Revisión de acuerdos anteriores

| ID | Status nuevo | Comentario |
|---|---|---|
| A-003 | En curso | Umbral de 50 por defecto; la tabla de sensibilidad sale de S1-12. |
| A-004 | En curso | S1-07 y S1-08 (Diana). |
| A-006 | Cumplido | Reparto aprobado en la sesión: [sprint-1-tareas.md](../sprint-1-tareas.md) e issues #3 a #20. |
| A-007 | En curso | Correlación de 0.01 en el EDA; se cierra con S1-06 (Luis). |
| A-008 | En curso | Versión del 24-nov confirmada y subida a `data/raw/` (PR #23); falta que cada quien confirme `verificarVersion()`. |
| A-009 | En curso | Reglas presentadas en la sesión. |
| A-010 | Pendiente | Se actualizó la nota 0002 con el valor por defecto; faltan 0001 completa, 0003 y 0004. |
| A-011 | Cumplido | PR #22 (`alejandra/arreglar-merge-eda`), con merge el 2026-11-25. |
| A-012 | Pendiente | Alejandra marcó en la sesión los conflictos de versión de datos de los notebooks 02a a 02d. |
| A-013 | Pendiente | Se pospuso en la sesión («eso lo podemos ver después»). |
| A-014 | Pendiente | Se revisa el lunes 30 al cerrar el Sprint 1. |
| A-015 | En curso | Los issues tienen etiqueta de responsable; siguen sin *assignee* en GitHub. |
| A-016 | En curso | Responsable: Filiberto. Resumen y transcripción subidos; falta el enlace a la grabación. |

## Preguntas abiertas

- **D-002 e inicio del periodo:** ¿se excluyen 2025 y 2026? ¿El periodo empieza en 2010, 2015, 2019 o sin límite inferior? La sensibilidad de S1-12 aporta la evidencia.
- **Variables derivadas de desarrollador y publisher (D-009):** ¿entran en el modelo final? Depende de S1-07, S1-08 y de la ablación del Sprint 2.
- **Artículos de la industria:** Filiberto tiene uno o dos artículos por subir a `references/articulos/`.

## Notas sobre el resumen de Zoom

El resumen automático tiene imprecisiones; esta nota es la versión que manda:

| Dice el resumen | Según el repositorio y la transcripción |
|---|---|
| Juego con precio de «$1,007 USD» | Son 2 registros de 107,500 USD, ambos de 2026 (EDA §2; `config.PRECIO_MAX_VALIDO`). D-004 decía 107,000. |
| «Filiberto revisa a Sari Alejandra; Sari Alejandra a Diana; Diana a Luis; Luis a Filiberto» | En la sesión, Alejandra leyó en voz alta la tabla *Autor → Revisa* de las reglas de integración; esa tabla y cada tarea de [sprint-1-tareas.md](../sprint-1-tareas.md) dicen lo contrario: **Alejandra revisa a Filiberto, Diana a Alejandra, Luis a Diana y Filiberto a Luis**. Vale la tabla del repositorio; confirmarlo el lunes 30. |
| Notebook `02_eda_unificado` | Es `notebooks/02_eda.ipynb` (título: «02 Análisis exploratorio unificado»). |
| Tareas en `docs/equipo/sprint_1` | Es [docs/equipo/sprint-1-tareas.md](../sprint-1-tareas.md). |
| Datos (≈ 1 GB) «pendientes de subir» | Ya están en `data/raw/` en 8 partes del parquet *slim* (PR #23, con merge el 2026-11-25). |
| La sensibilidad, a cargo de «Sari Alejandra» como tarea única | Alejandra también tiene el objetivo, la muestra y la partición (S1-10, S1-11, S1-13). Diana tiene el historial y la auditoría Pre\*; Luis, los géneros, las categorías y los idiomas. |
| Correlación de 0.01 «entre dos variables analizadas» | Es idiomas contra proporción de reseñas positivas (A-007). |

## Revisión de por-clasificar

Sin cambios en la sesión. La propuesta de la [agenda](2026-11-25-variables-y-limpieza.md) sigue pendiente.

## Próxima sesión

- **Fecha:** lunes 2026-11-30, 21:05 (hora de Ciudad de México), por Zoom, después de la clase de Filiberto (18:00 a 21:00).
- **Temas:** cierre del Sprint 1, revisión del pipeline integrado de punta a punta, arranque del Sprint 2 (modelado) y plan del Sprint 2 (A-014).
