---
fecha: 2026-11-25
tema: Selección de variables y reparto de la limpieza
hora: 18:00
asistentes: [Filiberto, Diana, Alejandra, Luis]
moderador: 
grabacion: 
codigo_grabacion: 
resumen_zoom: resumenes-zoom/2026-11-25-variables-y-limpieza.md
transcripcion: transcripciones/2026-11-25-variables-y-limpieza.txt
---

# 2026-11-25 Selección de variables y reparto de la limpieza

Sesión por Zoom, 18:00 (hora de Ciudad de México). **Estado: agenda preparada; la nota se completa después de la sesión.**

Antes de empezar: activar la grabación en la nube con transcripción, para poder subir después el resumen y la transcripción de Zoom.

## Agenda

1. Revisión de acuerdos con fecha límite 2026-11-25 (A-002 a A-007).
2. EDA de Alejandra (pendiente de A-002).
3. Selección de variables del modelo (A-006).
4. Preguntas abiertas de la sesión anterior.
5. Temas discutidos el 2026-11-22 que quedaron sin cerrar.
6. Reparto de la limpieza de datos (A-006).
7. Clasificación del material en `por-clasificar/`.
8. Formalización de decisiones y pendientes de organización.
9. Fecha de la siguiente sesión.

### 1. Revisión de acuerdos

| ID | Acuerdo | Status al 2026-11-25 | A revisar en sesión |
|---|---|---|---|
| A-002 | Compartir los EDA individuales y propuestas de variables | En curso | Ya están los de Diana, Luis y Filiberto en `por-clasificar/`; falta Alejandra. Nadie ha entregado todavía su lista de variables propuestas. |
| A-003 | Probar umbrales de reseñas y filtros de antigüedad | Pendiente | Resultados de cada quien; el notebook de Diana muestra juegos disponibles según el mínimo de reseñas. Base en `notebooks/02a_antiguedad_resenas.ipynb`, `02b_percentiles_cohorte.ipynb` y la tabla de umbrales de `02_eda.ipynb`. |
| A-004 | Variables derivadas de desarrolladores | Pendiente | El notebook de Diana ya calcula los juegos previos de cada desarrollador con control de fuga. Falta el éxito histórico promedio y la "curva de aprendizaje". |
| A-005 | Fecha de corte fija para la descarga de datos | Pendiente | Propuesta: adoptar la versión del 2026-11-19 que ya usamos y anotarla en `data/README.md`. |
| A-006 | Acordar variables y repartir la limpieza | Se atiende en esta sesión | Puntos 3 y 6. |
| A-007 | Idiomas vs. proporción de reseñas positivas | Pendiente | ¿Alguien hizo el diagrama de dispersión? |

### 2. EDA de Alejandra

- Presentación de su análisis (notebook de Kaggle) y subida a `por-clasificar/alejandra/`.

### 3. Selección de variables (A-006)

- Reunir la lista de variables propuestas por cada integrante.
- Criterio: solo variables **disponibles antes del lanzamiento** (ver la columna *Momento* del borrador de diccionario en `por-clasificar/filiberto/02-diccionario-datos.md`).
- Decidir para cada una: entra, entra derivada (con qué transformación) o se descarta.

### 4. Preguntas abiertas de la sesión anterior

| Pregunta | Se relaciona con |
|---|---|
| Umbral mínimo de reseñas: ¿30, 50 o 100? (también se mencionó 5) | A-003, decisión [0002](../../decisiones/0002-minimo-de-resenas.md) |
| ¿La plataforma (Windows, Mac, Linux) diferencia, si casi todos los juegos son para Windows? | Propuesta de Luis de analizarla contra las reseñas |
| Inicio del periodo: ¿desde 2019, 2018, 2020 o todo el historial? | D-002, decisión [0003](../../decisiones/0003-particion-temporal.md) |

### 5. Temas sin cerrar del 2026-11-22

Propuestos o discutidos en la [transcripción](transcripciones/2026-11-22-exploracion-de-datos.txt) sin llegar a acuerdo:

