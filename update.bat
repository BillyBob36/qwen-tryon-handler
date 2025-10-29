@echo off
echo Mise a jour du handler sur GitHub...
echo.

git add .
git commit -m "Fix: Handler simplifie sans Qwen pour eviter throttling"
git push origin main

echo.
echo ========================================
echo Mise a jour pushee sur GitHub!
========================================
echo.
echo RunPod va automatiquement rebuilder l'endpoint
echo Attendez 2-3 minutes pour le nouveau build
echo.
pause
