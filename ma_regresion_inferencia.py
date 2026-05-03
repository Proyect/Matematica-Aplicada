"""
Inferencia en regresion lineal simple (complemento habitual a la estimacion puntual).

Errores estandar, contraste t sobre la pendiente beta, intervalos de confianza
para alpha y beta, y F de significacion global (MSR/MSE), usando la t de Student
y la F de Fisher con scipy (libros tipo Anderson / Wackerly).

Requisitos: numpy, scipy
"""

from __future__ import annotations

from dataclasses import dataclass

from ma_minimos_cuadrados import ResultadoRegresionLineal


@dataclass
class InferenciaRegresionLineal:
    """Inferencia clasica para Y = alpha + beta * X + e, con n observaciones y gl = n-2."""

    nivel: float
    gl: int
    se: float
    se_beta: float
    se_alpha: float
    t_estadistico_beta: float
    p_valor_beta: float
    ic_beta_inf: float
    ic_beta_sup: float
    ic_alpha_inf: float
    ic_alpha_sup: float
    f_estadistico: float
    p_valor_f: float


def inferencia_regresion_lineal(
    res: ResultadoRegresionLineal,
    nivel: float = 0.05,
) -> InferenciaRegresionLineal:
    """
    Supuestos habituales: errores i.i.d. N(0, sigma^2) con sigma desconocido.

    MSE = SSE/(n-2), se = sqrt(MSE).
    se(beta) = sqrt(MSE/Sxx), se(alpha) = sqrt(MSE*(1/n + x_bar^2/Sxx)).
    t0 = beta / se(beta) ~ t_{n-2} bajo H0: beta = 0.
    IC al 1-nivel: beta +/- t_{1-nivel/2, n-2} * se(beta) (idem para alpha).
    F = (SSR/1)/(SSE/(n-2)) = MSR/MSE ~ F_{1, n-2} (en regresion simple equivale a t0^2).
    """
    from scipy import stats

    if res.n <= 2:
        raise ValueError("Se necesitan al menos 3 observaciones para inferencia (gl = n-2 >= 1).")
    if not (0 < nivel < 1):
        raise ValueError("nivel debe estar en (0,1).")

    n = res.n
    gl = n - 2
    mse = res.mse
    if mse <= 0 or not np_isfinite(mse):
        raise ValueError("MSE no valido; no se puede calcular inferencia.")

    se = float(mse**0.5)
    sxx = res.sxx
    if sxx <= 1e-15:
        raise ValueError("Sxx nulo.")

    se_beta = float((mse / sxx) ** 0.5)
    se_alpha = float((mse * (1.0 / n + (res.x_media**2) / sxx)) ** 0.5)

    t_beta = res.beta / se_beta if se_beta > 1e-15 else float("nan")
    p_beta = float(2 * stats.t.sf(abs(t_beta), gl))

    t_crit = float(stats.t.ppf(1 - nivel / 2, gl))
    ic_bi = res.beta - t_crit * se_beta
    ic_bs = res.beta + t_crit * se_beta
    ic_ai = res.alpha - t_crit * se_alpha
    ic_as = res.alpha + t_crit * se_alpha

    msr = res.ssr / 1.0
    f0 = msr / mse if mse > 0 else float("nan")
    p_f = float(stats.f.sf(f0, 1, gl))

    return InferenciaRegresionLineal(
        nivel=nivel,
        gl=gl,
        se=se,
        se_beta=se_beta,
        se_alpha=se_alpha,
        t_estadistico_beta=t_beta,
        p_valor_beta=p_beta,
        ic_beta_inf=ic_bi,
        ic_beta_sup=ic_bs,
        ic_alpha_inf=ic_ai,
        ic_alpha_sup=ic_as,
        f_estadistico=f0,
        p_valor_f=p_f,
    )


def np_isfinite(x: float) -> bool:
    import math

    return math.isfinite(x)


def demo() -> None:
    import numpy as np

    from ma_minimos_cuadrados import regresion_lineal_simple

    x = np.array([0.0, 1.0, 2.0, 3.0, 4.0])
    y = np.array([1.1, 1.9, 3.2, 3.9, 5.1])
    res = regresion_lineal_simple(x, y)
    inf = inferencia_regresion_lineal(res, nivel=0.05)
    print("=== Inferencia regresion simple (nivel 0.05) ===")
    print(f"gl = {inf.gl}, se = sqrt(MSE) = {inf.se}")
    print(f"se(beta) = {inf.se_beta}, se(alpha) = {inf.se_alpha}")
    print(f"t (H0: beta=0) = {inf.t_estadistico_beta}, p-valor (bilateral) = {inf.p_valor_beta}")
    print(f"IC beta: [{inf.ic_beta_inf}, {inf.ic_beta_sup}]")
    print(f"IC alpha: [{inf.ic_alpha_inf}, {inf.ic_alpha_sup}]")
    print(f"F (MSR/MSE) = {inf.f_estadistico}, p-valor = {inf.p_valor_f}")


if __name__ == "__main__":
    demo()
