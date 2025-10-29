# Script de déploiement automatique pour Qwen-Image-Edit Handler
# Usage: .\deploy.ps1 -DockerUsername "votre-username"

param(
    [Parameter(Mandatory=$true)]
    [string]$DockerUsername
)

Write-Host "🚀 Déploiement du Handler Qwen-Image-Edit" -ForegroundColor Cyan
Write-Host ""

# Variables
$ImageName = "$DockerUsername/qwen-tryon:latest"
$ScriptPath = $PSScriptRoot

# Vérifier que Docker est lancé
Write-Host "🔍 Vérification de Docker..." -ForegroundColor Yellow
try {
    docker version | Out-Null
    Write-Host "✅ Docker est actif" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker n'est pas lancé" -ForegroundColor Red
    Write-Host "Veuillez lancer Docker Desktop et réessayer" -ForegroundColor Yellow
    exit 1
}

Write-Host ""

# Build l'image
Write-Host "🔨 Build de l'image Docker..." -ForegroundColor Yellow
Write-Host "Image: $ImageName" -ForegroundColor Cyan
Write-Host ""

docker build -t $ImageName $ScriptPath

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Erreur lors du build" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "✅ Image buildée avec succès!" -ForegroundColor Green
Write-Host ""

# Login Docker Hub
Write-Host "🔐 Login Docker Hub..." -ForegroundColor Yellow
Write-Host "Entrez vos identifiants Docker Hub:" -ForegroundColor Cyan
Write-Host ""

docker login

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Erreur lors du login" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "✅ Login réussi!" -ForegroundColor Green
Write-Host ""

# Push l'image
Write-Host "📤 Push de l'image sur Docker Hub..." -ForegroundColor Yellow
Write-Host "Cela peut prendre 5-10 minutes..." -ForegroundColor Cyan
Write-Host ""

docker push $ImageName

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Erreur lors du push" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "✅ Image pushée avec succès!" -ForegroundColor Green
Write-Host ""

# Résumé
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "✨ Déploiement terminé avec succès!" -ForegroundColor Green
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host ""
Write-Host "📝 Prochaines étapes:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Allez sur RunPod Console:" -ForegroundColor White
Write-Host "   https://www.runpod.io/console/serverless" -ForegroundColor Cyan
Write-Host ""
Write-Host "2. Créez un nouvel Endpoint avec:" -ForegroundColor White
Write-Host "   - Docker Image: $ImageName" -ForegroundColor Cyan
Write-Host "   - GPU: RTX 4090 (24GB)" -ForegroundColor Cyan
Write-Host "   - Workers Min: 0" -ForegroundColor Cyan
Write-Host "   - Workers Max: 1" -ForegroundColor Cyan
Write-Host "   - Container Disk: 30 GB" -ForegroundColor Cyan
Write-Host "   - Volume Disk: 50 GB" -ForegroundColor Cyan
Write-Host "   - Execution Timeout: 120s" -ForegroundColor Cyan
Write-Host ""
Write-Host "3. Copiez l'Endpoint ID" -ForegroundColor White
Write-Host ""
Write-Host "4. Mettez à jour .env.local:" -ForegroundColor White
Write-Host "   NEXT_PUBLIC_RUNPOD_ENDPOINT_URL=https://api.runpod.ai/v2/VOTRE_ID/runsync" -ForegroundColor Cyan
Write-Host ""
Write-Host "5. Redémarrez l'application:" -ForegroundColor White
Write-Host "   npm run dev" -ForegroundColor Cyan
Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host ""
Write-Host "🎉 Bon déploiement!" -ForegroundColor Green
Write-Host ""
