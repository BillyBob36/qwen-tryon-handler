# Script pour commit et push vers GitHub
# Usage: .\commit-and-push.ps1

Write-Host "🚀 Commit et Push vers GitHub" -ForegroundColor Cyan
Write-Host ""

# Ajouter tous les fichiers
Write-Host "📦 Ajout des fichiers..." -ForegroundColor Yellow
git add .

# Créer le commit
Write-Host "💾 Création du commit..." -ForegroundColor Yellow
git commit -m "Initial commit"

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Erreur lors du commit" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Commit créé" -ForegroundColor Green
Write-Host ""

# Vérifier le remote
Write-Host "🔍 Vérification du remote..." -ForegroundColor Yellow
$remotes = git remote -v

if ($remotes -match "origin") {
    Write-Host "✅ Remote 'origin' configuré" -ForegroundColor Green
} else {
    Write-Host "⚠️  Ajout du remote..." -ForegroundColor Yellow
    git remote add origin https://github.com/BillyBob36/qwen-tryon-handler.git
    Write-Host "✅ Remote ajouté" -ForegroundColor Green
}

Write-Host ""

# Push vers GitHub
Write-Host "📤 Push vers GitHub..." -ForegroundColor Yellow
Write-Host "Cela peut prendre quelques secondes..." -ForegroundColor Cyan
Write-Host ""

git push -u origin main

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "❌ Erreur lors du push" -ForegroundColor Red
    Write-Host ""
    Write-Host "💡 Solutions possibles:" -ForegroundColor Yellow
    Write-Host "1. Vérifiez votre connexion internet" -ForegroundColor White
    Write-Host "2. Vérifiez que le repo existe: https://github.com/BillyBob36/qwen-tryon-handler" -ForegroundColor White
    Write-Host "3. Authentifiez-vous avec: gh auth login" -ForegroundColor White
    exit 1
}

Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "✅ Code pushé avec succès sur GitHub!" -ForegroundColor Green
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host ""
Write-Host "🔗 Votre repo:" -ForegroundColor Yellow
Write-Host "   https://github.com/BillyBob36/qwen-tryon-handler" -ForegroundColor Cyan
Write-Host ""
Write-Host "📝 Prochaines étapes:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Créez l'endpoint sur RunPod:" -ForegroundColor White
Write-Host "   https://www.runpod.io/console/serverless" -ForegroundColor Cyan
Write-Host ""
Write-Host "2. Sélectionnez 'Import from GitHub'" -ForegroundColor White
Write-Host ""
Write-Host "3. Choisissez: BillyBob36/qwen-tryon-handler" -ForegroundColor White
Write-Host ""
Write-Host "4. Configuration:" -ForegroundColor White
Write-Host "   - GPU: RTX 4090 (24GB)" -ForegroundColor Cyan
Write-Host "   - Workers Min: 0" -ForegroundColor Cyan
Write-Host "   - Workers Max: 1" -ForegroundColor Cyan
Write-Host "   - Container Disk: 30 GB" -ForegroundColor Cyan
Write-Host "   - Volume Disk: 50 GB" -ForegroundColor Cyan
Write-Host "   - Execution Timeout: 120s" -ForegroundColor Cyan
Write-Host ""
Write-Host "5. Copiez l'Endpoint ID dans .env.local" -ForegroundColor White
Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host ""
Write-Host "🎉 Prêt pour le déploiement RunPod!" -ForegroundColor Green
Write-Host ""
