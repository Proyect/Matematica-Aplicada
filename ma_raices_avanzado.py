"""
Metodos adicionales para raices: secante y punto fijo x = g(x).

Requisitos: numpy (solo tipado ligero; implementacion en float puro).
"""

from __future__ import annotations

import math
from typing import Callable


def secante(
    f: Callable[[float], float],
    x0: float,
    x1: float,
    tol: float = 1e-12,
    max_iter: int = 100,
) -> tuple[float, int]:
    """
    x_{n+1} = x_n - f(x_n) * (x_n - x_{n-1}) / (f(x_n) - f(x_{n-1})).
    """
    x_prev, x = float(x0), float(x1)
    f_prev, f_cur = f(x_prev), f(x)
    if f_cur == f_prev:
        raise ValueError("f(x0) y f(x1) no pueden ser iguales al inicio.")
    for k in range(max_iter):
        if abs(f_cur) < tol:
            return x, k + 1
        denom = f_cur - f_prev
        if denom == 0:
            raise ValueError("Denominador nulo en secante.")
        x_new = x - f_cur * (x - x_prev) / denom
        x_prev, f_prev = x, f_cur
        x, f_cur = x_new, f(x_new)
    return x, max_iter


def punto_fijo(
    g: Callable[[float], float],
    x0: float,
    tol: float = 1e-10,
    max_iter: int = 200,
) -> tuple[float, int]:
    """
    x_{k+1} = g(x_k) hasta |x_{k+1} - x_k| < tol.
    Converge si |g'(alpha)| < 1 en la raiz (condicion local).
    """
    x = float(x0)
    for k in range(max_iter):
        x_new = g(x)
        if abs(x_new - x) < tol:
            return x_new, k + 1
        x = x_new
    return x, max_iter


def demo() -> None:
    f = lambda x: x**3 - x - 2
    r, it = secante(f, 1.0, 2.0)
    print("=== Secante: raiz x^3 - x - 2, x0=1, x1=2 ===")
    print(f"raiz ~ {r}, iteraciones = {it}, f(r) = {f(r)}")

    # Raiz de x - cos(x)=0  <=>  x = cos(x)
    g = lambda x: math.cos(x)
    r2, it2 = punto_fijo(g, 0.5)
    print("=== Punto fijo x = cos(x), x0=0.5 ===")
    print(f"punto fijo ~ {r2}, iteraciones = {it2}, x-cos(x) = {r2 - g(r2)}")


if __name__ == "__main__":
    demo()
