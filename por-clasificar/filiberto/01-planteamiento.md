---
titulo: Planteamiento del problema
estado: borrador
notebook: 
actualizado: 2026-11-24
---

# Planteamiento del problema

## Contexto

Cada año se publican más juegos en Steam. En el conjunto de datos del proyecto (Steam Games Dataset de Kaggle, versión del 2026-11-19, 150,199 registros y 42 columnas) la generación de juegos del año 2015 tiene 2,513 juegos y la de 2024 tiene 19,898 ([percentiles por cohorte](../reports/metrics/percentilesCohorte_resumen.csv)). Con más oferta, la atención de los jugadores se reparte entre más títulos y la mayoría de los lanzamientos recibe muy pocas reseñas.

Quien financia o desarrolla un juego tiene que decidir **antes del lanzamiento**: cuánto cobrar, qué géneros y funciones incluir, a cuántos idiomas traducir y en qué plataformas publicar. En ese momento no existe ninguna de las señales que después se usan para juzgar el resultado (reseñas, propietarios estimados, jugadores simultáneos, Metacritic). El valor del proyecto está en identificar qué información disponible en ese momento se asocia con una mejor recepción, para orientar decisiones de inversión y de diseño.

### Dificultades del problema

- **Sesgo de antigüedad.** El número de reseñas crece con el tiempo en tienda: 98.6 % de los juegos con menos de un año tiene 0 reseñas, y la mediana sube a 352 en los juegos con 12 años ([antigüedad vs. reseñas](../reports/metrics/antiguedadVsResenas_resumen.csv)). Comparar juegos de distintos años sin ajuste mezcla éxito con exposición.
- **La recepción también cambia por año de publicación.** La mediana de la proporción de reseñas positivas pasa de 0.75 en 2018 a 0.875 en 2024 ([percentiles por cohorte](../reports/metrics/percentilesCohorte_resumen.csv)), por lo que conviene comparar cada juego con los de su mismo año.
- **Fuga de información.** Varias columnas se generan después del lanzamiento (reseñas, propietarios, tiempo de juego, `peak_ccu`, `tags` de usuarios, Steam Trading Cards) y no pueden usarse como predictores.
- **Datos que no son estáticos.** Precio, idiomas, categorías y otros atributos reflejan el estado de la tienda en la fecha de descarga, no necesariamente el del lanzamiento.
- **Alta cardinalidad.** Hay 94,963 desarrolladores y unos 80,000 distribuidores; la mayoría tiene pocos lanzamientos, así que el nombre no sirve como variable directa.

## Pregunta de investigación

**Pregunta principal:** ¿qué factores, disponibles antes del lanzamiento, se asocian con una mayor probabilidad de que un juego nuevo en Steam tenga buena recepción, comparado con los juegos lanzados en su mismo periodo?

**Preguntas secundarias:**

1. ¿Qué tanto mejora un modelo con factores previos al lanzamiento frente a una referencia que solo usa la tasa base de su cohorte?
2. ¿Qué peso tienen las decisiones de producto (precio, géneros, categorías, idiomas, plataformas) frente al historial del desarrollador?
3. ¿Los factores asociados con la recepción son los mismos que se asocian con la tracción (volumen de reseñas)?

## Definición de éxito

El éxito se mide con la **proporción de reseñas positivas**, acordada como variable objetivo en la [sesión del 2026-11-22](equipo/sesiones/resumenes-zoom/2026-11-22-Exploración-de-datos.md):

$$
p_i = \frac{\text{positive}_i}{\text{positive}_i + \text{negative}_i}
$$

Se prefirió a precio y propietarios estimados porque estos son poco confiables como medida de resultado (`estimated_owners` viene en rangos amplios).

Para que la medida sea comparable entre juegos:

- **Mínimo de reseñas.** Solo se evalúan juegos con un número mínimo de reseñas; el valor (30, 50 o 100) está pendiente en la decisión [0002 Mínimo de reseñas](decisiones/0002-minimo-de-resenas.md).
- **Comparación por cohorte.** La proporción se expresa como percentil dentro del año de lanzamiento, para absorber el cambio de la recepción entre cohortes.
- **Variantes en evaluación.** Límite inferior de Wilson (para no premiar juegos con 3 de 3 positivas) y una etiqueta binaria de "buena recepción" (por ejemplo, estar en el cuartil superior de su cohorte), más fácil de explicar a inversionistas. La elección final queda en la decisión [0001 Variable objetivo](decisiones/0001-variable-objetivo.md).

