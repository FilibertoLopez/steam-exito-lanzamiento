"""Datos de juguete (12 juegos) con las mismas columnas y casos raros del parquet real."""
import pandas as pd

COLUMNAS = [
    "app_id", "name", "release_date", "price", "price_status", "estimated_owners", "developers",
    "publishers", "genres", "categories", "positive", "negative", "recommendations", "peak_ccu",
    "metacritic_score", "user_score", "average_playtime_forever", "median_playtime_forever",
    "average_playtime_2weeks", "median_playtime_2weeks", "achievements", "dlc_count",
    "supported_languages", "full_audio_languages", "windows", "mac", "linux",
    "steam_store_available", "steam_spy_available", "has_website", "has_support_url",
    "has_support_email", "has_notes",
]


def _fila(app_id, name, fecha, **kw):
    base = dict(
        app_id=app_id, name=name, release_date=fecha, price=9.99, price_status="paid",
        estimated_owners="0 - 20000", developers='["Estudio A"]', publishers='["Estudio A"]',
        genres='["Action", "Indie"]', categories='["Single-player", "Steam Achievements"]',
        positive=80, negative=20, recommendations=0.0, peak_ccu=0, metacritic_score=0.0,
        user_score=0, average_playtime_forever=0, median_playtime_forever=0,
        average_playtime_2weeks=0, median_playtime_2weeks=0, achievements=10.0, dlc_count=0,
        supported_languages='["English", "Spanish - Spain"]', full_audio_languages="[]",
        windows="True", mac="False", linux="False", steam_store_available=True,
        steam_spy_available=True, has_website=True, has_support_url=False,
        has_support_email=True, has_notes=False,
    )
    base.update(kw)
    return base


def crearDfMini() -> pd.DataFrame:
    """12 juegos: mismo desarrollador en varios años, formatos mezclados, fecha inválida, precio
    atípico, sin reseñas, sin dato de género, no-juego y mac vacío."""
    filas = [
        _fila(1, "A1", "2018-03-01"),
        _fila(2, "A2", "2019-06-15", positive=90, negative=10),
        _fila(3, "A3", "2021-01-20", positive=30, negative=70),
        _fila(4, "B1", "2020-05-05", developers='["Estudio B"]', publishers='["Pub X"]',
              genres='[{"id": "1", "description": "Action"}, {"id": "23", "description": "Indie"}]',
              categories='[{"id": 2, "description": "Single-player"}]'),
        _fila(5, "B2", "2022-09-09", developers='["Estudio B", "Estudio A"]', publishers='["Pub X"]',
              positive=500, negative=100, price=0.0, price_status="free"),
        _fila(6, "C1", "2023-02-02", developers='["Estudio C"]', positive=0, negative=0),
        _fila(7, "D1", "fecha-mala", developers='["Estudio D"]'),
        _fila(8, "E1", "2024-07-07", price=107500.0, developers='["Estudio E"]'),
        _fila(9, "F1", "2024-11-11", developers="[]", publishers="[]", genres="[]", positive=60, negative=40),
        _fila(10, "Herramienta", "2021-10-10", genres='["Utilities"]', developers='["Estudio G"]'),
        _fila(11, "G2", "2025-03-03", mac=None, linux="True", positive=5, negative=1),
        _fila(12, "A4", "2024-02-02", price=None, price_status="unavailable",
              supported_languages=None, full_audio_languages='["English"]', positive=45, negative=5),
    ]
    return pd.DataFrame(filas, columns=COLUMNAS)
