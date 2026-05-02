# Formulas — Matemática Aplicada (métodos numéricos)

Script en Python con implementaciones de fórmulas habituales de **matemática aplicada / métodos numéricos**: errores, bisección, Newton–Raphson, trapecio y Simpson, diferencias finitas y resolución de sistemas lineales.

Contexto de la clase de referencia: [Clase MA - 27/04/26](https://www.youtube.com/watch?v=_SgUUsTz390) (MATEMÁTICA APLICADA LCD).

## Requisitos

- Python 3.10 o superior recomendado
- Dependencias: `pip install -r requirements.txt`

## Uso

```bash
python formulas_clase_ma.py
```

Ejecuta la demo. También puedes importar las funciones desde otro módulo:

```python
from formulas_clase_ma import biseccion, newton_raphson, regla_trapecio
```

## Archivos

| Archivo | Descripción |
|--------|---------------|
| `formulas_clase_ma.py` | Funciones numéricas y demo |
| `requirements.txt` | Dependencias (`numpy`) |
| `LICENSE` | Licencia MIT |
| `.github/workflows/ci.yml` | CI: instala dependencias y ejecuta la demo |

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

Tras el primer `push`, en GitHub se ejecutará el workflow **CI** (instala `numpy` y corre `python formulas_clase_ma.py`).

## Licencia

[MIT](LICENSE).
