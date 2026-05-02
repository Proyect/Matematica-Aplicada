"""
Optimizacion unidimensional: busqueda dorada (golden section) para minimo
de una funcion unimodal en [a, b].

Requisitos: solo float / sin numpy obligatorio (implementacion escalar).
"""

from __future__ import annotations

from typing import Callable


def golden_section_search(
    f: Callable[[float], float],
    a: float,
    b: float,
    tol: float = 1e-6,
    max_iter: int = 200,
) -> tuple[float, float, int]:
    """
    Minimiza f en [a,b] suponiendo unimodalidad.
    Usa razon aurea phi = (1+sqrt(5))/2; mismo esquema que el libro clasico de optimizacion.
    Devuelve (x_min, f(x_min), iteraciones).
    """
    phi = (1 + 5**0.5) / 2
    resphi = 2 - phi  # 1/phi^2 aprox

    x1 = a + resphi * (b - a)
    x2 = b - resphi * (b - a)
    f1, f2 = f(x1), f(x2)
    it = 0
    while abs(b - a) > tol and it < max_iter:
        it += 1
        if f1 < f2:
            b, x2, f2 = x2, x1, f1
            x1 = a + resphi * (b - a)
            f1 = f(x1)
        else:
            a, x1, f1 = x1, x2, f2
            x2 = b - resphi * (b - a)
            f2 = f(x2)
    x_min = (a + b) / 2
    return x_min, f(x_min), it


def demo() -> None:
    # Minimo de (x-2)^2 en [-1, 5] es x=2
    f = lambda x: (x - 2.0) ** 2
    xm, fm, it = golden_section_search(f, -1.0, 5.0, tol=1e-8)
    print("=== Golden section: min (x-2)^2 en [-1, 5] ===")
    print(f"x_min ~ {xm}, f_min ~ {fm}, iteraciones = {it}")


if __name__ == "__main__":
    demo()