El volumen de reseñas (`positive + negative`) no es la variable objetivo, pero se conserva como medida de tracción para comparar resultados, porque gustar y vender son cosas distintas.

## Alcance y restricciones

### Alcance

- **Unidad de análisis:** un juego publicado en Steam. Se excluye el software que no es juego (por ejemplo, Animation & Modeling o Design & Illustration).
- **Periodo:** juegos lanzados hasta 2024. Los de 2025 y 2026 se excluyen porque aún no acumulan reseñas suficientes; está en evaluación excluir también los anteriores a 2014, cuyas cohortes son pequeñas y atípicas.
- **Predictores:** solo atributos conocidos antes del lanzamiento: precio, géneros, etiquetas de marketing (Indie, Early Access, Free to Play) tratadas aparte de los géneros, categorías de Steam, idiomas, plataformas, fecha de lanzamiento e historial del desarrollador calculado solo con sus juegos anteriores.
- **Evaluación:** partición temporal (entrenar con cohortes antiguas y probar con las más recientes) para simular la predicción de lanzamientos futuros; los detalles están en la decisión [0003 Partición temporal](decisiones/0003-particion-temporal.md).

### Restricciones

- **Asociación, no causalidad.** Los datos son observacionales; los resultados indican qué factores acompañan a la buena recepción, no qué la provoca.
- **Variables ausentes.** El conjunto no incluye seguidores, wishlists, presupuesto de marketing ni búsquedas previas, que la literatura señala como predictores importantes.
- **Estado actual vs. lanzamiento.** Los atributos se observan en la fecha de descarga (2026-11-19). Que un dato esté en la ficha hoy no prueba que estuviera disponible el día del lanzamiento.
- **Calidad de datos.** Hay valores atípicos (un precio de USD 107,000 que se elimina), ceros que pueden significar "sin dato" y deben auditarse, y un cambio de formato de la columna de categorías alrededor de 2019.
- **Sesgo de selección.** El mínimo de reseñas deja fuera los juegos que casi nadie compró, por lo que el modelo describe la recepción entre juegos que sí lograron cierta tracción.

## Hipótesis

Hipótesis nula general: una vez controlada la cohorte de lanzamiento, los factores previos al lanzamiento no mejoran la predicción de la recepción frente a la tasa base de la cohorte.

Hipótesis de trabajo (cada una se contrasta con el modelo y con análisis exploratorio):

| ID | Hipótesis | Variables | Cómo se evalúa |
|---|---|---|---|
| H1 | El historial del desarrollador es el factor con mayor asociación: quienes ya tuvieron juegos bien recibidos tienden a repetir. | Número de juegos previos, recepción media previa | Importancia en el modelo; partición agrupada por desarrollador para descartar memorización |
| H2 | La recepción varía por género, y las etiquetas de marketing (Indie, Early Access, Free to Play) tienen un efecto distinto al del género. | Géneros, etiquetas de marketing | Comparación por grupo dentro de cada cohorte; efectos parciales |
| H3 | El precio tiene una relación no lineal con la recepción: los juegos gratuitos y los de precio muy bajo o muy alto se reciben distinto que los de precio medio. | `price`, indicador de gratuito | Curvas de dependencia parcial o de un modelo aditivo |
| H4 | Traducir a más idiomas se asocia con mejor recepción, con rendimientos decrecientes. | Número de idiomas de interfaz y de audio | Diagrama de dispersión por cohorte y efecto parcial |
| H5 | Las funciones de la plataforma (logros, Steam Cloud, soporte de control) se asocian con mejor recepción como señal de cuidado en el producto. | Categorías de Steam | Importancia y efecto parcial de cada categoría |
| H6 | La plataforma (Windows, Mac, Linux) aporta poco, porque casi todos los juegos salen en Windows. | Indicadores de plataforma | Importancia por permutación cercana a cero |

Las hipótesis se revisarán cuando se cierren las decisiones sobre la variable objetivo, el mínimo de reseñas y la partición temporal.
