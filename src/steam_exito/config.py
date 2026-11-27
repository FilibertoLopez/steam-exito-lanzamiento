"""Parámetros únicos del proyecto. Todo valor que sea una decisión del equipo vive aquí.

Regla: ninguna función hardcodea umbrales, años ni listas de columnas; los lee de este módulo.
Cambiar una decisión (p. ej. el umbral de reseñas) = cambiar una línea aquí.
"""
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT_DIR / "data"
REPORTS_DIR = ROOT_DIR / "reports"

SEMILLA = 42

# Versión congelada de los datos (acuerdo A-005)
VERSION_DATOS = {
    "fuente": "Kaggle: hubertsidorowicz/steam-games-dataset-daily-updates (steam_games.csv)",
    "fecha_descarga": "2026-11-24",
    "fecha_max_lanzamiento": "2026-11-24",
    "filas": 151023,
    "columnas": 33,
    "sha256_parquet_original": "eb64467236ae174808e76ff94e8f9304bcc0ad7faec756c2bc9099cb49431992",
    "huella_app_id": "337e875fa555995e2668a38019fe3c5bb4567418c2e92dd09c166d0a9c9d0cd3",   # no depende de cómo se partió el archivo
}

# Decisiones de muestra y objetivo (ver docs/decisiones/ y docs/equipo/acuerdos.md)
UMBRAL_RESENAS = 50                    # D-008 / decisión 0002 (propuesta de trabajo)
UMBRALES_SENSIBILIDAD = (30, 50, 100)  # A-003
ANIO_MAX = 2024                        # D-002: se excluyen 2025 y 2026
ANIO_MIN = None                        # None = todo el historial; abierto (decisión 0003)
ANIO_MIN_SENSIBILIDAD = 2019
MESES_ANTIGUEDAD_HISTORIAL = 12        # solo juegos previos con >= N meses cuentan en el historial
OBJETIVO_PRINCIPAL = "y_pct_pos"       # D-003
PESOS_DE_MUESTRA = None                # D-008: sin pesos por ahora
PRECIO_MAX_VALIDO = 100_000            # D-004: los registros de 107,500 USD se eliminan
CORTES_PRECIO = [0, 5, 10, 20, 40]     # S1-02: límites superiores (USD) de precio_rango 0..4; >40 es el rango 5 (EDA §5.1)

FRACCION_TRAIN = 0.70                  # partición temporal por cuantiles de fecha
FRACCION_VALID = 0.15

# Disponibilidad temporal de las columnas (docs/02-diccionario-datos.md)
COLUMNAS_POST = [
    "positive", "negative", "estimated_owners", "recommendations", "peak_ccu",
    "metacritic_score", "user_score", "average_playtime_forever",
    "median_playtime_forever", "average_playtime_2weeks", "median_playtime_2weeks",
    "tags", "metacritic_url",
]
# Pre*: se conoce antes, pero el valor guardado es el actual de la tienda (D-010)
VARIABLES_PRE_ASTERISCO = [
    "price", "dlc_count", "packages", "screenshots", "movies", "tags",
    "supported_languages", "full_audio_languages", "categories",
]
COLUMNAS_DESCARTAR = [
    "dlc_count", "steam_spy_available", "windows", "tags", "packages",
    "header_image", "detailed_description", "metacritic_url",
]
COLUMNAS_CERO_ES_NULO = [
    "recommendations", "peak_ccu", "metacritic_score", "user_score",
    "average_playtime_forever", "median_playtime_forever",
    "average_playtime_2weeks", "median_playtime_2weeks",
]
# Columnas de lista donde "[]" = sin dato (en full_audio_languages [] es un valor real)
COLUMNAS_LISTA = ["developers", "publishers", "genres", "categories", "supported_languages"]

# Géneros (D-005)
GENEROS_JUEGO = ["Action", "Adventure", "Casual", "Simulation", "Strategy", "RPG", "Sports", "Racing", "Massively Multiplayer"]
ETIQUETAS_MARKETING = ["Indie", "Early Access", "Free To Play"]
AVISO_CONTENIDO = ["Violent", "Gore", "Nudity", "Sexual Content"]
GENEROS_NO_JUEGO = [
    "Utilities", "Design & Illustration", "Animation & Modeling", "Education",
    "Video Production", "Game Development", "Audio Production", "Software Training",
    "Photo Editing", "Web Publishing", "Accounting", "Movie", "Documentary",
    "Episodic", "Short", "Tutorial", "360 Video",
]
GENEROS_NO_JUEGO_SOLO_SI_UNICOS = ["Education", "Episodic", "Short"]
MAPA_GENEROS_TRADUCIDOS = {
    "Aventure": "Adventure", "Occasionnel": "Casual", "インディー": "Indie",
    "早期アクセス": "Early Access", "Strategie": "Strategy", "Gratuit": "Free To Play",
    "Indépendant": "Indie", "Stratégie": "Strategy", "Aventura": "Adventure",
    "Simuladores": "Simulation",
}
CATEGORIAS_EXCLUIR = ["Steam Trading Cards"]   # Steam la activa según las ventas

# Convenciones del pipeline
COLUMNAS_BASE = ["app_id", "name", "release_date"]
PREFIJOS = {
    "precio": "precio_", "fecha": "fecha_", "ficha": "ficha_",
    "generos": "gen_", "categorias": "cat_", "idiomas": "idi_",
    "desarrollador": "dev_", "publisher": "pub_", "objetivo": "y_",
}
