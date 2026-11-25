---
titulo: Acuerdos del equipo
actualizado: 2026-11-25
---

# Acuerdos del equipo

Lista única de acuerdos tomados en las sesiones. Cada acuerdo tiene un responsable y un status. Actualiza el status aquí cuando cambie; si el acuerdo necesita discusión o seguimiento detallado, abre un issue con la plantilla **Acuerdo** y enlázalo en la columna *Issue*.

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
| A-002 | 2026-11-22 | Compartir los EDA individuales y propuestas de variables | Todos | 2026-11-25 | En curso | [2026-11-22](sesiones/2026-11-22-exploracion-de-datos.md) |  | En `por-clasificar/` (2026-11-24): Diana (docx, ipynb), Filiberto (planteamiento, diccionario), Luis (docx, ipynb). Falta Alejandra. Falta la propuesta de variables de cada quien. |
| A-003 | 2026-11-22 | Probar umbrales mínimos de reseñas (5, 30, 50, 100) y filtros de antigüedad; medir el impacto en tamaño del dataset y calidad del modelo | Todos | 2026-11-25 | Pendiente | [2026-11-22](sesiones/2026-11-22-exploracion-de-datos.md) |  | Base existente: `notebooks/borradores/antiguedadVsResenas.py` y `percentilesPorCohorte.py`. |
| A-004 | 2026-11-22 | Crear variables derivadas de desarrolladores (juegos previos, curva de aprendizaje, éxito histórico promedio) en lugar de usar su nombre | Todos | 2026-11-25 | Pendiente | [2026-11-22](sesiones/2026-11-22-exploracion-de-datos.md) |  | Evitar fuga de información: calcular solo con juegos lanzados antes de cada juego. |
| A-005 | 2026-11-22 | Definir una fecha de corte fija para la descarga de datos y usar esa versión en todo el proyecto | Todos | 2026-11-25 | Pendiente | [2026-11-22](sesiones/2026-11-22-exploracion-de-datos.md) |  | Transcripción 12:29. Los datos actuales son la versión del 2026-11-19 (descarga de Filiberto). Registrar la fecha en `data/README.md`. |
| A-006 | 2026-11-22 | En la próxima sesión, acordar las variables del modelo a partir de las propuestas de cada integrante y repartir la limpieza de datos | Todos | 2026-11-25 | Pendiente | [2026-11-22](sesiones/2026-11-22-exploracion-de-datos.md) |  | Transcripción 12:47 (propuesta de Diana). Depende de A-002. |
| A-007 | 2026-11-22 | Analizar la relación entre los idiomas y la proporción de reseñas positivas (diagrama de dispersión) antes de incluirlos como variable | Todos | 2026-11-25 | Pendiente | [2026-11-22](sesiones/2026-11-22-exploracion-de-datos.md) |  | Transcripción 13:14–13:15 (propuesta de Luis). No se asignó responsable en la sesión. |

## Acuerdos cerrados

Mueve aquí los acuerdos *Cumplidos* o *Cancelados* para mantener corta la tabla de abiertos.

| ID | Fecha | Acuerdo | Responsable | Fecha de cierre | Status | Sesión | Issue | Notas |
|---|---|---|---|---|---|---|---|---|
| A-001 | 2026-11-22 | Enviar invitación al repositorio de GitHub a los integrantes | Filiberto | 2026-11-23 | Cumplido | [2026-11-22](sesiones/2026-11-22-exploracion-de-datos.md) |  | Invitaciones enviadas el 2026-11-23 a los usuarios de GitHub (no a los correos del ITAM, como se dijo en la sesión). Diana (@dianaba27) y Luis (@LuisRabasa) ya son colaboradores. La de Alejandra (@alename) se reenvió el 2026-11-24 y ya fue aceptada (2026-11-25). |

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

## Reglas

- Un acuerdo = una acción concreta con **un solo responsable** (si son varios, nombra a quien coordina). Si cada integrante debe hacer su parte, usa *Todos* y anota en *Notas* quién ya cumplió.
- IDs consecutivos (`A-001`, `A-002`, …); no se reutilizan.
- Fechas en formato `AAAA-MM-DD`.
- Responsables: Filiberto, Diana, Alejandra o Luis.