| Hora | Tema | Propuso |
|---|---|---|
| 12:52–12:53 | Comparar juegos dentro de su cohorte de lanzamiento, o crear una métrica que combine reseñas y antigüedad | Filiberto |
| 13:02 | Early Access como variable propia | Luis |
| 13:08–13:09 | Convertir los idiomas en mercado potencial (número de hablantes) | Filiberto |
| 13:18 | Reportar como hallazgo la menor significancia en desarrolladores novatos | Alejandra |
| 13:24 | Unificar el formato de la columna de categorías (texto → diccionario hacia 2019) | Alejandra |
| 13:40 | ¿Excluir a los desarrolladores más famosos del modelo? | Filiberto |

### 6. Reparto de la limpieza (A-006)

Asignar un responsable por bloque; cada bloque se convierte en un acuerdo con fecha límite.

| Bloque | Incluye | Responsable |
|---|---|---|
| Fechas | 82 fechas inválidas; filtro de años según D-002 y la pregunta del inicio del periodo | |
| Precios | Precio de 107,000 dólares (D-004); juegos gratuitos y retirados | |
| Reseñas y muestra | Umbral mínimo (A-003, D-008); juegos sin reseñas | |
| Géneros y categorías | Separar etiquetas de marketing (D-005); quitar categorías que no son juegos; unificar el formato de categorías | |
| Idiomas | Limpieza del texto (marcas HTML) y conteo; resultado de A-007 | |
| Desarrolladores y publishers | Variables derivadas (A-004, D-006, D-009) | |
| Faltantes y listas vacías | `[]` y cadenas vacías como «sin dato»; `metacritic_score`, `recommendations` | |

### 7. Clasificación de `por-clasificar/`

| Archivo | Destino propuesto |
|---|---|
| `filiberto/01-planteamiento.md` | `docs/01-planteamiento.md` |
| `filiberto/02-diccionario-datos.md` | `docs/02-diccionario-datos.md` |
| `diana/2026-11-24-eda-steam.ipynb` y `.docx` | `notebooks/02_eda.ipynb` (como base) y `docs/03-analisis-exploratorio.md` |
| `luis/2026-11-23-eda-steam-v1.ipynb` y `avance-eda-steam-v1.docx` | `notebooks/borradores/` y `docs/03-analisis-exploratorio.md` |

Pregunta: ¿unificamos los tres EDA en un solo `02_eda.ipynb` y un solo `03-analisis-exploratorio.md`? ¿Quién lo hace?

### 8. Decisiones y organización

- ¿Quién redacta las notas de decisión [0001 Variable objetivo](../../decisiones/0001-variable-objetivo.md) (D-003) y [0003 Partición temporal](../../decisiones/0003-particion-temporal.md) (D-002)?
- Roles de cada integrante (columna *Rol* en [Equipo](../README.md)).
- Carpeta compartida para guardar las grabaciones de Zoom si la nube las borra.
- Quién sube después de cada sesión el resumen, la transcripción y el enlace a la grabación.

### 9. Siguiente sesión

- Fecha, hora y temas.

## Avances por integrante

| Integrante | Avance desde la sesión anterior | Bloqueos |
|---|---|---|
| Filiberto |  |  |
| Diana |  |  |
| Alejandra |  |  |
| Luis |  |  |

## Discusión y decisiones

## Acuerdos

Copiar a [acuerdos.md](../acuerdos.md) con su ID (el siguiente libre es A-008; decisiones, D-010).

| ID | Acuerdo | Responsable | Fecha límite |
|---|---|---|---|
| A-008 |  |  |  |

## Revisión de acuerdos anteriores

| ID | Status nuevo | Comentario |
|---|---|---|
| A-002 |  |  |
| A-003 |  |  |
| A-004 |  |  |
| A-005 |  |  |
| A-006 |  |  |
| A-007 |  |  |

## Revisión de por-clasificar

| Archivo | Decisión (mover a… / eliminar) |
|---|---|
|  |  |

## Próxima sesión

- **Fecha:** 
- **Temas:** 
