@echo off
echo Fix Docker build error...
echo.

git add .
git commit -m "Fix: Correction erreur build Docker - separation installation deps"
git push origin main

echo.
echo ========================================
echo Fix pousse sur GitHub!
========================================
echo.
echo RunPod va rebuilder (5-10 min)
echo Le build devrait passer cette fois
echo.
pause
