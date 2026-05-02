"""
Metodos numericos para EDO escalar: y' = f(t, y).

Euler explicito, Heun (RK2) y Runge-Kutta clasico de orden 4 (RK4).

Requisitos: numpy
"""

from __future__ import annotations

import math
from typing import Callable

import numpy as np


def euler(
    f: Callable[[float, float], float],
    t0: float,
    y0: float,
    t_end: float,
    n_pasos: int,
) -> tuple[np.ndarray, np.ndarray]:
    """y_{n+1} = y_n + h f(t_n, y_n), h = (t_end - t0) / n_pasos."""
    if n_pasos < 1:
        raise ValueError("n_pasos debe ser >= 1.")
    h = (t_end - t0) / n_pasos
    t = np.zeros(n_pasos + 1)
    y = np.zeros(n_pasos + 1)
    t[0], y[0] = t0, y0
    for n in range(n_pasos):
        y[n + 1] = y[n] + h * f(t[n], y[n])
        t[n + 1] = t[n] + h
    return t, y


def heun(
    f: Callable[[float, float], float],
    t0: float,
    y0: float,
    t_end: float,
    n_pasos: int,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Heun (RK2): predictor y* = y_n + h f(t_n,y_n);
    corrector y_{n+1} = y_n + h/2 (f(t_n,y_n) + f(t_{n+1}, y*)).
    """
    if n_pasos < 1:
        raise ValueError("n_pasos debe ser >= 1.")
    h = (t_end - t0) / n_pasos
    t = np.zeros(n_pasos + 1)
    y = np.zeros(n_pasos + 1)
    t[0], y[0] = t0, y0
    for n in range(n_pasos):
        k1 = f(t[n], y[n])
        y_star = y[n] + h * k1
        k2 = f(t[n] + h, y_star)
        y[n + 1] = y[n] + 0.5 * h * (k1 + k2)
        t[n + 1] = t[n] + h
    return t, y


def rk4(
    f: Callable[[float, float], float],
    t0: float,
    y0: float,
    t_end: float,
    n_pasos: int,
) -> tuple[np.ndarray, np.ndarray]:
    """Runge-Kutta de cuarto orden (formula clasica)."""
    if n_pasos < 1:
        raise ValueError("n_pasos debe ser >= 1.")
    h = (t_end - t0) / n_pasos
    t = np.zeros(n_pasos + 1)
    y = np.zeros(n_pasos + 1)
    t[0], y[0] = t0, y0
    for n in range(n_pasos):
        tn, yn = t[n], y[n]
        k1 = f(tn, yn)
        k2 = f(tn + 0.5 * h, yn + 0.5 * h * k1)
        k3 = f(tn + 0.5 * h, yn + 0.5 * h * k2)
        k4 = f(tn + h, yn + h * k3)
        y[n + 1] = yn + (h / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
        t[n + 1] = tn + h
    return t, y


def demo() -> None:
    # y' = -y, y(0)=1  =>  y(t)=exp(-t)
    f = lambda t, y: -y
    t0, y0, tend = 0.0, 1.0, 2.0
    n = 40

    _, ye = euler(f, t0, y0, tend, n)
    _, yh = heun(f, t0, y0, tend, n)
    _, yr = rk4(f, t0, y0, tend, n)
    exacto = math.exp(-tend)
    print("=== EDO y'=-y, y(0)=1, t en [0,2], n=40 ===")
    print(f"Euler y(2) ~ {ye[-1]}, error = {abs(ye[-1] - exacto)}")
    print(f"Heun  y(2) ~ {yh[-1]}, error = {abs(yh[-1] - exacto)}")
    print(f"RK4   y(2) ~ {yr[-1]}, error = {abs(yr[-1] - exacto)}")
    print(f"Exacto exp(-2) = {exacto}")


if __name__ == "__main__":
    demo()
