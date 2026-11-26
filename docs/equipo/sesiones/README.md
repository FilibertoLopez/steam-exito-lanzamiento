# Registro de sesiones

Una fila por sesión de Zoom (F = Filiberto, D = Diana, A = Alejandra, L = Luis). Las **grabaciones no se suben al repositorio** (son pesadas): se comparten como enlace a la nube de Zoom o a la carpeta compartida del equipo. Los resúmenes y transcripciones sí se guardan aquí porque son texto.

| Fecha | Tema | Asistentes | Notas de sesión | Resumen Zoom | Transcripción | Grabación | Acuerdos |
|---|---|---|---|---|---|---|---|
| 2026-11-22 | Exploración de datos | F, D, A, L | [notas](2026-11-22-exploracion-de-datos.md) | [resumen](resumenes-zoom/2026-11-22-exploracion-de-datos.md) | [txt](transcripciones/2026-11-22-exploracion-de-datos.txt) | [Zoom](https://us06web.zoom.us/rec/share/KMSer_E2vuT2Soo-Bg_wwVoEhs55-5wlIRt8xKIAZ09ZIuJXAZWPwCUpCdLMOwPh.hEf57Mp54VvxGSv1) (código: `6PXv&AUu`) | A-001 a A-007, D-001 a D-009 |
| 2026-11-25 | EDA unificado y plan del Sprint 1 ([agenda](2026-11-25-variables-y-limpieza.md)) | F, D, A, L | [notas](2026-11-25-EDA-y-sprint-1.md) | [resumen](resumenes-zoom/2026-11-25-EDA-y-sprint-1.md) | [txt](transcripciones/2026-11-25-EDA-y-sprint-1.txt) | [Zoom](https://us06web.zoom.us/rec/share/mjXNAyWh82GbfD91i3YbjEi222hi4KIu9pWpb5KuxM1pOwPN-wsJ2bEh0dkBC-jZ.TijxRE8Xf9C7GRUl?startTime=1795650233000) (código: `y@Fo%+V2`) | A-017 a A-020, D-014 a D-019; confirma A-008 a A-016 y D-010 a D-013 |

## Próxima sesión

- **Fecha:** 2026-11-30 (lunes), 21:05 (hora de Ciudad de México), después de la clase de Filiberto
- **Lugar:** Zoom (Filiberto envía la invitación, A-019)
- **Temas previstos:** cierre del Sprint 1, revisión del pipeline integrado de punta a punta, arranque y plan del Sprint 2 (A-014). Ver [notas del 2026-11-25](2026-11-25-EDA-y-sprint-1.md#próxima-sesión).
- **Antes de la sesión:** funciones del Sprint 1 con pruebas y PR abiertos a más tardar el domingo 29 (A-017) y revisión cruzada hecha (A-018).
- **Acuerdos a revisar:** A-003, A-004, A-007 a A-010 y A-012 a A-019 ([acuerdos](../acuerdos.md#acuerdos-abiertos)).

### Preguntas abiertas pendientes

| Pregunta | Origen | Contexto |
|---|---|---|
| ¿Se confirma D-002 (excluir 2025 y 2026)? ¿El periodo empieza en 2010, 2015, 2019 o sin límite inferior? | [2026-11-22](2026-11-22-exploracion-de-datos.md#preguntas-abiertas), [2026-11-25](2026-11-25-EDA-y-sprint-1.md#preguntas-abiertas) | Filiberto señaló el 25-nov que D-002 «todavía no» se decide. La evidencia sale de S1-12 (sensibilidad); decisión [0004](../../decisiones/0004-periodo-de-la-muestra.md). Mientras tanto: hasta 2024 y sin límite inferior (D-022) |
| ¿Las variables derivadas de desarrollador y publisher (D-009) entran en el modelo final? | [2026-11-25](2026-11-25-EDA-y-sprint-1.md#preguntas-abiertas) | Depende de S1-07, S1-08 y de la ablación del Sprint 2 |
| ¿La plataforma (Windows, Mac, Linux) diferencia, si casi todos los juegos son para Windows? | [2026-11-22](2026-11-22-exploracion-de-datos.md#preguntas-abiertas) | No se trató el 25-nov. El EDA unificado indica que Mac y Linux se asocian con +0.05 sobre su cohorte; Windows es casi constante. Se resuelve con S1-03 |

Resueltas el 2026-11-25: el **umbral mínimo de reseñas** queda en 50 por defecto (D-014), con el valor final según la sensibilidad (S1-12).

Al resolver una pregunta en sesión, regístrala en [acuerdos](../acuerdos.md) como acuerdo o decisión y bórrala de esta tabla.

## Grabaciones

- **Dónde:** nube de Zoom de quien organizó la sesión (o carpeta compartida del equipo: _pendiente de definir_).
- **Cómo compartir:** en Zoom → *Grabaciones* → *Compartir* → copiar el enlace (y el código de acceso, si lo tiene) en la columna *Grabación*.
- **Caducidad:** revisa la política de retención de la cuenta de Zoom; si las grabaciones se borran automáticamente, descárgalas a la carpeta compartida.
- El repositorio es privado, pero aun así no publiques aquí enlaces con códigos de acceso si el repositorio se vuelve público.

## Nomenclatura

`AAAA-MM-DD-tema-corto` en minúsculas, con guiones, sin acentos ni espacios. Ejemplo: `2026-11-24-seleccion-variable-objetivo`.
