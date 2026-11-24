# Cómo colaborar

Equipo: Diana, Alejandra, Luis y Filiberto. Ver [docs/equipo](docs/equipo/README.md).

## Ramas

- `main` siempre debe funcionar. No se trabaja directamente en `main` salvo notas de sesión y actualización de acuerdos.
- Una rama por tarea: `nombre/tema-corto` (p. ej. `diana/eda-generos`, `luis/modelo-xgboost`).
- Al terminar, abrir un **pull request** hacia `main` y pedir revisión a otro integrante.

## Commits

- Mensajes en español, en imperativo y concretos: `Agregar análisis de etiquetas en 02_eda`.
- Commits pequeños y frecuentes. Antes de empezar: `git pull`.

## Notebooks

- Los notebooks numerados (`notebooks/0X_*.ipynb`) tienen un responsable a la vez para evitar conflictos; anótalo en el issue.
- Para experimentar, crea una copia en `notebooks/borradores/` con tu nombre: `borradores/alejandra_prueba_lgbm.ipynb`.
- Variables en lowerCamelCase.

## Archivos grandes

- Datos (`data/raw`, `data/interim`, `data/processed`) y modelos (`models/`) no se suben.
- PDF, PPTX, DOCX y XLSX se suben con Git LFS (configurado en `.gitattributes`). Cada integrante debe ejecutar `git lfs install` una vez.
- Las grabaciones de Zoom no se suben: se enlazan en el [registro de sesiones](docs/equipo/sesiones/README.md).

## Material sin lugar definido

- Súbelo a tu carpeta en [`por-clasificar/`](por-clasificar/README.md) y regístralo en su tabla.
- En cada sesión se revisa la carpeta y cada archivo se mueve a su destino o se elimina.

## Seguimiento

- **Acuerdos:** [docs/equipo/acuerdos.md](docs/equipo/acuerdos.md) es la lista oficial.
- **Tareas técnicas:** issues con la plantilla *Tarea* y la etiqueta `resp: <nombre>`.
