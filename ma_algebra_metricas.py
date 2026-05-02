"""
Normas vectoriales y matriciales, determinante y numero de condicion.

Requisitos: numpy
"""

from __future__ import annotations

from typing import Sequence

import numpy as np


def norma_vectorial(v: Sequence[float], p: float | int = 2) -> float:
    """||v||_p; p puede ser 1, 2, o np.inf."""
    arr = np.asarray(v, dtype=float).ravel()
    if p == np.inf:
        return float(np.max(np.abs(arr)))
    return float(np.linalg.norm(arr, ord=float(p)))


def norma_matricial_frobenius(A: Sequence[Sequence[float]]) -> float:
    """||A||_F = sqrt(sum_ij a_ij^2)."""
    return float(np.linalg.norm(np.asarray(A, dtype=float), ord="fro"))


def norma_matricial_inducida(A: Sequence[Sequence[float]], p: float | int = 2) -> float:
    """Norma matricial inducida (subordinada) ||A||_p."""
    return float(np.linalg.norm(np.asarray(A, dtype=float), ord=p))


def determinante(A: Sequence[Sequence[float]]) -> float:
    """det(A) para matriz cuadrada."""
    M = np.asarray(A, dtype=float)
    if M.ndim != 2 or M.shape[0] != M.shape[1]:
        raise ValueError("A debe ser cuadrada.")
    return float(np.linalg.det(M))


def numero_condicion(A: Sequence[Sequence[float]], p: float | int = 2) -> float:
    """kappa_p(A) = ||A||_p ||A^{-1}||_p (numpy.linalg.cond)."""
    return float(np.linalg.cond(np.asarray(A, dtype=float), p=p))


def demo() -> None:
    v = [3.0, -4.0]
    print("=== Normas del vector [3, -4] ===")
    print("L1:", norma_vectorial(v, 1), "L2:", norma_vectorial(v, 2), "Linf:", norma_vectorial(v, np.inf))
    A = [[1.0, 2.0], [3.0, 4.0]]
    print("=== Matriz [[1,2],[3,4]] ===")
    print("Frobenius:", norma_matricial_frobenius(A))
    print("det:", determinante(A))
    print("cond(2):", numero_condicion(A, 2))


if __name__ == "__main__":
    demo()
