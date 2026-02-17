# Render Build Script - Windows PowerShell
# Usage: .\render-build.ps1

Write-Host "Building AgriTech for Render..."

try {
    Write-Host "Cleaning previous builds..."
    Remove-Item -Recurse -Force -ErrorAction SilentlyContinue build, dist, *.egg-info
    Get-ChildItem -Recurse -Directory -Filter __pycache__ | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
    Get-ChildItem -Recurse -Filter "*.pyc" | Remove-Item -Force -ErrorAction SilentlyContinue

    Write-Host "Installing dependencies..."
    python -m pip install --upgrade pip setuptools wheel
    python -m pip install -r requirements.txt

    Write-Host "Build complete!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:"
    Write-Host "1. Test locally: gunicorn run:app -b 0.0.0.0:5000"
    Write-Host "2. Push to GitHub: git push origin main"
    Write-Host "3. Render will automatically build and deploy"
}
catch {
    Write-Host "Build failed: $_" -ForegroundColor Red
    exit 1
}
