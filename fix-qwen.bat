@echo off
echo Correction Qwen-Image-Edit avec QwenImageEditPlusPipeline...
echo.

git add .
git commit -m "Fix: Utilisation de QwenImageEditPlusPipeline et diffusers dev"
git push origin main

echo.
echo ========================================
echo Correction poussee sur GitHub!
========================================
echo.
echo RunPod va rebuilder (5-10 min)
echo Cette fois avec la bonne pipeline Qwen
echo.
pause
