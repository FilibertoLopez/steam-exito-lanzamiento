## Resultados Clave

El equipo completó la integración del análisis exploratorio de datos (EDA) unificado y estructuró el repositorio en GitHub con documentación, acuerdos, decisiones y tareas asignadas por sprint. Alejandra presentó un plan detallado de trabajo colaborativo con reglas de integración, pipeline modular y revisión cruzada entre miembros. El primer sprint tiene como objetivo dejar todo listo para correr el primer modelo predictivo, con entrega de tareas individuales para el **domingo** y reunión de cierre el **lunes a las 9:05 p.m.**

---

## Decisiones Tomadas

- **Variable objetivo confirmada:** proporción de reseñas positivas.
- **Umbral mínimo de reseñas:** valor default establecido en **50**, sujeto a análisis de sensibilidad posterior.
- **Semilla aleatoria unificada:** todos los miembros usarán la misma semilla para garantizar reproducibilidad.
- **Sin procesamiento de lenguaje natural (NLP):** descartado para esta etapa del proyecto.
- **Sin ponderación por número de reseñas:** la muestra se define únicamente con el umbral mínimo y el filtro de antigüedad.
- **Desarrollador y publisher:** se conservan mediante variables derivadas a partir de su historial, no como variables directas.
- **Etiquetas de marketing** (ej. *Free to Play*): se separan de los géneros en una variable distinta.
- **Registro atípico eliminado:** juego con precio de $1,007 USD excluido del dataset.
- **Datos de referencia:** se usará la descarga realizada por Alejandra el día anterior como dataset congelado base.
- **Lenguaje de código:** Python como estándar del equipo; R disponible solo si algún miembro lo requiere individualmente.
- **Convención de nombres:** *camelCase* (primera palabra en minúscula, siguientes con mayúscula inicial) para estandarizar variables y funciones.

---

## Estructura del Repositorio

Filiberto presentó la organización del repositorio en GitHub, que incluye los siguientes directorios principales:

- **`docs/`** — Documentación del proyecto: planteamiento del problema, diccionario de datos, EDA, ingeniería de variables, selección de modelos, evaluación e interpretación. También contiene el registro de acuerdos, decisiones, minutas de sesiones y el plan de sprints.
- **`notebooks/`** — Jupyter Notebooks individuales por miembro y el EDA unificado (`02_eda_unificado`).
- **`src/`** **o scripts reutilizables** — Funciones de limpieza de datos compartidas para reutilización por todo el equipo.
- **`data/`** — Datos crudos (~1 GB); aún pendiente de subir al repositorio de forma completa.
- **`reports/`** — Imágenes del EDA, tablas y matrices de métricas organizadas en subcarpetas (`figures/`, `metrics/`).
- **`references/`** — Artículos académicos sobre la industria de videojuegos para apoyar la presentación final.
- **Directorios individuales** — Cada integrante tiene su propio espacio de trabajo para desarrollo independiente antes de integrar al pipeline.

El repositorio también incluye grabaciones de sesiones Zoom, transcripciones automáticas y notas editables por sesión, accesibles desde el documento de registro de sesiones.

---

## Plan del Sprint 1: Limpieza e Ingeniería de Variables

### Alcance

El objetivo del sprint es construir un **pipeline modular de extremo a extremo** que deje los datos listos para entrenar el primer modelo predictivo. Cada función recibe un input definido y produce un output estándar, permitiendo encadenarlas como un pipeline reutilizable.

### Reglas de Integración

- Cada miembro desarrolla **sus propias funciones** en su archivo individual; nadie edita el archivo de otro.
- Todas las funciones deben ser **puras** (sin efectos secundarios) y seguir las convenciones de nombres acordadas.
- Se incluye al menos **una prueba unitaria por función** usando un mini-dataset sintético ya preparado.
- Flujo de trabajo Git: rama propia → prueba con mini-data → *pull request* a `main` para revisión cruzada.

### Revisión Cruzada Asignada

- **Filiberto** revisa a **Alejandra**
- **Alejandra** revisa a **Diana**
- **Diana** revisa a **Luis Alberto**
- **Luis Alberto** revisa a **Filiberto**

### Tareas por Miembro

- **Filiberto:** limpieza básica del dataset y responsable del pipeline principal.
- **Alejandra:** análisis de sensibilidad de umbrales (reseñas mínimas y antigüedad) para evaluar impacto en el dataset y calidad del modelo.
- **Diana y Luis Alberto:** funciones de ingeniería de variables y limpieza complementaria (ej. filtrar registros que no son juegos).

---

## EDA Unificado y Hallazgos Relevantes

Alejandra integró los análisis exploratorios individuales de todos los miembros en un notebook unificado (`02_eda_unificado`), disponible en la rama de recuperación del repositorio.

- Todas las **imágenes y tablas** del EDA están organizadas en `reports/figures/` y `reports/metrics/`.
- Se identificó que la **correlación entre dos variables analizadas es de apenas 0.01**, lo que indica una asociación débil sin impacto significativo en el modelo.
- Algunas variables marcadas con **estrellita** corresponden a datos disponibles solo después del lanzamiento (ej. precio), lo que representa una **debilidad metodológica conocida** que se documentará explícitamente en el reporte final.
- El EDA se considera **cerrado**; se actualizó la fecha de corte de los datos.
- Se detectaron conflictos menores en notebooks de Filiberto al integrar con el EDA unificado; están marcados para corrección pero no bloquean el avance.

---

## Gestión de Tareas con GitHub Issues

El equipo adoptó **GitHub Issues** como herramienta de seguimiento de tareas del sprint.

- Cada miembro tiene sus issues asignados con etiquetas de color por persona (*labels*).
- La descripción detallada de cada tarea (qué desarrollar, cómo integrarlo, dónde consultar) está en `docs/equipo/sprint_1`.
- Los issues sirven tanto para reporte de errores como para tracking de progreso.

---

## Pendiente de Confirmación

- **Años a excluir:** definir si se eliminan juegos lanzados en 2025 y 2026, y si el filtro de antigüedad inicia en 2010, 2015 u otro año.
- **Tamaño del dataset:** evaluar si conviene reducir el archivo de datos (~1 GB) para facilitar que cada miembro lo ejecute localmente.
- **Variables derivadas del desarrollador/publisher:** confirmar si se usarán en el modelo final a partir de su historial.
- **Notebooks de Filiberto:** resolver los conflictos de bases de datos detectados al integrar con el EDA unificado.

---

## Elementos de Acción

- **Todos los miembros:** completar sus funciones asignadas del sprint (limpieza e ingeniería de variables) antes del **domingo**.
- **Alejandra:** subir el dataset congelado (descarga del día anterior) al directorio `data/raw/` del repositorio.
- **Filiberto:** enviar invitación de Zoom para la reunión del lunes a las **9:05 p.m.**
- **Filiberto:** actualizar el documento de acuerdos y decisiones tras cada sesión.
- **Todos:** revisar la tarea asignada del compañero según el esquema de revisión cruzada antes de la reunión del lunes.

---

## Próxima Reunión

- **Fecha:** lunes (próxima semana)
- **Hora:** 9:05 p.m. (después de la clase de Filiberto, que termina a las 9:00 p.m.)
- **Objetivo:** cierre del Sprint 1, revisión del pipeline integrado de punta a punta y arranque del Sprint 2 (modelado).
