---
titulo: Acuerdos del equipo
actualizado: 2026-11-25
---

# Acuerdos del equipo

Lista única de acuerdos tomados en las sesiones. Cada acuerdo tiene un responsable y un status. Actualiza el status aquí cuando cambie; si el acuerdo necesita discusión o seguimiento detallado, abre un issue con la plantilla **Acuerdo** y enlázalo en la columna *Issue*.

> Los acuerdos A-008 en adelante y las decisiones D-010 a D-013 son la **propuesta para la sesión del 2026-11-25**. Se confirman (o se editan) en la sesión y después se quita esta nota.

## Status

| Status | Significado |
|---|---|
| Pendiente | Aún no se empieza |
| En curso | Alguien ya está trabajando en él |
| Cumplido | Terminado y revisado por el equipo |
| Bloqueado | No puede avanzar; explicar el motivo en *Notas* |
| Cancelado | Se decidió no hacerlo; explicar el motivo en *Notas* |

## Acuerdos abiertos

| ID | Fecha | Acuerdo | Responsable | Fecha límite | Status | Sesión | Issue | Notas |
|---|---|---|---|---|---|---|---|---|
| A-003 | 2026-11-22 | Probar umbrales mínimos de reseñas (5, 30, 50, 100) y filtros de antigüedad; medir el impacto en tamaño del dataset y calidad del modelo | Alejandra | 2026-11-30 | En curso | [2026-11-22](sesiones/2026-11-22-exploracion-de-datos.md) | [#14](https://github.com/FilibertoLopez/steam-exito-lanzamiento/issues/14) | Base: `notebooks/02_eda.ipynb` (tabla de umbrales) y `02a`, `02b`. Se cierra con S1-12 (`sensibilidadMuestra`). Responsable y fecha límite reasignados el 2026-11-25. |
| A-004 | 2026-11-22 | Crear variables derivadas de desarrolladores (juegos previos, curva de aprendizaje, éxito histórico promedio) en lugar de usar su nombre | Diana | 2026-11-28 | En curso | [2026-11-22](sesiones/2026-11-22-exploracion-de-datos.md) | [#9](https://github.com/FilibertoLopez/steam-exito-lanzamiento/issues/9), [#10](https://github.com/FilibertoLopez/steam-exito-lanzamiento/issues/10) | Evitar fuga: solo juegos previos con ≥12 meses (D-011). Se cumple con S1-07 y S1-08. |
| A-006 | 2026-11-22 | Acordar las variables del modelo a partir de las propuestas de cada integrante y repartir la limpieza de datos | Alejandra | 2026-11-26 | En curso | [2026-11-22](sesiones/2026-11-22-exploracion-de-datos.md) |  | Se cierra en la sesión del 2026-11-25 con el reparto de [sprint-1-tareas.md](sprint-1-tareas.md). |
| A-007 | 2026-11-22 | Analizar la relación entre los idiomas y la proporción de reseñas positivas (diagrama de dispersión) antes de incluirlos como variable | Luis | 2026-11-28 | En curso | [2026-11-22](sesiones/2026-11-22-exploracion-de-datos.md) | [#8](https://github.com/FilibertoLopez/steam-exito-lanzamiento/issues/8) | Se cumple con S1-06. El EDA ya muestra una asociación débil (Spearman ≈ 0.01 con `dif_cohorte`). |
| A-008 | 2026-11-25 | Adoptar la versión congelada del 24-nov-2026 (151,023 filas) como única fuente y no volver a descargar de Kaggle; compartir el dataset privado `steam-games-slim` con todos y comprobar que `verificarVersion()` pasa en cada equipo (cierra A-005) | Alejandra | 2026-11-26 | Pendiente | [2026-11-25](sesiones/2026-11-25-variables-y-limpieza.md) |  | Propuesta. Alternativa descartada: la descarga del 19-nov (150,199 filas), que usan el planteamiento y los notebooks 02a a 02d. |
| A-009 | 2026-11-25 | Seguir las [reglas de integración](reglas-de-integracion.md): un dueño por archivo, no cambiar firmas ni prefijos, `pytest` en verde y revisión cruzada antes del merge | Todos | 2026-11-26 | Pendiente | [2026-11-25](sesiones/2026-11-25-variables-y-limpieza.md) |  | Cada quien lee las reglas, crea su rama y corre `pytest`. Anotar aquí quién ya cumplió. |
| A-010 | 2026-11-25 | Cerrar las decisiones 0001 (objetivo), 0002 (mínimo de reseñas), 0003 (partición e inicio del periodo) y 0004 con los valores acordados en la sesión | Filiberto | 2026-11-30 | Pendiente | [2026-11-25](sesiones/2026-11-25-variables-y-limpieza.md) |  | Filiberto redacta las notas en `docs/decisiones/`. |
| A-011 | 2026-11-25 | Reparar `main`: restaurar `notebooks/02_eda.ipynb` desde el commit `96f8bec`, reemplazar `docs/03-analisis-exploratorio.md` por la versión reparada, ejecutar el notebook con el archivo congelado y subir figuras y tablas (`02_eda_*`) | Alejandra | 2026-11-26 | Pendiente | [2026-11-25](sesiones/2026-11-25-variables-y-limpieza.md) |  | El merge del PR #2 dejó mezcladas la versión del 19-nov y la del 24-nov. |
| A-012 | 2026-11-25 | Adaptar los notebooks 02a a 02d y `docs/01-planteamiento.md` a la versión congelada (usar `cargarSlim()` y la fecha de corte de `config.VERSION_DATOS`), volver a ejecutarlos y actualizar la sección 13 de `docs/03` | Filiberto | 2026-11-29 | Pendiente | [2026-11-25](sesiones/2026-11-25-variables-y-limpieza.md) |  | Incluye actualizar H6 en el planteamiento (el EDA no la respalda) y las cifras de desarrolladores y cohortes. |
| A-013 | 2026-11-25 | Definir el formato y el lugar de ensamble del reporte (documento, numeración de figuras, estilo de citas) y llenar `references/referencias.bib` | Alejandra | 2026-11-27 | Pendiente | [2026-11-25](sesiones/2026-11-25-variables-y-limpieza.md) |  | Los borradores S1-R1 a S1-R4 vencen el 2026-11-30. |
| A-014 | 2026-11-25 | Acordar el plan del Sprint 2 (1 al 8 de diciembre): baseline, modelos, ajuste, ablación con y sin Pre\* y con y sin historial del desarrollador, partición agrupada por desarrollador, interpretación, reporte y presentación | Todos | 2026-11-30 | Pendiente | [2026-11-25](sesiones/2026-11-25-variables-y-limpieza.md) |  | Alejandra prepara la propuesta de tareas; se revisa el lunes 30 al cerrar el Sprint 1. |
| A-015 | 2026-11-25 | Asignar a cada integrante en los issues del milestone Sprint 1 y corregir el estado del #20 (aparece «In review» sin PR) | Alejandra | 2026-11-25 | Pendiente | [2026-11-25](sesiones/2026-11-25-variables-y-limpieza.md) |  | Los 18 issues están abiertos y sin assignee. |
| A-016 | 2026-11-25 | Subir después de cada sesión el resumen de Zoom, la transcripción y el enlace a la grabación | Luis | 2026-11-26 | Pendiente | [2026-11-25](sesiones/2026-11-25-variables-y-limpieza.md) |  | Propuesta de responsable; confirmar en la sesión. |

## Acuerdos cerrados

Mueve aquí los acuerdos *Cumplidos* o *Cancelados* para mantener corta la tabla de abiertos.

| ID | Fecha | Acuerdo | Responsable | Fecha de cierre | Status | Sesión | Issue | Notas |
|---|---|---|---|---|---|---|---|---|
| A-001 | 2026-11-22 | Enviar invitación al repositorio de GitHub a los integrantes | Filiberto | 2026-11-23 | Cumplido | [2026-11-22](sesiones/2026-11-22-exploracion-de-datos.md) |  | Invitaciones enviadas el 2026-11-23 a los usuarios de GitHub (no a los correos del ITAM, como se dijo en la sesión). Diana (@dianaba27) y Luis (@LuisRabasa) ya son colaboradores. La de Alejandra (@alename) se reenvió el 2026-11-24 y ya fue aceptada (2026-11-25). |
| A-002 | 2026-11-22 | Compartir los EDA individuales y propuestas de variables | Todos | 2026-11-25 | Cumplido | [2026-11-22](sesiones/2026-11-22-exploracion-de-datos.md) |  | Los cuatro EDA están en `por-clasificar/` y quedaron integrados en `notebooks/02_eda.ipynb` y `docs/03-analisis-exploratorio.md`. Las variables propuestas se reúnen en [sprint-1-tareas.md](sprint-1-tareas.md). Confirmar en la sesión. |
| A-005 | 2026-11-22 | Definir una fecha de corte fija para la descarga de datos y usar esa versión en todo el proyecto | Todos | 2026-11-25 | Cumplido | [2026-11-22](sesiones/2026-11-22-exploracion-de-datos.md) |  | Se cumple con A-008: versión del 2026-11-24, registrada en `data/README.md` y `config.py`. Confirmar en la sesión. |

## Decisiones vigentes

Decisiones del equipo que condicionan el análisis. No tienen status: siguen vigentes hasta que otra sesión las cambie. Las técnicas se formalizan en [docs/decisiones](../decisiones/).

| ID | Fecha | Decisión | Sesión | Documento afectado |
|---|---|---|---|---|
| D-001 | 2026-11-22 | Usar un repositorio compartido en GitHub, vinculado a los correos del ITAM | [2026-11-22](sesiones/2026-11-22-exploracion-de-datos.md) | — |
| D-002 | 2026-11-22 | Excluir juegos lanzados en 2025 y 2026 por historial de reseñas insuficiente | [2026-11-22](sesiones/2026-11-22-exploracion-de-datos.md) | [0003 Partición temporal](../decisiones/0003-particion-temporal.md), [04 Limpieza](../04-estrategia-limpieza.md) |
| D-003 | 2026-11-22 | Variable objetivo: proporción de reseñas positivas (no precio ni propietarios estimados) | [2026-11-22](sesiones/2026-11-22-exploracion-de-datos.md) | [0001 Variable objetivo](../decisiones/0001-variable-objetivo.md) |
| D-004 | 2026-11-22 | Eliminar el registro con precio atípico de 107,000 dólares | [2026-11-22](sesiones/2026-11-22-exploracion-de-datos.md) | [04 Limpieza](../04-estrategia-limpieza.md) |
| D-005 | 2026-11-22 | Separar etiquetas de marketing (Indie, Early Access, Free to Play) de los géneros; eliminar categorías que no son juegos | [2026-11-22](sesiones/2026-11-22-exploracion-de-datos.md) | [05 Ingeniería de variables](../05-ingenieria-variables.md) |
| D-006 | 2026-11-22 | No usar el nombre del desarrollador como variable; derivar variables a partir de su historial | [2026-11-22](sesiones/2026-11-22-exploracion-de-datos.md) | [05 Ingeniería de variables](../05-ingenieria-variables.md) |
| D-007 | 2026-11-22 | No usar procesamiento de lenguaje natural: se descartan como variables los textos de descripción y de reseñas | [2026-11-22](sesiones/2026-11-22-exploracion-de-datos.md) | [05 Ingeniería de variables](../05-ingenieria-variables.md) |
| D-008 | 2026-11-22 | Por ahora no ponderar por número de reseñas: la muestra se define solo con el umbral mínimo de reseñas y el filtro de antigüedad | [2026-11-22](sesiones/2026-11-22-exploracion-de-datos.md) | [0002 Mínimo de reseñas](../decisiones/0002-minimo-de-resenas.md), [04 Limpieza](../04-estrategia-limpieza.md) |
| D-009 | 2026-11-22 | Por ahora conservar tanto el desarrollador como el publisher, mediante variables derivadas, para controlar el efecto de la fama (complementa D-006) | [2026-11-22](sesiones/2026-11-22-exploracion-de-datos.md) | [05 Ingeniería de variables](../05-ingenieria-variables.md) |
| D-010 *(propuesta)* | 2026-11-25 | Las variables Pre\* (precio, categorías, idiomas: valor actual de la tienda) entran con reserva; se audita la deriva por año y se hace ablación con y sin Pre\* en el Sprint 2 | [2026-11-25](sesiones/2026-11-25-variables-y-limpieza.md) | [05 Ingeniería de variables](../05-ingenieria-variables.md) |
| D-011 *(propuesta)* | 2026-11-25 | El historial de desarrollador y publisher solo cuenta juegos con ≥12 meses de antigüedad y ≥ umbral de reseñas, usa todos los desarrolladores del juego e incluye un indicador de «sin historial» | [2026-11-25](sesiones/2026-11-25-variables-y-limpieza.md) | [05 Ingeniería de variables](../05-ingenieria-variables.md) |
| D-012 *(propuesta)* | 2026-11-25 | Se excluyen las variables POST como predictoras, incluyendo `metacritic_score`, `user_score` y `dlc_count`; `positive` y `negative` solo construyen el objetivo | [2026-11-25](sesiones/2026-11-25-variables-y-limpieza.md) | [05 Ingeniería de variables](../05-ingenieria-variables.md) |
| D-013 *(propuesta)* | 2026-11-25 | `dif_cohorte` y los percentiles por cohorte solo se usan para análisis y objetivos secundarios; ni el año ni la antigüedad son variables | [2026-11-25](sesiones/2026-11-25-variables-y-limpieza.md) | [0001 Variable objetivo](../decisiones/0001-variable-objetivo.md) |

## Reglas

- Un acuerdo = una acción concreta con **un solo responsable** (si son varios, nombra a quien coordina). Si cada integrante debe hacer su parte, usa *Todos* y anota en *Notas* quién ya cumplió.
- IDs consecutivos (`A-001`, `A-002`, …); no se reutilizan.
- Fechas en formato `AAAA-MM-DD`.
- Responsables: Filiberto, Diana, Alejandra o Luis.
