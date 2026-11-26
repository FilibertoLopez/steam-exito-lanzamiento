# Equipo

## Integrantes

| Integrante | Usuario GitHub | Rol / áreas principales | Etiqueta |
|---|---|---|---|
| Filiberto | [@FilibertoLopez](https://github.com/FilibertoLopez) | Dueño del pipeline (`pipeline.py`) e integración; limpieza básica, precio, fecha y ficha; registro de sesiones y acuerdos | `resp: Filiberto` |
| Diana | [@dianaba27](https://github.com/dianaba27) | Historial de desarrollador y publisher; auditoría Pre\* | `resp: Diana` |
| Alejandra | [@alename](https://github.com/alename) | Plan de sprints e issues; EDA unificado; objetivo, muestra, sensibilidad y partición | `resp: Alejandra` |
| Luis | [@LuisRabasa](https://github.com/LuisRabasa) | Géneros, filtro de no-juegos, categorías e idiomas | `resp: Luis` |

Roles según el reparto del Sprint 1, aprobado en la [sesión del 2026-11-25](sesiones/2026-11-25-EDA-y-sprint-1.md).

## Dónde está cada cosa

| Necesito… | Ir a |
|---|---|
| Ver qué se acordó, quién es responsable y cómo va | [Acuerdos](acuerdos.md) |
| Ver el resumen, la grabación o la transcripción de una sesión | [Registro de sesiones](sesiones/README.md) |
| Guardar el resumen que generó Zoom | [`sesiones/resumenes-zoom/`](sesiones/resumenes-zoom/README.md) |
| Guardar la transcripción de Zoom | [`sesiones/transcripciones/`](sesiones/transcripciones/README.md) |
| Escribir las notas de una sesión | [Plantilla de sesión](sesiones/plantilla-sesion.md) |
| Ver las tareas del sprint y quién las revisa | [Sprint 1](sprint-1-tareas.md) y [reglas de integración](reglas-de-integracion.md) |
| Saber cómo trabajar con ramas, commits y PRs | [CONTRIBUTING.md](../../CONTRIBUTING.md) |

## Flujo después de cada sesión de Zoom

1. Filiberto (A-016), o quien organizó la sesión, descarga de Zoom el **resumen** (AI Companion) y la **transcripción** (`.vtt`).
2. Los guarda como `AAAA-MM-DD-tema.md` en `sesiones/resumenes-zoom/` y `AAAA-MM-DD-tema.vtt` (o `.txt`) en `sesiones/transcripciones/`.
3. Crea la nota de sesión `sesiones/AAAA-MM-DD-tema.md` a partir de la plantilla.
4. Agrega una fila al [registro de sesiones](sesiones/README.md) con el enlace a la grabación en la nube.
5. Copia los acuerdos nuevos a [acuerdos.md](acuerdos.md) con responsable, fecha límite y status.
6. Hace commit y push (o abre un PR) con el mensaje `Sesión AAAA-MM-DD: tema`.
