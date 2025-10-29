@echo off
echo Correction et push vers GitHub...
echo.

git add .
git commit --amend --no-edit
git push -u origin main --force

echo.
echo ========================================
echo Code pushe sur GitHub!
========================================
echo.
echo Repo: https://github.com/BillyBob36/qwen-tryon-handler
echo.
echo Prochaine etape: Creer l'endpoint sur RunPod
echo https://www.runpod.io/console/serverless
echo.
pause
