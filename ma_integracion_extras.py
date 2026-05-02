"""
Reglas de cuadratura adicionales: punto medio compuesto y Simpson 3/8 compuesto.

Requisitos: numpy
"""

from __future__ import annotations

from typing import Callable

import numpy as np


def regla_punto_medio(f: Callable[[float], float], a: float, b: float, n: int) -> float:
    """
    Formula del rectangulo / punto medio compuesto:
    integral ~ h * sum_{i=0}^{n-1} f(m_i), m_i = a + (i+0.5)h, h=(b-a)/n.
    """
    if n < 1:
        raise ValueError("n >= 1.")
    h = (b - a) / n
    total = 0.0
    for i in range(n):
        mi = a + (i + 0.5) * h
        total += f(mi)
    return float(h * total)


def regla_simpson_38(f: Callable[[float], float], a: float, b: float, n_mult_3: int) -> float:
    """
    Simpson 3/8 compuesto: numero de subintervalos n debe ser multiplo de 3.
    En cada bloque de 3 subintervalos de longitud h: (3h/8)(f0 + 3f1 + 3f2 + f3).
    """
    if n_mult_3 < 3 or n_mult_3 % 3 != 0:
        raise ValueError("n debe ser multiplo de 3 y >= 3.")
    h = (b - a) / n_mult_3
    xs = np.linspace(a, b, n_mult_3 + 1)
    ys = np.array([f(float(x)) for x in xs])
    blocks = n_mult_3 // 3
    acc = 0.0
    for k in range(blocks):
        i0 = 3 * k
        acc += (ys[i0] + 3 * ys[i0 + 1] + 3 * ys[i0 + 2] + ys[i0 + 3])
    return float((3 * h / 8) * acc)


def demo() -> None:
    import math

    g = lambda x: math.exp(-x)
    a, b = 0.0, 1.0
    exacto = 1 - math.exp(-1)
    pm = regla_punto_medio(g, a, b, 30)
    s38 = regla_simpson_38(g, a, b, 30)
    print("=== Integral e^(-x) de 0 a 1 ===")
    print(f"Punto medio n=30: {pm}, error = {abs(pm - exacto)}")
    print(f"Simpson 3/8 n=30: {s38}, error = {abs(s38 - exacto)}")
    print(f"Exacto: {exacto}")


if __name__ == "__main__":
    demo()
