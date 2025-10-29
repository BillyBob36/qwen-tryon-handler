@echo off
echo Mise a jour avec Qwen-Image-Edit-2509...
echo.

git add .
git commit -m "Integration Qwen-Image-Edit-2509 pour virtual try-on"
git push origin main

echo.
echo ========================================
echo Code pousse sur GitHub!
========================================
echo.
echo RunPod va rebuilder automatiquement (5-10 min)
echo Le modele Qwen-Image-Edit sera telecharge au premier demarrage
echo.
pause
