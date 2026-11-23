"""Utilidades de graficación."""
from pathlib import Path

import matplotlib.pyplot as plt

FIGURES_DIR = Path(__file__).resolve().parents[2] / "reports" / "figures"


def guardarFigura(fig: plt.Figure, nombre: str, dpi: int = 150) -> Path:
    """Guarda la figura en reports/figures como PNG."""
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    ruta = FIGURES_DIR / f"{nombre}.png"
    fig.savefig(ruta, dpi=dpi, bbox_inches="tight")
    return ruta
