# Equipo

## Integrantes

| Integrante | Usuario GitHub | Rol / áreas principales | Etiqueta |
|---|---|---|---|
| Filiberto | [@FilibertoLopez](https://github.com/FilibertoLopez) | _por definir_ | `resp: Filiberto` |
| Diana | [@dianaba27](https://github.com/dianaba27) | _por definir_ | `resp: Diana` |
| Alejandra | [@alename](https://github.com/alename) | _por definir_ | `resp: Alejandra` |
| Luis | [@LuisRabasa](https://github.com/LuisRabasa) | _por definir_ | `resp: Luis` |

## Dónde está cada cosa

| Necesito… | Ir a |
|---|---|
| Ver qué se acordó, quién es responsable y cómo va | [Acuerdos](acuerdos.md) |
| Ver el resumen, la grabación o la transcripción de una sesión | [Registro de sesiones](sesiones/README.md) |
| Guardar el resumen que generó Zoom | [`sesiones/resumenes-zoom/`](sesiones/resumenes-zoom/README.md) |
| Guardar la transcripción de Zoom | [`sesiones/transcripciones/`](sesiones/transcripciones/README.md) |
| Escribir las notas de una sesión | [Plantilla de sesión](sesiones/plantilla-sesion.md) |
| Saber cómo trabajar con ramas, commits y PRs | [CONTRIBUTING.md](../../CONTRIBUTING.md) |

## Flujo después de cada sesión de Zoom

1. Quien organizó la sesión descarga de Zoom el **resumen** (AI Companion) y la **transcripción** (`.vtt`).
2. Los guarda como `AAAA-MM-DD-tema.md` en `sesiones/resumenes-zoom/` y `AAAA-MM-DD-tema.vtt` en `sesiones/transcripciones/`.
3. Crea la nota de sesión `sesiones/AAAA-MM-DD-tema.md` a partir de la plantilla.
4. Agrega una fila al [registro de sesiones](sesiones/README.md) con el enlace a la grabación en la nube.
5. Copia los acuerdos nuevos a [acuerdos.md](acuerdos.md) con responsable, fecha límite y status.
6. Hace commit y push (o abre un PR) con el mensaje `Sesión AAAA-MM-DD: tema`.
