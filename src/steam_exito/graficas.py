"""Utilidades de graficación. Todas las figuras salen a reports/figures/<prefijo>_*.png."""
from pathlib import Path

import matplotlib.pyplot as plt
import seaborn as sns

FIGURES_DIR = Path(__file__).resolve().parents[2] / "reports" / "figures"
METRICS_DIR = Path(__file__).resolve().parents[2] / "reports" / "metrics"
COLOR = "#2f6f8f"
COLOR_2 = "#e08a2e"


def estiloBase() -> None:
    """Estilo común para todas las figuras del proyecto."""
    sns.set_theme(style="whitegrid", context="notebook")
    plt.rcParams.update({"figure.dpi": 100, "savefig.dpi": 150, "axes.titlesize": 11, "axes.labelsize": 10})


def guardarFigura(fig: plt.Figure, nombre: str, dpi: int = 150) -> Path:
    """Guarda la figura en reports/figures como PNG. Usa el prefijo del notebook: 02_eda_xxx."""
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    ruta = FIGURES_DIR / f"{nombre}.png"
    fig.savefig(ruta, dpi=dpi, bbox_inches="tight")
    return ruta


def guardarMetrica(df, nombre: str) -> Path:
    """Guarda una tabla en reports/metrics como CSV (UTF-8)."""
    METRICS_DIR.mkdir(parents=True, exist_ok=True)
    ruta = METRICS_DIR / f"{nombre}.csv"
    df.to_csv(ruta, encoding="utf-8")
    return ruta
