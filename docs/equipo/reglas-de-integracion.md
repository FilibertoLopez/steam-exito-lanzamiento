---
titulo: Reglas de integración del código
ubicacion: docs/equipo/reglas-de-integracion.md
actualizado: 2026-11-25
---

# Reglas de integración del código

Objetivo: que cada integrante programe su parte por separado y que todo encaje como rompecabezas en `pipeline.py` el **lunes 30 de noviembre**. Si respetas estas reglas, tu función se integra sin tocar el código de nadie más.

Complementa a [CONTRIBUTING.md](../../CONTRIBUTING.md) (ramas, commits, archivos grandes). Si algo choca, manda este documento para temas de código.

## 1. El rompecabezas en una imagen

```
data/raw/*.parquet ──► cargarSlim() ──► verificarVersion()
        │
        ▼
  PASOS DE LIMPIEZA  (df → df, pueden quitar filas)
  convertirTipos → limpiarFechas → limpiarPrecios → marcarSinDato → quitarNoJuegos
        │
        ▼
  BLOQUES DE VARIABLES  (df → DataFrame indexado por app_id, columnas con prefijo)
  precio_ fecha_ ficha_ gen_ cat_ idi_ dev_ pub_ y_
        │
        ▼  ensamblar() une por app_id
  tabla unificada ──► filtrarMuestra() ──► particionTemporal() ──► data/processed/
```

Todo está en `src/steam_exito/`. El orden y la lista de funciones viven en `pipeline.py` (`PASOS_LIMPIEZA` y `BLOQUES`). **Nadie edita `pipeline.py` salvo Filiberto.**

## 2. Quién es dueño de cada archivo

Una persona por archivo. Si necesitas algo de otro archivo, abre un issue o pide el cambio por PR al dueño.

| Archivo en `src/steam_exito/` | Dueño | Tareas |
|---|---|---|
| `config.py`, `parsers.py`, `contrato.py`, `carga.py`, `graficas.py`, `pipeline.py` | Filiberto | S1-14 (infraestructura ya entregada) |
| `limpieza_basica.py` | Filiberto | S1-01 |
| `variables_precio_fecha.py` | Filiberto | S1-02 |
| `variables_ficha.py` | Filiberto | S1-03 |
| `variables_generos.py` | Luis | S1-04, S1-05 |
| `variables_idiomas.py` | Luis | S1-06 |
| `variables_desarrollador.py` | Diana | S1-07, S1-08 |
| `auditoria.py` | Diana | S1-09 |
| `muestra.py` | Alejandra | S1-10, S1-11, S1-12 |
| `evaluacion.py` | Alejandra | S1-13 |

Las funciones ya tienen firma, docstring con la especificación y un `raise NotImplementedError`. **Tu trabajo es reemplazar ese `raise` por la implementación, sin cambiar el nombre, los parámetros ni los prefijos de columna.** Si crees que la firma debe cambiar, discútelo antes en el issue.

## 3. Los dos tipos de función

### 3.1 Paso de limpieza (`@pasoLimpieza`)

- Recibe un `DataFrame` con la columna `app_id` y devuelve un `DataFrame`.
- Puede **quitar** filas y cambiar tipos o valores. No puede agregar filas ni duplicar `app_id`.
- Debe **conservar la columna `app_id`**.
- Cuántas filas quita queda registrado solo en `contrato.BITACORA` (sirve para la tabla del reporte).

### 3.2 Bloque de variables (`@bloqueVariables`)

- Recibe el `DataFrame` ya limpio y devuelve un `DataFrame` **indexado por `app_id`** (`.set_index("app_id")`), con **una fila por cada juego de la entrada**.
- **Todas** las columnas empiezan con el prefijo del bloque.
- Las columnas son **numéricas o booleanas** (nada de texto; codifica antes).
- Sin infinitos. Los faltantes (`NaN`) son válidos, pero si el valor "sin dato" tiene significado, agrega un indicador `*_sin_dato`.
- No puede incluir columnas con nombre de variable POST (`positive`, `negative`, `peak_ccu`, etc.). El único bloque que puede usar `positive`/`negative` es `y_` (Alejandra).

El decorador verifica todo esto y falla con un mensaje claro. **Si tus pruebas pasan, tu bloque se integra.**

### Prefijos reservados

| Prefijo | Bloque | Dueño |
|---|---|---|
| `precio_` | `variablesPrecio` | Filiberto |
| `fecha_` | `variablesFecha` | Filiberto |
| `ficha_` | `variablesFicha` | Filiberto |
| `gen_` | `variablesGeneros` | Luis |
| `cat_` | `variablesCategorias` | Luis |
| `idi_` | `variablesIdiomas` | Luis |
| `dev_` | `variablesDesarrollador` | Diana |
| `pub_` | `variablesPublisher` | Diana |
| `y_` | `construirObjetivo` | Alejandra |

## 4. Reglas de código

1. **Funciones puras:** no leen ni escriben archivos, no imprimen, no modifican el `DataFrame` de entrada (usa `.copy()`), no dependen de variables globales.
2. **Sin números mágicos:** umbrales, años y listas salen de `config.py`. Si falta un parámetro, agrégalo ahí por PR a Filiberto.
3. **Listas:** léelas siempre con `parsers.aLista` (o `parsers.idiomasYAudio` para idiomas). No uses `split(",")` a mano.
4. **Nombres:** funciones y variables en lowerCamelCase en español (`variablesPrecio`, `mesesMinimos`). Columnas de datos en snake_case con prefijo (`dev_pct_pos_previo`).
5. **Docstring** con qué hace, columnas que devuelve y cualquier regla de negocio. La especificación que ya existe en el esqueleto es tu punto de partida.
6. **Semillas:** si hay aleatoriedad, usa `config.SEMILLA`.
7. **Cada función lleva al menos una prueba** en `tests/test_<modulo>.py` con los datos de juguete de `tests/datos_mini.py` (12 juegos con casos raros: fecha mala, precio atípico, no-juego, formatos mezclados, sin reseñas).
8. **Rendimiento:** debe correr sobre los 151,023 juegos en menos de ~2 minutos. Evita `apply` fila por fila sobre listas largas si hay una alternativa vectorizada (el prototipo de historial del EDA usa `searchsorted`).

