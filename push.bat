@echo off
echo Commit et push vers GitHub...
echo.

git add .
git commit -m "Initial commit: Qwen handler"
git push -u origin main

echo.
echo ========================================
echo Code pushe sur GitHub!
echo ========================================
echo.
echo Repo: https://github.com/BillyBob36/qwen-tryon-handler
echo.
echo Prochaine etape: Creer l'endpoint sur RunPod
echo https://www.runpod.io/console/serverless
echo.
pause
