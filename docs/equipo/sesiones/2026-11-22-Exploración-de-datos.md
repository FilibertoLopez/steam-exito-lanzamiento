---
fecha: 2026-11-22
tema: Exploración de datos
hora: 12:07–13:45
asistentes: [Filiberto, Diana, Alejandra, Luis]
moderador: Filiberto
grabacion: https://us06web.zoom.us/rec/share/KMSer_E2vuT2Soo-Bg_wwVoEhs55-5wlIRt8xKIAZ09ZIuJXAZWPwCUpCdLMOwPh.hEf57Mp54VvxGSv1 
Código de acceso: 6PXv&AUu
resumen_zoom: resumenes-zoom/2026-11-22-Exploración-de-datos.md
transcripcion: transcripciones/2026-11-22-Exploración-de-datos.txt
---

# 2026-11-22 Exploración de datos

Sesión por Zoom de 12:07 a 13:45 (≈ 1 h 38 min). Asistieron los cuatro integrantes; Diana se unió unos minutos después del inicio. Fuentes: [resumen de Zoom](resumenes-zoom/2026-11-22-Exploración-de-datos.md) y [transcripción](transcripciones/2026-11-22-Exploración-de-datos.txt).

## Agenda

1. Planteamiento del problema: factores conocidos antes del lanzamiento que influyen en el éxito de un juego en Steam.
2. Presentación de los análisis exploratorios (EDA) individuales.
3. Estrategia de limpieza y variable objetivo.
4. Organización del trabajo (repositorio compartido).

## Avances por integrante

| Integrante | Lo que presentó | Bloqueos |
|---|---|---|
| Filiberto | Planteamiento del proyecto, diccionario de datos, problemas de calidad y sesgo de antigüedad en el número de reseñas. | — |
| Diana | EDA en Python con 26 variables seleccionadas (identificación, predictoras y reseñas). Faltantes en `metacritic_score` y `recommendations`; listas vacías (`[]`) que no aparecen como NA. Diferencias menores en porcentajes de faltantes respecto a los de Filiberto. | Conexión inestable |
| Alejandra | Notebook en Kaggle con las tres reglas de limpieza: mínimo de reseñas (propuso al menos 5), ~45 % de juegos sin reseñas, 82 fechas inválidas, posible filtro desde 2019. | — |
| Luis | Idiomas vs. reseñas (propuesta de diagrama de dispersión). 94,963 desarrolladores únicos, con concentración en pocos estudios (p. ej. Erotic Games Club, 237 juegos). Umbral de 50 reseñas como opción. | — |

## Hallazgos de datos

- Más de 150,000 juegos y 42 columnas.
- ~95 % de los juegos tiene precio; el resto es gratuito o ya no está en la tienda.
- ~62,000 registros sin reseñas positivas ni negativas, sobre todo juegos muy recientes.
- *Indie* es el género más frecuente; hay categorías que no son juegos (p. ej. *Animation*, *Design*) que deben eliminarse.
- Hasta 103 idiomas registrados, con casos atípicos (p. ej. tigriña).
- 94,963 desarrolladores y ~80,000 publishers: demasiada cardinalidad para usarlos directamente.

## Discusión y decisiones

Registradas en [acuerdos.md](../acuerdos.md#decisiones-vigentes) como D-001 a D-006:

- Repositorio compartido en GitHub (requisito del profesor).
- Excluir juegos lanzados en 2025 y 2026 (historial de reseñas insuficiente).
- Variable objetivo: proporción de reseñas positivas (no precio ni propietarios estimados).
- Eliminar el registro con precio atípico de 107,000 dólares.
- Separar etiquetas de marketing (*Indie*, *Early Access*, *Free to Play*) de los géneros.
- No usar el nombre del desarrollador; derivar variables (juegos previos, éxito histórico promedio).

Decisiones técnicas por formalizar en [decisiones](../../decisiones/): variable objetivo ([0001](../../decisiones/0001-variable-objetivo.md)), mínimo de reseñas ([0002](../../decisiones/0002-minimo-de-resenas.md)) y corte temporal ([0003](../../decisiones/0003-particion-temporal.md)).

## Riesgos

- **Sesgo de antigüedad:** los juegos más viejos acumulan más reseñas por el paso del tiempo.
- **Datos no estáticos:** precio y otras métricas cambian a diario; hace falta una fecha de corte fija.
- **Formato inconsistente:** la columna de categorías cambió de texto a diccionario hacia 2019.
- **Alta cardinalidad** en desarrolladores y publishers.

## Preguntas abiertas

- Umbral mínimo de reseñas: ¿30, 50 o 100? (también se mencionó 5).
- ¿Ponderar por volumen de reseñas, o eso sesga el modelo hacia éxitos conocidos?
- ¿El número o tipo de idiomas se relaciona con el éxito? Revisar con diagrama de dispersión antes de incluirlo.
- ¿La plataforma (Windows, Mac, Linux) diferencia, si casi todos son para Windows?
- Inicio del periodo: ¿desde 2019 (propuesta de Alejandra) o todo el historial?

## Acuerdos

Copiados a [acuerdos.md](../acuerdos.md).

| ID | Acuerdo | Responsable | Fecha límite |
|---|---|---|---|
| A-001 | Enviar invitación al repositorio de GitHub a los integrantes | Filiberto | — |
| A-002 | Compartir los EDA individuales y propuestas de variables | Todos | Próxima sesión |
| A-003 | Probar umbrales de reseñas y filtros de antigüedad (impacto en tamaño y calidad) | Todos | Próxima sesión |
| A-004 | Crear variables derivadas de desarrolladores (curva de aprendizaje, éxito histórico) | Todos | Próxima sesión |

## Revisión de acuerdos anteriores

Primera sesión registrada; no hay acuerdos anteriores.

## Revisión de por-clasificar

| Archivo | Decisión (mover a… / eliminar) |
|---|---|
|  |  |

## Próxima sesión

- **Fecha:** _por definir_
- **Temas:** revisión de EDA individuales, elección de variables predictoras, reparto de la limpieza.
