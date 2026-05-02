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

1. Entra en [github.com/new](https://github.com/new) e inicia sesión.
2. **Repository name:** por ejemplo `formulas-matematica-aplicada` (sin espacios).
3. Elige **Public**. No marques “Add a README” (ya tienes uno local).
4. Crea el repositorio y copia la URL HTTPS (p. ej. `https://github.com/TU_USUARIO/formulas-matematica-aplicada.git`).

En PowerShell, dentro de esta carpeta:

```powershell
cd "c:\Users\amdiaz\Desktop\code\Python\v.13.13\Matematica Aplicada"
git remote add origin https://github.com/TU_USUARIO/NOMBRE_REPO.git
git push -u origin main
```

Sustituye `TU_USUARIO` y `NOMBRE_REPO` por los tuyos. Si GitHub pide autenticación, usa un **Personal Access Token** como contraseña (no la contraseña de la cuenta), o configura [Git Credential Manager](https://github.com/git-ecosystem/git-credential-manager).

Opcional: instala [GitHub CLI](https://cli.github.com/) (`gh`) y podrás crear el remoto desde terminal con `gh repo create`.

## Licencia

[MIT](LICENSE).