## 5. Reglas anti-fuga (data leakage)

Estas reglas son parte de la rúbrica (§3.5 de los lineamientos).

1. **Solo información disponible antes del lanzamiento.** Las columnas POST están en `config.COLUMNAS_POST` y no se usan como predictoras.
2. **Nunca el año de lanzamiento ni la antigüedad como variable.** Se usan para filtrar, agrupar cohortes y particionar.
3. **Historial de desarrollador/publisher (D-006, D-009):** para un juego lanzado en la fecha F solo cuentan juegos lanzados al menos `config.MESES_ANTIGUEDAD_HISTORIAL` meses antes de F (por defecto, 12), y la calidad se promedia solo entre los que tienen al menos `config.UMBRAL_RESENAS` reseñas. **Nunca el valor del propio juego ni de juegos posteriores.**
4. **Variables Pre\*** (`config.VARIABLES_PRE_ASTERISCO`): el valor guardado es el de la tienda hoy, no el del lanzamiento. Entran con reserva; la ablación con/sin Pre\* se hace en el Sprint 2.
5. **Variables relativas a la cohorte** (percentiles por año) se calculan **dentro del propio año de lanzamiento del juego**, sin usar años posteriores.

## 6. Flujo de trabajo (ramas, PR y revisión)

1. `git pull` y crea tu rama: `nombre/s1-XX-tema` (ej. `luis/s1-04-generos`).
2. Implementa solo tus funciones, con sus pruebas.
3. Corre `pytest` y comprueba que **sigue pasando todo**.
4. Corre `python -m steam_exito.pipeline` y revisa que tu bloque ya no aparece en "Pendientes".
5. Abre PR hacia `main` con la plantilla del repo. Enlaza el issue (`Closes #N`) y el acuerdo (A-0XX).
6. Revisión cruzada (un revisor, obligatoria antes de hacer merge):

| Autor | Revisa |
|---|---|
| Filiberto | Alejandra |
| Alejandra | Diana |
| Diana | Luis |
| Luis | Filiberto |

7. El revisor comprueba: pruebas en verde, contrato respetado, sin fuga, sin números mágicos, docstring.
8. Hacer merge no se hace sin aprobación. Después del merge, borra la rama.

**Conflictos:** como cada archivo tiene un solo dueño, no deberían existir. Si aparece uno, avisa en el canal antes de resolverlo.

## 7. Notebooks

- Los notebooks numerados son **delgados**: importan de `src/` y solo orquestan, grafican y comentan. La lógica reutilizable va en `src/`, no en la celda.
- `02_eda.ipynb` (entregado) es el EDA unificado. `03_limpieza.ipynb` y `04_ingenieria_variables.ipynb` los arma Filiberto el día de integración.
- Experimentos: `notebooks/borradores/<nombre>_<tema>.ipynb` (sin salidas, con `nbstripout`).
- Figuras: `reports/figures/<prefijo-del-notebook>_*.png`. Tablas: `reports/metrics/<prefijo>_*.csv`.
- Los notebooks numerados se suben con sus resultados (para que GitHub muestre las gráficas).

## 8. Datos

- Todos usan **la misma versión congelada** (descarga del 24-nov-2026, 151,023 filas). Ver [data/README.md](../../data/README.md).
- `carga.verificarVersion()` falla si tu archivo es otro. Las cifras oficiales salen del parquet congelado (dataset privado de Kaggle, ver `data/README.md`). El CSV público de Kaggle cambia a diario: sirve para probar, no para las cifras finales.
- Los datos no se suben al repo (`data/raw`, `data/interim`, `data/processed` están ignorados).

## 9. Definición de "terminado" del Sprint 1 (lunes 30 de noviembre)

- [ ] Las 13 funciones de las tareas S1-01 a S1-13 implementadas, con pruebas.
- [ ] `pytest` en verde.
- [ ] `python -m steam_exito.pipeline` corre de punta a punta **sin pendientes** y deja `data/processed/steam_modelo.parquet` y `data/processed/particion.parquet`.
- [ ] La muestra final tiene **28,708 juegos** con `UMBRAL_RESENAS = 50` (cifra del EDA; si difiere, hay que investigar antes de seguir).
- [ ] `notebooks/03_limpieza.ipynb` y `04_ingenieria_variables.ipynb` corren y guardan sus figuras/tablas.
- [ ] Secciones del reporte entregadas en borrador (ver [sprint-1-tareas.md](sprint-1-tareas.md)).
- [ ] `acuerdos.md` y `docs/decisiones/` actualizados.

## 10. Qué hacer si algo no encaja

| Problema | Qué hacer |
|---|---|
| Mi función necesita una columna que ningún paso produce | Abre un issue a Filiberto: se agrega al paso de limpieza correspondiente |
| Mi bloque falla el contrato | Lee el mensaje: dice la regla incumplida y la columna |
| Dos bloques quieren la misma columna | Gana el dueño del prefijo; el otro la deriva de la columna ya entregada |
| Quiero cambiar un umbral | Se cambia en `config.py` por PR de Filiberto y se registra una decisión en `docs/decisiones/` |
| No sé si una variable es POST o Pre | Consulta la columna *Momento* de `docs/02-diccionario-datos.md`; en caso de duda, pregunta antes de usarla |
