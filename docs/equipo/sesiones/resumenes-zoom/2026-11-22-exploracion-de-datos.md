## Resultados clave

El equipo acordó avanzar con un **repositorio compartido en GitHub** para centralizar código y documentación, ya que es un requisito del profesor. Se identificaron problemas de calidad en los datos (valores atípicos, formatos inconsistentes, datos faltantes) y se propuso un **corte temporal de datos hasta 2024** para evitar juegos demasiado recientes sin historial suficiente de reseñas. Se planteó una estrategia de limpieza basada en tres reglas: **umbral mínimo de reseñas**, **filtro de antigüedad** y posible **ponderación por volumen de reseñas** para reducir ruido en la variable objetivo.

## Decisiones tomadas

- **Repositorio:** Usar un repositorio compartido en **GitHub** vinculado a los correos del ITAM.
- **Corte temporal:** Excluir juegos de **2025 y 2026** para asegurar que los datos de éxito estén lo suficientemente maduros.
- **Variable objetivo:** Utilizar la proporción de **reseñas positivas** como métrica de éxito, en lugar de precio o estimaciones de dueños, que son poco confiables.
- **Limpieza de precios:** Eliminar el registro con un precio atípico de **107,000 dólares**.
- **Tratamiento de géneros/categorías:** Separar etiquetas de marketing (ej. **Indie**, **Early Access**, **Free to Play**) de los géneros de juego, ya que son dimensiones ortogonales.
- **Variables de desarrollador:** No usar el nombre del desarrollador directamente por su alta cardinalidad; en su lugar, derivar variables como **número de juegos previos** y **promedio de éxito histórico**.

## Hallazgos de datos

- **Volumen:** El dataset tiene más de **150,000 juegos** y 42 columnas.
- **Precios:** Aproximadamente el **95%** de los juegos tienen precio; el resto son gratuitos o ya no están disponibles en la tienda.
- **Reseñas:** Hay unos **62,000 registros** sin reseñas positivas ni negativas, principalmente juegos muy recientes.
- **Géneros:** El género **Indie** es el más frecuente; existen categorías no relacionadas con juegos (ej. **Animation**, **Design**) que deben eliminarse.
- **Idiomas:** Hay hasta **103 idiomas** registrados, incluyendo casos atípicos como el **tigriña**.
- **Desarrolladores:** Existe una alta concentración en algunos estudios (ej. **Erotic Games Club** con 237 juegos), pero la mayoría son desarrolladores independientes con pocos lanzamientos.

## Riesgos y bloqueos

- **Sesgo de antigüedad:** Los juegos más viejos tienden a acumular más reseñas por el simple paso del tiempo, no necesariamente por ser mejores.
- **Datos no estáticos:** El precio y otras métricas varían diariamente; se necesita definir una **fecha de corte fija** para la descarga de datos.
- **Formato inconsistente:** La columna de categorías cambió de formato de **texto a diccionario** alrededor de 2019, lo que requiere unificación.
- **Alta cardinalidad:** Hay **94,963 desarrolladores** y **80,000 publishers**, lo que impide usarlos directamente como variables categóricas en el modelo.

## Preguntas abiertas

- **Umbral de reseñas:** Definir si el mínimo será **30, 50 o 100 reseñas** para considerar un juego como válido para el entrenamiento.
- **Ponderación:** Determinar si se debe ponderar la importancia de los juegos con más reseñas o si eso sesgaría el modelo hacia los éxitos ya conocidos.
- **Idiomas:** Confirmar si la cantidad o tipo de idiomas realmente correlaciona con el éxito mediante un análisis de dispersión (scatter plot) antes de incluir la variable.
- **Plataformas:** Evaluar si la plataforma (Windows, Mac, Linux) es un diferenciador relevante o si puede ignorarse dado que la mayoría son para Windows.

## Elementos de acción

- **Filiberto:** Enviar invitación al repositorio de GitHub a los correos del ITAM.
- **Equipo:** Compartir los análisis individuales (EDAs) y propuestas de variables para la próxima sesión.
- **Equipo:** Probar diferentes umbrales de reseñas y filtros de antigüedad para ver el impacto en el tamaño del dataset y la calidad del modelo.
- **Equipo:** Crear variables derivadas para desarrolladores (ej. **curva de aprendizaje**, promedio de éxito histórico) en lugar de usar nombres individuales.
