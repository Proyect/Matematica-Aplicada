# Formulas — Matemática Aplicada (métodos numéricos)

Scripts en Python con fórmulas habituales de **matemática aplicada / métodos numéricos**: errores, raíces (bisección, Newton, secante, punto fijo), integración (trapecio, Simpson 1/3 y 3/8, punto medio), diferencias finitas, EDO (Euler, Heun, RK4), interpolación, mínimos cuadrados, normas y condicionamiento, y optimización 1D (sección áurea).

Contexto de la clase de referencia: [Clase MA - 27/04/26](https://www.youtube.com/watch?v=_SgUUsTz390) (MATEMÁTICA APLICADA LCD).

## Requisitos

- Python 3.10 o superior recomendado
- Dependencias: `pip install -r requirements.txt`

## Uso

```bash
python run_all_demos.py
```

Ejecuta todas las demos. Solo el núcleo original:

```bash
python formulas_clase_ma.py
```

También puedes importar desde cualquier módulo, por ejemplo:

```python
from formulas_clase_ma import biseccion, newton_raphson, regla_trapecio
from ma_edo import rk4
from ma_interpolacion import lagrange_eval
```

## Archivos

| Archivo | Descripción |
|--------|---------------|
| `formulas_clase_ma.py` | Errores, bisección, Newton, trapecio, Simpson 1/3, diferencias finitas, `Ax=b` |
| `ma_interpolacion.py` | Lineal a trozos y Lagrange |
| `ma_raices_avanzado.py` | Secante y punto fijo |
| `ma_edo.py` | Euler, Heun, RK4 para `y' = f(t,y)` escalar |
| `ma_minimos_cuadrados.py` | Ajuste lineal y polinómico por mínimos cuadrados |
| `ma_algebra_metricas.py` | Normas, Frobenius, determinante, número de condición |
| `ma_optimizacion.py` | Búsqueda dorada (mínimo unimodal en un intervalo) |
| `ma_integracion_extras.py` | Punto medio compuesto y Simpson 3/8 compuesto |
| `run_all_demos.py` | Ejecuta todas las demos en secuencia |
| `requirements.txt` | Dependencias (`numpy`) |
| `LICENSE` | Licencia MIT |
| `.github/workflows/ci.yml` | CI: instala dependencias y ejecuta `run_all_demos.py` |

## Publicar en GitHub

### Opción A: GitHub CLI (recomendado si ya tienes `gh`)

1. Inicia sesión (solo la primera vez): `gh auth login` y sigue el asistente.
2. Desde esta carpeta del proyecto:

```powershell
cd "c:\Users\amdiaz\Desktop\code\Python\v.13.13\Matematica Aplicada"
gh repo create formulas-matematica-aplicada --public --source=. --remote=origin --push
```

Cambia `formulas-matematica-aplicada` si quieres otro nombre. Si ya existe un remoto `origin`, elimínalo antes: `git remote remove origin`.

### Opción B: Sitio web de GitHub

1. [github.com/new](https://github.com/new): nombre sugerido `formulas-matematica-aplicada`, repositorio **Public**, sin README inicial.
2. En PowerShell:

```powershell
cd "c:\Users\amdiaz\Desktop\code\Python\v.13.13\Matematica Aplicada"
git remote add origin https://github.com/TU_USUARIO/NOMBRE_REPO.git
git push -u origin main
```

Si pide contraseña, usa un **Personal Access Token** o [Git Credential Manager](https://github.com/git-ecosystem/git-credential-manager).

Tras el primer `push`, en GitHub se ejecutará el workflow **CI** (instala `numpy` y corre `python run_all_demos.py`).

## Licencia

[MIT](LICENSE).
