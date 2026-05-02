"""
Diagrama de dispersion y recta de regresion (Unidad 3).

Requisitos: numpy, matplotlib
"""

from __future__ import annotations

import numpy as np

from ma_minimos_cuadrados import ResultadoRegresionLineal


def figura_dispersion_recta(
    x: np.ndarray,
    y: np.ndarray,
    resultado: ResultadoRegresionLineal,
    titulo: str = "Diagrama de dispersion y regresion lineal",
):
    """Construye la figura (no la muestra); usar con GUI o plt.show(). Devuelve Figure."""
    import matplotlib.pyplot as plt

    x = np.asarray(x, dtype=float).ravel()
    y = np.asarray(y, dtype=float).ravel()
    fig, ax = plt.subplots(figsize=(6.5, 4.5))
    ax.scatter(x, y, color="tab:blue", edgecolors="k", linewidths=0.4, label="Observaciones", zorder=3)
    xs = np.linspace(float(np.min(x)), float(np.max(x)), 200)
    ys = resultado.alpha + resultado.beta * xs
    ax.plot(xs, ys, color="tab:red", linewidth=2, label=r"$\hat{y} = \hat{\alpha} + \hat{\beta} x$", zorder=2)
    ax.axhline(resultado.y_media, color="gray", linestyle="--", linewidth=1, alpha=0.7, label=r"$\bar{y}$")
    ax.set_xlabel("X (independiente)")
    ax.set_ylabel("Y (dependiente)")
    ax.set_title(titulo)
    ax.legend(loc="best")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    return fig


def guardar_dispersion_recta(
    x: np.ndarray,
    y: np.ndarray,
    resultado: ResultadoRegresionLineal,
    ruta: str,
    titulo: str = "Diagrama de dispersion y regresion lineal",
) -> None:
    fig = figura_dispersion_recta(x, y, resultado, titulo=titulo)
    fig.savefig(ruta, dpi=150)
    import matplotlib.pyplot as plt

    plt.close(fig)
