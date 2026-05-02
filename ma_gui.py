"""
Interfaz grafica (tkinter) para los metodos numericos del proyecto.

Ejecutar: python ma_gui.py

Las expresiones usan la variable x (o t e y en EDO) y pueden usar math.* y np.*
Ejemplo f(x): x**3 - x - 2
Ejemplo f(t,y) en EDO: -y  o  t - y
"""

from __future__ import annotations

import math
import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk

import numpy as np

import formulas_clase_ma as core
import ma_algebra_metricas as alg
import ma_edo as edo
import ma_integracion_extras as intex
import ma_interpolacion as interp
import ma_minimos_cuadrados as mc
import ma_optimizacion as opt
import ma_raices_avanzado as raizx


def _safe_eval_x(expr: str, x: float) -> float:
    env = {"__builtins__": {}}
    loc = {"x": float(x), "np": np, "math": math}
    return float(eval(expr, env, loc))


def _safe_eval_ty(expr: str, t: float, y: float) -> float:
    env = {"__builtins__": {}}
    loc = {"t": float(t), "y": float(y), "np": np, "math": math}
    return float(eval(expr, env, loc))


def _make_f(expr: str):
    return lambda xv: _safe_eval_x(expr, xv)


def _make_df(expr: str):
    return lambda xv: _safe_eval_x(expr, xv)


def _make_g(expr: str):
    return lambda xv: _safe_eval_x(expr, xv)


def _make_ft_y(expr: str):
    return lambda tv, yv: _safe_eval_ty(expr, tv, yv)


def _parse_floats(s: str) -> np.ndarray:
    parts = [p.strip() for p in s.replace(";", ",").split(",") if p.strip()]
    return np.array([float(p) for p in parts], dtype=float)


def _out_append(w: scrolledtext.ScrolledText, text: str) -> None:
    w.insert(tk.END, text + "\n")
    w.see(tk.END)


def _clear_out(w: scrolledtext.ScrolledText) -> None:
    w.delete("1.0", tk.END)


class MaApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Matematica Aplicada — Metodos numericos")
        self.geometry("780x620")
        self.minsize(640, 480)

        nb = ttk.Notebook(self)
        nb.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        self._build_tab_errores(nb)
        self._build_tab_raices(nb)
        self._build_tab_integracion(nb)
        self._build_tab_diferencias(nb)
        self._build_tab_sistema(nb)
        self._build_tab_interpolacion(nb)
        self._build_tab_edo(nb)
        self._build_tab_mc(nb)
        self._build_tab_optim(nb)
        self._build_tab_algebra(nb)

        hint = ttk.Label(
            self,
            text="Expresiones: variable x (o t,y en EDO). Permitido: numeros, + - * / **, math.sin, np.exp, etc.",
            font=("Segoe UI", 9),
        )
        hint.pack(fill=tk.X, padx=10, pady=(0, 6))

    def _shared_output(self, parent: ttk.Frame) -> scrolledtext.ScrolledText:
        lf = ttk.LabelFrame(parent, text="Resultado")
        lf.pack(fill=tk.BOTH, expand=True, pady=(8, 0))
        w = scrolledtext.ScrolledText(lf, height=12, wrap=tk.WORD, font=("Consolas", 10))
        w.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)
        return w

    def _build_tab_errores(self, nb: ttk.Notebook) -> None:
        f = ttk.Frame(nb, padding=8)
        nb.add(f, text="Errores")
        ttk.Label(f, text="Valor aproximado x_tilde:").grid(row=0, column=0, sticky=tk.W)
        e_ap = ttk.Entry(f, width=28)
        e_ap.grid(row=0, column=1, sticky=tk.W, padx=4)
        ttk.Label(f, text="Valor real x*:").grid(row=1, column=0, sticky=tk.W)
        e_re = ttk.Entry(f, width=28)
        e_re.grid(row=1, column=1, sticky=tk.W, padx=4)
        out = self._shared_output(f)

        def run() -> None:
            _clear_out(out)
            try:
                xa, xr = float(e_ap.get()), float(e_re.get())
                ea = core.error_absoluto(xa, xr)
                er = core.error_relativo(xa, xr)
                _out_append(out, f"Error absoluto: {ea}")
                _out_append(out, f"Error relativo: {er}")
            except Exception as ex:
                messagebox.showerror("Error", str(ex))

        ttk.Button(f, text="Calcular", command=run).grid(row=2, column=1, sticky=tk.W, pady=8)

    def _build_tab_raices(self, nb: ttk.Notebook) -> None:
        f = ttk.Frame(nb, padding=8)
        nb.add(f, text="Raices")
        row = 0
        ttk.Label(f, text="f(x) =").grid(row=row, column=0, sticky=tk.W)
        e_f = ttk.Entry(f, width=50)
        e_f.insert(0, "x**3 - x - 2")
        e_f.grid(row=row, column=1, sticky=tk.W, padx=4)
        row += 1
        ttk.Label(f, text="Metodo:").grid(row=row, column=0, sticky=tk.W)
        met = ttk.Combobox(f, width=18, values=("Biseccion", "Newton", "Secante"), state="readonly")
        met.set("Biseccion")
        met.grid(row=row, column=1, sticky=tk.W, padx=4)
        row += 1
        ttk.Label(f, text="a / x0:").grid(row=row, column=0, sticky=tk.W)
        e_a = ttk.Entry(f, width=14)
        e_a.insert(0, "1.0")
        e_a.grid(row=row, column=1, sticky=tk.W, padx=4)
        row += 1
        ttk.Label(f, text="b / x1 (secante o ignorar Newton):").grid(row=row, column=0, sticky=tk.W)
        e_b = ttk.Entry(f, width=14)
        e_b.insert(0, "2.0")
        e_b.grid(row=row, column=1, sticky=tk.W, padx=4)
        row += 1
        ttk.Label(f, text="f'(x) solo Newton:").grid(row=row, column=0, sticky=tk.W)
        e_df = ttk.Entry(f, width=50)
        e_df.insert(0, "3*x**2 - 1")
        e_df.grid(row=row, column=1, sticky=tk.W, padx=4)
        row += 1
        out = self._shared_output(f)

        def run() -> None:
            _clear_out(out)
            try:
                expr = e_f.get().strip()
                ff = _make_f(expr)
                m = met.get()
                a = float(e_a.get())
                b = float(e_b.get())
                if m == "Biseccion":
                    r, it = core.biseccion(ff, a, b)
                    _out_append(out, f"Raiz ~ {r}, iteraciones {it}, f(r)={ff(r)}")
                elif m == "Newton":
                    dff = _make_df(e_df.get().strip())
                    r, it = core.newton_raphson(ff, dff, a)
                    _out_append(out, f"Raiz ~ {r}, iteraciones {it}, f(r)={ff(r)}")
                else:
                    r, it = raizx.secante(ff, a, b)
                    _out_append(out, f"Raiz ~ {r}, iteraciones {it}, f(r)={ff(r)}")
            except Exception as ex:
                messagebox.showerror("Error", str(ex))

        ttk.Button(f, text="Calcular", command=run).grid(row=row + 1, column=1, sticky=tk.W, pady=8)

        # Punto fijo sub-block
        sep = ttk.Separator(f, orient=tk.HORIZONTAL)
        sep.grid(row=row + 2, column=0, columnspan=2, sticky=tk.EW, pady=10)
        row += 3
        ttk.Label(f, text="Punto fijo g(x) =").grid(row=row, column=0, sticky=tk.W)
        e_g = ttk.Entry(f, width=50)
        e_g.insert(0, "math.cos(x)")
        e_g.grid(row=row, column=1, sticky=tk.W, padx=4)
        row += 1
        ttk.Label(f, text="x0:").grid(row=row, column=0, sticky=tk.W)
        e_g0 = ttk.Entry(f, width=14)
        e_g0.insert(0, "0.5")
        e_g0.grid(row=row, column=1, sticky=tk.W, padx=4)

        def run_pf() -> None:
            _clear_out(out)
            try:
                gg = _make_g(e_g.get().strip())
                x0 = float(e_g0.get())
                r, it = raizx.punto_fijo(gg, x0)
                _out_append(out, f"Punto fijo ~ {r}, iter {it}, r-g(r)={r - gg(r)}")
            except Exception as ex:
                messagebox.showerror("Error", str(ex))

        ttk.Button(f, text="Calcular punto fijo", command=run_pf).grid(row=row + 1, column=1, sticky=tk.W, pady=6)

    def _build_tab_integracion(self, nb: ttk.Notebook) -> None:
        f = ttk.Frame(nb, padding=8)
        nb.add(f, text="Integracion")
        ttk.Label(f, text="f(x) =").grid(row=0, column=0, sticky=tk.W)
        e_f = ttk.Entry(f, width=50)
        e_f.insert(0, "math.exp(-x)")
        e_f.grid(row=0, column=1, sticky=tk.W, padx=4)
        ttk.Label(f, text="a, b, n:").grid(row=1, column=0, sticky=tk.W)
        e_a = ttk.Entry(f, width=8)
        e_a.insert(0, "0")
        e_b = ttk.Entry(f, width=8)
        e_b.insert(0, "1")
        e_n = ttk.Entry(f, width=8)
        e_n.insert(0, "50")
        fr = ttk.Frame(f)
        fr.grid(row=1, column=1, sticky=tk.W)
        e_a.pack(side=tk.LEFT, padx=2)
        e_b.pack(side=tk.LEFT, padx=2)
        e_n.pack(side=tk.LEFT, padx=2)
        ttk.Label(f, text="Regla:").grid(row=2, column=0, sticky=tk.W)
        met = ttk.Combobox(
            f,
            width=22,
            values=("Trapecio", "Simpson 1/3", "Punto medio", "Simpson 3/8"),
            state="readonly",
        )
        met.set("Trapecio")
        met.grid(row=2, column=1, sticky=tk.W, padx=4)
        out = self._shared_output(f)

        def run() -> None:
            _clear_out(out)
            try:
                ff = _make_f(e_f.get().strip())
                a, b, n = float(e_a.get()), float(e_b.get()), int(e_n.get())
                m = met.get()
                if m == "Trapecio":
                    val = core.regla_trapecio(ff, a, b, n)
                elif m == "Simpson 1/3":
                    if n % 2 != 0:
                        raise ValueError("n debe ser par para Simpson 1/3.")
                    val = core.regla_simpson_13(ff, a, b, n)
                elif m == "Punto medio":
                    val = intex.regla_punto_medio(ff, a, b, n)
                else:
                    if n % 3 != 0 or n < 3:
                        raise ValueError("n debe ser multiplo de 3 y >= 3 para Simpson 3/8.")
                    val = intex.regla_simpson_38(ff, a, b, n)
                _out_append(out, f"Integral aproximada: {val}")
            except Exception as ex:
                messagebox.showerror("Error", str(ex))

        ttk.Button(f, text="Calcular", command=run).grid(row=3, column=1, sticky=tk.W, pady=8)

    def _build_tab_diferencias(self, nb: ttk.Notebook) -> None:
        f = ttk.Frame(nb, padding=8)
        nb.add(f, text="Diferencias finitas")
        ttk.Label(f, text="f(x) =").grid(row=0, column=0, sticky=tk.W)
        e_f = ttk.Entry(f, width=50)
        e_f.insert(0, "math.sin(x)")
        e_f.grid(row=0, column=1, sticky=tk.W, padx=4)
        ttk.Label(f, text="x, h:").grid(row=1, column=0, sticky=tk.W)
        e_x = ttk.Entry(f, width=10)
        e_x.insert(0, "0.0")
        e_h = ttk.Entry(f, width=10)
        e_h.insert(0, "1e-5")
        fr = ttk.Frame(f)
        fr.grid(row=1, column=1, sticky=tk.W)
        e_x.pack(side=tk.LEFT, padx=2)
        e_h.pack(side=tk.LEFT, padx=2)
        ttk.Label(f, text="Tipo:").grid(row=2, column=0, sticky=tk.W)
        met = ttk.Combobox(
            f,
            width=18,
            values=("Progresiva", "Regresiva", "Centrada", "Segunda centrada"),
            state="readonly",
        )
        met.set("Centrada")
        met.grid(row=2, column=1, sticky=tk.W, padx=4)
        out = self._shared_output(f)

        def run() -> None:
            _clear_out(out)
            try:
                ff = _make_f(e_f.get().strip())
                xv, hv = float(e_x.get()), float(e_h.get())
                m = met.get()
                if m == "Progresiva":
                    v = core.derivada_progresiva(ff, xv, hv)
                elif m == "Regresiva":
                    v = core.derivada_regresiva(ff, xv, hv)
                elif m == "Centrada":
                    v = core.derivada_centrada(ff, xv, hv)
                else:
                    v = core.derivada_segunda_centrada(ff, xv, hv)
                _out_append(out, f"Aproximacion f' o f'': {v}")
            except Exception as ex:
                messagebox.showerror("Error", str(ex))

        ttk.Button(f, text="Calcular", command=run).grid(row=3, column=1, sticky=tk.W, pady=8)

    def _build_tab_sistema(self, nb: ttk.Notebook) -> None:
        f = ttk.Frame(nb, padding=8)
        nb.add(f, text="Sistema Ax=b")
        ttk.Label(f, text="Matriz 2x2 (filas: a11 a12 | a21 a22)").grid(row=0, column=0, columnspan=4, sticky=tk.W)
        e11 = ttk.Entry(f, width=8)
        e12 = ttk.Entry(f, width=8)
        e21 = ttk.Entry(f, width=8)
        e22 = ttk.Entry(f, width=8)
        for i, e in enumerate((e11, e12, e21, e22)):
            e.grid(row=1, column=i, padx=2, pady=2)
        e11.insert(0, "2")
        e12.insert(0, "1")
        e21.insert(0, "1")
        e22.insert(0, "3")
        ttk.Label(f, text="b1, b2:").grid(row=2, column=0, sticky=tk.W)
        eb1 = ttk.Entry(f, width=8)
        eb2 = ttk.Entry(f, width=8)
        eb1.insert(0, "1")
        eb2.insert(0, "2")
        eb1.grid(row=2, column=1, padx=2)
        eb2.grid(row=2, column=2, padx=2)
        out = self._shared_output(f)

        def run() -> None:
            _clear_out(out)
            try:
                A = [
                    [float(e11.get()), float(e12.get())],
                    [float(e21.get()), float(e22.get())],
                ]
                b = [float(eb1.get()), float(eb2.get())]
                x = core.resolver_sistema_lineal(A, b)
                _out_append(out, f"Solucion x = {x.tolist()}")
            except Exception as ex:
                messagebox.showerror("Error", str(ex))

        ttk.Button(f, text="Resolver", command=run).grid(row=3, column=1, sticky=tk.W, pady=8)

    def _build_tab_interpolacion(self, nb: ttk.Notebook) -> None:
        f = ttk.Frame(nb, padding=8)
        nb.add(f, text="Interpolacion")
        ttk.Label(f, text="Nodos x (separados por coma):").grid(row=0, column=0, sticky=tk.W)
        e_x = ttk.Entry(f, width=50)
        e_x.insert(0, "0,1,2,3")
        e_x.grid(row=0, column=1, sticky=tk.W, padx=4)
        ttk.Label(f, text="Valores y:").grid(row=1, column=0, sticky=tk.W)
        e_y = ttk.Entry(f, width=50)
        e_y.insert(0, "1,2,1.5,2.5")
        e_y.grid(row=1, column=1, sticky=tk.W, padx=4)
        ttk.Label(f, text="Punto xq:").grid(row=2, column=0, sticky=tk.W)
        e_q = ttk.Entry(f, width=14)
        e_q.insert(0, "1.5")
        e_q.grid(row=2, column=1, sticky=tk.W, padx=4)
        met = ttk.Combobox(f, width=14, values=("Lagrange", "Lineal"), state="readonly")
        met.set("Lagrange")
        met.grid(row=3, column=1, sticky=tk.W, padx=4)
        ttk.Label(f, text="Metodo:").grid(row=3, column=0, sticky=tk.W)
        out = self._shared_output(f)

        def run() -> None:
            _clear_out(out)
            try:
                xs = _parse_floats(e_x.get())
                ys = _parse_floats(e_y.get())
                xq = float(e_q.get())
                if met.get() == "Lagrange":
                    v = interp.lagrange_eval(xs, ys, xq)
                else:
                    v = interp.interpolacion_lineal(xs, ys, xq)
                _out_append(out, f"P({xq}) ~ {v}")
            except Exception as ex:
                messagebox.showerror("Error", str(ex))

        ttk.Button(f, text="Evaluar", command=run).grid(row=4, column=1, sticky=tk.W, pady=8)

    def _build_tab_edo(self, nb: ttk.Notebook) -> None:
        f = ttk.Frame(nb, padding=8)
        nb.add(f, text="EDO y'=f(t,y)")
        ttk.Label(f, text="f(t,y) =").grid(row=0, column=0, sticky=tk.W)
        e_f = ttk.Entry(f, width=40)
        e_f.insert(0, "-y")
        e_f.grid(row=0, column=1, sticky=tk.W, padx=4)
        ttk.Label(f, text="t0, y0, t_fin, n:").grid(row=1, column=0, sticky=tk.W)
        et0 = ttk.Entry(f, width=8)
        ey0 = ttk.Entry(f, width=8)
        et1 = ttk.Entry(f, width=8)
        en = ttk.Entry(f, width=8)
        for e, v in ((et0, "0"), (ey0, "1"), (et1, "2"), (en, "40")):
            e.insert(0, v)
        fr = ttk.Frame(f)
        fr.grid(row=1, column=1, sticky=tk.W)
        for e in (et0, ey0, et1, en):
            e.pack(side=tk.LEFT, padx=2)
        met = ttk.Combobox(f, width=10, values=("Euler", "Heun", "RK4"), state="readonly")
        met.set("RK4")
        met.grid(row=2, column=1, sticky=tk.W, padx=4)
        ttk.Label(f, text="Metodo:").grid(row=2, column=0, sticky=tk.W)
        out = self._shared_output(f)

        def run() -> None:
            _clear_out(out)
            try:
                ft_y = _make_ft_y(e_f.get().strip())
                t0 = float(et0.get())
                y0 = float(ey0.get())
                t1 = float(et1.get())
                n = int(en.get())
                m = met.get()
                if m == "Euler":
                    t, y = edo.euler(ft_y, t0, y0, t1, n)
                elif m == "Heun":
                    t, y = edo.heun(ft_y, t0, y0, t1, n)
                else:
                    t, y = edo.rk4(ft_y, t0, y0, t1, n)
                _out_append(out, f"y({t1}) ~ {y[-1]}")
                _out_append(out, f"Puntos: {n+1} valores de t de {t[0]} a {t[-1]}")
            except Exception as ex:
                messagebox.showerror("Error", str(ex))

        ttk.Button(f, text="Integrar", command=run).grid(row=3, column=1, sticky=tk.W, pady=8)

    def _build_tab_mc(self, nb: ttk.Notebook) -> None:
        f = ttk.Frame(nb, padding=8)
        nb.add(f, text="Minimos cuadrados")
        ttk.Label(f, text="x (coma):").grid(row=0, column=0, sticky=tk.W)
        e_x = ttk.Entry(f, width=50)
        e_x.insert(0, "0,1,2,3,4")
        e_x.grid(row=0, column=1, sticky=tk.W, padx=4)
        ttk.Label(f, text="y (coma):").grid(row=1, column=0, sticky=tk.W)
        e_y = ttk.Entry(f, width=50)
        e_y.insert(0, "1.1,1.9,3.2,3.9,5.1")
        e_y.grid(row=1, column=1, sticky=tk.W, padx=4)
        ttk.Label(f, text="Grado polinomio (0=constante, 1=lineal, ...):").grid(row=2, column=0, sticky=tk.W)
        e_g = ttk.Entry(f, width=6)
        e_g.insert(0, "1")
        e_g.grid(row=2, column=1, sticky=tk.W, padx=4)
        out = self._shared_output(f)

        def run() -> None:
            _clear_out(out)
            try:
                xs = _parse_floats(e_x.get())
                ys = _parse_floats(e_y.get())
                g = int(e_g.get())
                if g == 1:
                    a0, a1 = mc.minimos_cuadrados_lineal(xs, ys)
                    _out_append(out, f"Recta: y = {a0} + {a1} * x")
                else:
                    c = mc.minimos_cuadrados_polinomio(xs, ys, g)
                    _out_append(out, f"Coeficientes (termino constante primero): {c.tolist()}")
            except Exception as ex:
                messagebox.showerror("Error", str(ex))

        ttk.Button(f, text="Ajustar", command=run).grid(row=3, column=1, sticky=tk.W, pady=8)

    def _build_tab_optim(self, nb: ttk.Notebook) -> None:
        f = ttk.Frame(nb, padding=8)
        nb.add(f, text="Optimizacion 1D")
        ttk.Label(f, text="f(x) a minimizar:").grid(row=0, column=0, sticky=tk.W)
        e_f = ttk.Entry(f, width=50)
        e_f.insert(0, "(x - 2)**2")
        e_f.grid(row=0, column=1, sticky=tk.W, padx=4)
        ttk.Label(f, text="Intervalo [a,b]:").grid(row=1, column=0, sticky=tk.W)
        ea = ttk.Entry(f, width=8)
        eb = ttk.Entry(f, width=8)
        ea.insert(0, "-1")
        eb.insert(0, "5")
        fr = ttk.Frame(f)
        fr.grid(row=1, column=1, sticky=tk.W)
        ea.pack(side=tk.LEFT, padx=2)
        eb.pack(side=tk.LEFT, padx=2)
        out = self._shared_output(f)

        def run() -> None:
            _clear_out(out)
            try:
                ff = _make_f(e_f.get().strip())
                a, b = float(ea.get()), float(eb.get())
                xm, fm, it = opt.golden_section_search(ff, a, b)
                _out_append(out, f"x_min ~ {xm}, f_min ~ {fm}, iteraciones {it}")
            except Exception as ex:
                messagebox.showerror("Error", str(ex))

        ttk.Button(f, text="Minimizar", command=run).grid(row=2, column=1, sticky=tk.W, pady=8)

    def _build_tab_algebra(self, nb: ttk.Notebook) -> None:
        f = ttk.Frame(nb, padding=8)
        nb.add(f, text="Algebra / normas")
        ttk.Label(f, text="Matriz 2x2:").grid(row=0, column=0, sticky=tk.W)
        e11 = ttk.Entry(f, width=8)
        e12 = ttk.Entry(f, width=8)
        e21 = ttk.Entry(f, width=8)
        e22 = ttk.Entry(f, width=8)
        for i, e in enumerate((e11, e12, e21, e22)):
            e.grid(row=1, column=i, padx=2)
        e11.insert(0, "1")
        e12.insert(0, "2")
        e21.insert(0, "3")
        e22.insert(0, "4")
        out = self._shared_output(f)

        def run() -> None:
            _clear_out(out)
            try:
                A = [
                    [float(e11.get()), float(e12.get())],
                    [float(e21.get()), float(e22.get())],
                ]
                _out_append(out, f"det(A) = {alg.determinante(A)}")
                _out_append(out, f"cond_2(A) = {alg.numero_condicion(A, 2)}")
                _out_append(out, f"||A||_F = {alg.norma_matricial_frobenius(A)}")
            except Exception as ex:
                messagebox.showerror("Error", str(ex))

        ttk.Button(f, text="Calcular", command=run).grid(row=2, column=1, sticky=tk.W, pady=8)


def main() -> None:
    app = MaApp()
    app.mainloop()


if __name__ == "__main__":
    main()
