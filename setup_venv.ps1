# Crea o actualiza el entorno virtual .venv e instala requirements.txt
# Uso (PowerShell): .\setup_venv.ps1

$ErrorActionPreference = "Stop"
$Root = $PSScriptRoot
Set-Location -LiteralPath $Root

$Py = Get-Command python -ErrorAction SilentlyContinue
if (-not $Py) {
    Write-Error "No se encontro 'python' en el PATH. Instala Python 3 y vuelve a intentar."
}

$VenvPython = Join-Path $Root ".venv\Scripts\python.exe"
if (-not (Test-Path -LiteralPath $VenvPython)) {
    Write-Host "Creando entorno virtual en .venv ..."
    python -m venv (Join-Path $Root ".venv")
}

Write-Host "Actualizando pip e instalando dependencias ..."
& $VenvPython -m pip install --upgrade pip
& (Join-Path $Root ".venv\Scripts\pip.exe") install -r (Join-Path $Root "requirements.txt")

Write-Host ""
Write-Host "Listo. Activa el entorno en PowerShell:"
Write-Host "  .\.venv\Scripts\Activate.ps1"
Write-Host "Prueba:"
Write-Host "  python run_all_demos.py"
