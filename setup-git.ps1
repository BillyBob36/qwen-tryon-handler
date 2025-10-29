# Script de setup Git pour le handler Qwen-Image-Edit
# Usage: .\setup-git.ps1

Write-Host "🔧 Configuration Git pour le handler Qwen-Image-Edit" -ForegroundColor Cyan
Write-Host ""

# Vérifier si Git est installé
try {
    git --version | Out-Null
    Write-Host "✅ Git est installé" -ForegroundColor Green
} catch {
    Write-Host "❌ Git n'est pas installé" -ForegroundColor Red
    Write-Host "Téléchargez Git: https://git-scm.com/download/win" -ForegroundColor Yellow
    exit 1
}

Write-Host ""

# Configurer Git (si pas déjà fait)
Write-Host "📝 Configuration de Git..." -ForegroundColor Yellow

$gitEmail = git config --global user.email
$gitName = git config --global user.name

if (-not $gitEmail) {
    Write-Host "Entrez votre email Git:" -ForegroundColor Cyan
    $email = Read-Host
    git config --global user.email $email
    Write-Host "✅ Email configuré" -ForegroundColor Green
} else {
    Write-Host "✅ Email déjà configuré: $gitEmail" -ForegroundColor Green
}

if (-not $gitName) {
    Write-Host "Entrez votre nom Git:" -ForegroundColor Cyan
    $name = Read-Host
    git config --global user.name $name
    Write-Host "✅ Nom configuré" -ForegroundColor Green
} else {
    Write-Host "✅ Nom déjà configuré: $gitName" -ForegroundColor Green
}

Write-Host ""

# Vérifier si déjà initialisé
if (Test-Path ".git") {
    Write-Host "✅ Repo Git déjà initialisé" -ForegroundColor Green
} else {
    Write-Host "🔨 Initialisation du repo Git..." -ForegroundColor Yellow
    git init
    Write-Host "✅ Repo initialisé" -ForegroundColor Green
}

Write-Host ""

# Ajouter les fichiers
Write-Host "📦 Ajout des fichiers..." -ForegroundColor Yellow
git add .
Write-Host "✅ Fichiers ajoutés" -ForegroundColor Green

Write-Host ""

# Commit
Write-Host "💾 Création du commit initial..." -ForegroundColor Yellow
git commit -m "Initial commit: Qwen-Image-Edit handler"
Write-Host "✅ Commit créé" -ForegroundColor Green

Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "✨ Setup Git terminé!" -ForegroundColor Green
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host ""
Write-Host "📝 Prochaines étapes:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Créez un repo sur GitHub:" -ForegroundColor White
Write-Host "   https://github.com/new" -ForegroundColor Cyan
Write-Host "   Nom suggéré: qwen-tryon-handler" -ForegroundColor Cyan
Write-Host ""
Write-Host "2. Ajoutez le remote (remplacez VOTRE_USERNAME):" -ForegroundColor White
Write-Host "   git remote add origin https://github.com/VOTRE_USERNAME/qwen-tryon-handler.git" -ForegroundColor Cyan
Write-Host ""
Write-Host "3. Créez la branche main:" -ForegroundColor White
Write-Host "   git branch -M main" -ForegroundColor Cyan
Write-Host ""
Write-Host "4. Pushez le code:" -ForegroundColor White
Write-Host "   git push -u origin main" -ForegroundColor Cyan
Write-Host ""
Write-Host "5. Créez l'endpoint sur RunPod:" -ForegroundColor White
Write-Host "   - Allez sur: https://www.runpod.io/console/serverless" -ForegroundColor Cyan
Write-Host "   - Sélectionnez 'Import from GitHub'" -ForegroundColor Cyan
Write-Host "   - Choisissez votre repo" -ForegroundColor Cyan
Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host ""
