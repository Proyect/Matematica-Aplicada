"""
Ajuste por minimos cuadrados: modelo lineal y = a0 + a1*x (y extension polinomica).

Requisitos: numpy
"""

from __future__ import annotations

import numpy as np


def minimos_cuadrados_lineal(x: np.ndarray, y: np.ndarray) -> tuple[float, float]:
    """
    Minimiza ||X beta - y||_2 con X = [1, x], beta = [a0, a1]^T.
    Ecuaciones normales: (X^T X) beta = X^T y.
    """
    x = np.asarray(x, dtype=float).ravel()
    y = np.asarray(y, dtype=float).ravel()
    if len(x) != len(y) or len(x) < 2:
        raise ValueError("Se necesitan al menos dos puntos (x,y).")
    X = np.column_stack([np.ones_like(x), x])
    beta, _, _, _ = np.linalg.lstsq(X, y, rcond=None)
    return float(beta[0]), float(beta[1])


def minimos_cuadrados_polinomio(x: np.ndarray, y: np.ndarray, grado: int) -> np.ndarray:
    """
    Coeficientes del polinomio en base monomial {1, x, x^2, ...} de menor grado dado,
    en el mismo orden que numpy.polyfit (grado alto primero si se desea consistencia:
    aqui devolvemos [a0, a1, ..., a_grado] para y ~ sum_k a_k x^k).
    """
    if grado < 0:
        raise ValueError("grado >= 0.")
    x = np.asarray(x, dtype=float).ravel()
    y = np.asarray(y, dtype=float).ravel()
    if len(x) != len(y) or len(x) <= grado:
        raise ValueError("Mas puntos que parametros.")
    cols = [x**k for k in range(grado + 1)]
    X = np.column_stack(cols)
    coef, _, _, _ = np.linalg.lstsq(X, y, rcond=None)
    return coef.astype(float)


def demo() -> None:
    x = np.array([0.0, 1.0, 2.0, 3.0, 4.0])
    y = np.array([1.1, 1.9, 3.2, 3.9, 5.1])
    a0, a1 = minimos_cuadrados_lineal(x, y)
    print("=== Minimos cuadrados lineal y = a0 + a1 x ===")
    print(f"a0 = {a0}, a1 = {a1}")
    c = minimos_cuadrados_polinomio(x, y, 2)
    print("=== Ajuste cuadratico (coef a0..a2 para 1,x,x^2) ===")
    print(c)


if __name__ == "__main__":
    demo()
