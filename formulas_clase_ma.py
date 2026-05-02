"""
Herramientas numéricas alineadas con clases típicas de Matemática Aplicada.

Referencia de la clase: https://www.youtube.com/watch?v=_SgUUsTz390
(Título oEmbed: «Clase MA - 27/04/26» — MATEMÁTICA APLICADA LCD)

Si en el vídeo usan otras fórmulas, añade funciones aquí o pásame el enunciado
y las integro en el mismo estilo.

Requisitos: pip install numpy
"""

from __future__ import annotations

import math
from typing import Callable, Sequence

import numpy as np


# --- Errores ---


def error_absoluto(valor_aprox: float, valor_real: float) -> float:
    """E_abs = |x* - x̃|"""
    return abs(valor_real - valor_aprox)


def error_relativo(valor_aprox: float, valor_real: float) -> float:
    """E_rel = E_abs / |x*|  (si x* ≠ 0)"""
    if valor_real == 0:
        raise ValueError("El valor real no puede ser 0 para el error relativo clásico.")
    return error_absoluto(valor_aprox, valor_real) / abs(valor_real)


# --- Raíces: bisección ---


def biseccion(
    f: Callable[[float], float],
    a: float,
    b: float,
    tol: float = 1e-10,
    max_iter: int = 200,
) -> tuple[float, int]:
    """
    Teorema: si f ∈ C([a,b]) y f(a)f(b) < 0, existe c ∈ (a,b) con f(c)=0.
    Partimos [a,b] por la mitad repetidamente.
    """
    fa, fb = f(a), f(b)
    if fa * fb > 0:
        raise ValueError("f(a) y f(b) deben tener signo distinto.")

    it = 0
    while (b - a) / 2 > tol and it < max_iter:
        m = (a + b) / 2
        fm = f(m)
        if fa * fm <= 0:
            b, fb = m, fm
        else:
            a, fa = m, fm
        it += 1
    return (a + b) / 2, it


# --- Raíces: Newton-Raphson ---


def newton_raphson(
    f: Callable[[float], float],
    df: Callable[[float], float],
    x0: float,
    tol: float = 1e-12,
    max_iter: int = 100,
) -> tuple[float, int]:
    """
    x_{k+1} = x_k - f(x_k) / f'(x_k)
    """
    x = float(x0)
    for k in range(max_iter):
        fx = f(x)
        if abs(fx) < tol:
            return x, k + 1
        dfx = df(x)
        if dfx == 0:
            raise ValueError("Derivada nula; el método no puede continuar.")
        x -= fx / dfx
    return x, max_iter


# --- Integración numérica ---


def regla_trapecio(f: Callable[[float], float], a: float, b: float, n: int) -> float:
    """
    ∫_a^b f(x) dx ≈ h/2 (f(x_0) + 2∑_{i=1}^{n-1} f(x_i) + f(x_n)),
    h = (b-a)/n, x_i = a + i h.
    """
    if n < 1:
        raise ValueError("n debe ser ≥ 1.")
    h = (b - a) / n
    xs = np.linspace(a, b, n + 1)
    ys = np.array([f(float(x)) for x in xs])
    return float(h * (0.5 * ys[0] + ys[1:-1].sum() + 0.5 * ys[-1]))


def regla_simpson_13(f: Callable[[float], float], a: float, b: float, n_par: int) -> float:
    """
    Regla de Simpson 1/3 compuesta (n subintervalos, n par).
    ∫_a^b f(x) dx ≈ h/3 [f_0 + 4∑ f_{impares} + 2∑ f_{pares internos} + f_n].
    """
    if n_par < 2 or n_par % 2 != 0:
        raise ValueError("n debe ser par y ≥ 2.")
    h = (b - a) / n_par
    xs = np.linspace(a, b, n_par + 1)
    ys = np.array([f(float(x)) for x in xs])
    impares = ys[1:-1:2].sum()
    pares_internos = ys[2:-1:2].sum()
    return float(h / 3 * (ys[0] + 4 * impares + 2 * pares_internos + ys[-1]))


# --- Diferencias finitas (aproximación de derivadas) ---


def derivada_progresiva(f: Callable[[float], float], x: float, h: float) -> float:
    """f'(x) ≈ (f(x+h) - f(x)) / h"""
    return (f(x + h) - f(x)) / h


def derivada_regresiva(f: Callable[[float], float], x: float, h: float) -> float:
    """f'(x) ≈ (f(x) - f(x-h)) / h"""
    return (f(x) - f(x - h)) / h


def derivada_centrada(f: Callable[[float], float], x: float, h: float) -> float:
    """f'(x) ≈ (f(x+h) - f(x-h)) / (2h)"""
    return (f(x + h) - f(x - h)) / (2 * h)


def derivada_segunda_centrada(f: Callable[[float], float], x: float, h: float) -> float:
    """f''(x) ≈ (f(x+h) - 2f(x) + f(x-h)) / h²"""
    return (f(x + h) - 2 * f(x) + f(x - h)) / (h**2)


# --- Álgebra lineal (resolución Ax = b) ---


def resolver_sistema_lineal(A: Sequence[Sequence[float]], b: Sequence[float]) -> np.ndarray:
    """Solución de Ax = b con numpy.linalg.solve (eliminación gaussiana con pivoteo)."""
    A_arr = np.asarray(A, dtype=float)
    b_arr = np.asarray(b, dtype=float).reshape(-1)
    if A_arr.shape[0] != A_arr.shape[1] or A_arr.shape[0] != len(b_arr):
        raise ValueError("A debe ser cuadrada y compatible con b.")
    return np.linalg.solve(A_arr, b_arr)


# --- Ejemplos rápidos (descomenta o ejecuta: python formulas_clase_ma.py) ---


def _demo() -> None:
    print("=== Errores ===")
    print("E_abs(3.14, pi) =", error_absoluto(3.14, math.pi))
    print("E_rel(3.14, pi) =", error_relativo(3.14, math.pi))

    print("\n=== Biseccion: raiz de x^3 - x - 2 en [1, 2] ===")
    f = lambda x: x**3 - x - 2
    r, it = biseccion(f, 1.0, 2.0)
    print(f"raiz ~ {r}, iteraciones = {it}, f(r) = {f(r)}")

    print("\n=== Newton: misma funcion, f'(x) = 3x^2 - 1 ===")
    df = lambda x: 3 * x**2 - 1
    r2, it2 = newton_raphson(f, df, 1.5)
    print(f"raiz ~ {r2}, iteraciones = {it2}, f(r) = {f(r2)}")

    print("\n=== Integral de 0 a 1 de e^(-x) dx ===")
    g = lambda x: math.exp(-x)
    exacto = 1 - math.exp(-1)
    T = regla_trapecio(g, 0, 1, 50)
    S = regla_simpson_13(g, 0, 1, 50)
    print(f"Trapecio n=50: {T}, Simpson: {S}, exacto: {exacto}")

    print("\n=== derivada de sin(x) en 0, h=1e-5 ===")
    h = 1e-5
    s = math.sin
    print("centrada:", derivada_centrada(s, 0.0, h), "(esperado cos(0)=1)")

    print("\n=== Sistema 2x2 ===")
    A = [[2, 1], [1, 3]]
    b_vec = [1, 2]
    x_sol = resolver_sistema_lineal(A, b_vec)
    print("x =", x_sol)


if __name__ == "__main__":
    _demo()
