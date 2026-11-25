---
titulo: Acuerdos del equipo
actualizado: 2026-11-24
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
| A-001 | 2026-11-22 | Enviar invitación al repositorio de GitHub a los integrantes | Filiberto | — | En curso | [2026-11-22](sesiones/2026-11-22-exploracion-de-datos.md) |  | Diana (@dianaba27) y Luis (@LuisRabasa) ya son colaboradores; la invitación a Alejandra (@alename) sigue sin aceptarse (2026-11-24). |
| A-002 | 2026-11-22 | Compartir los EDA individuales y propuestas de variables | Todos | Próxima sesión | En curso | [2026-11-22](sesiones/2026-11-22-exploracion-de-datos.md) |  | En `por-clasificar/` (2026-11-24): Diana (docx, ipynb), Filiberto (planteamiento, diccionario), Luis (docx, ipynb). Falta Alejandra. Falta la propuesta de variables de cada quien. |
| A-003 | 2026-11-22 | Probar umbrales mínimos de reseñas (5, 30, 50, 100) y filtros de antigüedad; medir el impacto en tamaño del dataset y calidad del modelo | Todos | Próxima sesión | Pendiente | [2026-11-22](sesiones/2026-11-22-exploracion-de-datos.md) |  | Base existente: `notebooks/borradores/antiguedadVsResenas.py` y `percentilesPorCohorte.py`. |
| A-004 | 2026-11-22 | Crear variables derivadas de desarrolladores (juegos previos, curva de aprendizaje, éxito histórico promedio) en lugar de usar su nombre | Todos | Próxima sesión | Pendiente | [2026-11-22](sesiones/2026-11-22-exploracion-de-datos.md) |  | Evitar fuga de información: calcular solo con juegos lanzados antes de cada juego. |

## Acuerdos cerrados

Mueve aquí los acuerdos *Cumplidos* o *Cancelados* para mantener corta la tabla de abiertos.

| ID | Fecha | Acuerdo | Responsable | Fecha de cierre | Status | Sesión | Issue | Notas |
|---|---|---|---|---|---|---|---|---|

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

## Reglas

- Un acuerdo = una acción concreta con **un solo responsable** (si son varios, nombra a quien coordina). Si cada integrante debe hacer su parte, usa *Todos* y anota en *Notas* quién ya cumplió.
- IDs consecutivos (`A-001`, `A-002`, …); no se reutilizan.
- Fechas en formato `AAAA-MM-DD`.
- Responsables: Filiberto, Diana, Alejandra o Luis.
