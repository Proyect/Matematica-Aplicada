"""
Interpolacion polinomica (Lagrange) e interpolacion lineal a trozos.

Requisitos: numpy
"""

from __future__ import annotations

import numpy as np


def interpolacion_lineal(x: np.ndarray, y: np.ndarray, xq: float) -> float:
    """
    Entre dos puntos consecutivos (x_i, x_{i+1}) que encierran xq:
    p(xq) = y_i + (y_{i+1}-y_i)/(x_{i+1}-x_i) * (xq - x_i).
    """
    x = np.asarray(x, dtype=float).ravel()
    y = np.asarray(y, dtype=float).ravel()
    if len(x) != len(y) or len(x) < 2:
        raise ValueError("x e y deben tener la misma longitud >= 2.")
    if not np.all(np.diff(x) > 0):
        raise ValueError("x debe ser estrictamente creciente.")
    idx = np.searchsorted(x, xq) - 1
    idx = int(np.clip(idx, 0, len(x) - 2))
    x0, x1 = x[idx], x[idx + 1]
    y0, y1 = y[idx], y[idx + 1]
    return float(y0 + (y1 - y0) * (xq - x0) / (x1 - x0))


def lagrange_eval(x_nodes: np.ndarray, y_nodes: np.ndarray, xq: float) -> float:
    """
    Polinomio de Lagrange P(xq) = sum_j y_j * L_j(xq),
    L_j(x) = prod_{m!=j} (x - x_m) / (x_j - x_m).
    """
    xn = np.asarray(x_nodes, dtype=float).ravel()
    yn = np.asarray(y_nodes, dtype=float).ravel()
    if len(xn) != len(yn) or len(xn) < 1:
        raise ValueError("Nodos invalidos.")
    n = len(xn)
    total = 0.0
    for j in range(n):
        lj = 1.0
        for m in range(n):
            if m == j:
                continue
            lj *= (xq - xn[m]) / (xn[j] - xn[m])
        total += yn[j] * lj
    return float(total)


def demo() -> None:
    x = np.array([0.0, 1.0, 2.0, 3.0])
    y = np.array([1.0, 2.0, 1.5, 2.5])
    print("=== Interpolacion lineal en x=1.25 ===")
    print(interpolacion_lineal(x, y, 1.25))
    print("=== Lagrange en x=1.5 (mismos nodos) ===")
    print(lagrange_eval(x, y, 1.5))


if __name__ == "__main__":
    demo()
