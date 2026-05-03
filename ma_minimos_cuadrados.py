"""
Ajuste por minimos cuadrados y regresion lineal simple (Unidad 3).

Incluye las formulas del apunte *Regresion y Correlacion Lineal* (UGR Lic. Ciencia de Datos):
  - Pendiente beta y ordenada al origen alpha (metodo de minimos cuadrados).
  - SST, SSR, SSE y R^2 = SSR/SST = 1 - SSE/SST.
  - Coeficiente de correlacion r (con R^2 = r^2 en regresion simple).
  - Prediccion y_hat = alpha + beta * x.

Requisitos: numpy
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class ResultadoRegresionLineal:
    """Resultados de regresion lineal simple Y ~ alpha + beta * X (apunte U3)."""

    n: int
    x_media: float
    y_media: float
    alpha: float
    beta: float
    y_hat: np.ndarray
    residuos: np.ndarray
    sst: float
    ssr: float
    sse: float
    r2: float
    r: float
    mse: float
    sxx: float
    syy: float
    sxy: float


def regresion_lineal_simple(x: np.ndarray, y: np.ndarray) -> ResultadoRegresionLineal:
    """
    Estima la recta y_hat = alpha + beta * x minimizando sum_i (y_i - alpha - beta x_i)^2.

    Formulas (apunte Anderson / U3):
      beta = sum((xi - x_media)(yi - y_media)) / sum((xi - x_media)^2)
           = (sum(xi yi) - n x_media y_media) / (sum(xi^2) - n x_media^2)
      alpha = y_media - beta * x_media

    Sumas de cuadrados:
      SST = sum((yi - y_media)^2)
      SSR = sum((y_hat_i - y_media)^2)
      SSE = sum((yi - y_hat_i)^2)
    con SST = SSR + SSE.

    Correlacion:
      r = sum((xi-x_media)(yi-y_media)) / sqrt(Sxx * Syy)
    En regresion simple, R^2 = r^2 y sign(r) = sign(beta).
    """
    x = np.asarray(x, dtype=float).ravel()
    y = np.asarray(y, dtype=float).ravel()
    if len(x) != len(y) or len(x) < 2:
        raise ValueError("Se necesitan al menos dos pares (x, y).")
    n = int(len(x))
    x_media = float(np.mean(x))
    y_media = float(np.mean(y))
    dx = x - x_media
    dy = y - y_media
    sxx = float(np.sum(dx * dx))
    syy = float(np.sum(dy * dy))
    sxy = float(np.sum(dx * dy))

    if sxx <= 1e-15:
        raise ValueError("La variable X no tiene variacion (Sxx = 0); no se puede ajustar pendiente.")

    beta = sxy / sxx
    alpha = y_media - beta * x_media
    y_hat = alpha + beta * x
    residuos = y - y_hat

    sse = float(np.sum(residuos**2))
    sst = syy
    ssr = float(np.sum((y_hat - y_media) ** 2))

    if sst <= 1e-15:
        r2 = 1.0 if sse <= 1e-15 else 0.0
    else:
        r2 = ssr / sst

    if syy <= 1e-15:
        r = 0.0
    else:
        r_raw = sxy / (sxx**0.5 * syy**0.5)
        r = float(np.clip(r_raw, -1.0, 1.0))

    if n > 2:
        mse = sse / (n - 2)
    else:
        mse = float("nan")

    return ResultadoRegresionLineal(
        n=n,
        x_media=x_media,
        y_media=y_media,
        alpha=float(alpha),
        beta=float(beta),
        y_hat=y_hat.astype(float),
        residuos=residuos.astype(float),
        sst=sst,
        ssr=ssr,
        sse=sse,
        r2=float(r2),
        r=r,
        mse=mse,
        sxx=sxx,
        syy=syy,
        sxy=sxy,
    )


def predecir_y(x_nuevo: float, alpha: float, beta: float) -> float:
    """y_hat = alpha + beta * x (prediccion puntual, apunte U3)."""
    return float(alpha + beta * float(x_nuevo))


def texto_fuerza_correlacion(r: float) -> str:
    """Criterios del apunte U3 sobre |r|."""
    a = abs(r)
    if a <= 0.5:
        return "debil (|r| <= 0,5)"
    if a < 0.8:
        return "moderada (0,5 < |r| < 0,8)"
    return "fuerte (|r| >= 0,8)"


def minimos_cuadrados_lineal(x: np.ndarray, y: np.ndarray) -> tuple[float, float]:
    """
    Recta y ~ alpha + beta * x por minimos cuadrados (equivale a regresion_lineal_simple).
    Devuelve (alpha, beta) en el orden ordenada, pendiente.
    """
    res = regresion_lineal_simple(x, y)
    return res.alpha, res.beta


def minimos_cuadrados_polinomio(x: np.ndarray, y: np.ndarray, grado: int) -> np.ndarray:
    """
    Coeficientes del polinomio en base monomial {1, x, x^2, ...},
    orden [a0, a1, ..., a_grado] para y ~ sum_k a_k x^k.
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
    res = regresion_lineal_simple(x, y)
    print("=== Regresion lineal simple (U3) ===")
    print(f"n = {res.n}, x_media = {res.x_media}, y_media = {res.y_media}")
    print(f"alpha (ordenada) = {res.alpha}, beta (pendiente) = {res.beta}")
    print(f"Recta: y_hat = {res.alpha} + ({res.beta}) * x")
    print(f"SST = {res.sst}, SSR = {res.ssr}, SSE = {res.sse}")
    print(f"Comprobacion SST ~ SSR+SSE: {res.sst} vs {res.ssr + res.sse}")
    print(f"R^2 = {res.r2}, r = {res.r}, MSE = {res.mse}")
    print(f"Fuerza correlacion (apunte): {texto_fuerza_correlacion(res.r)}")

    # Ejemplo altitud / temperatura del apunte (valores en metros y °C)
    alt = np.array(
        [200, 200, 400, 400, 600, 600, 700, 700, 900, 900, 1000, 1000, 1000, 1200, 1200],
        dtype=float,
    )
    temp = np.array([14, 18, 16, 14, 13, 14, 11, 14, 10, 9, 9, 13, 11, 11, 7], dtype=float)
    r2 = regresion_lineal_simple(alt, temp)
    print("\n=== Ejemplo apunte: temperatura vs altitud ===")
    print(f"beta ~ {r2.beta:.6f} (apunte: -0,007), alpha ~ {r2.alpha:.3f} (apunte: 17,459)")
    print(f"R^2 ~ {r2.r2:.4f} (apunte ilustrativo: 0,6914 con otra tabla de ejemplo)")

    c = minimos_cuadrados_polinomio(x, y, 2)
    print("\n=== Ajuste cuadratico (coef a0..a2) ===")
    print(c)


if __name__ == "__main__":
    demo()
