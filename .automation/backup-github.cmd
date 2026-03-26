@echo off
setlocal

set REPO_DIR=D:\HuynhMinhTien\LAP TRINH NANG CAO DUA TREN DU AN\PROJECT
set LOG_FILE=%REPO_DIR%\.automation\backup.log

cd /d "%REPO_DIR%"
if errorlevel 1 (
  echo [%date% %time%] ERROR: Cannot open repo dir >> "%LOG_FILE%"
  exit /b 1
)

for /f %%i in ('git status --porcelain') do (
  set HAS_CHANGES=1
  goto :do_backup
)

echo [%date% %time%] No changes to backup >> "%LOG_FILE%"
exit /b 0

:do_backup
git add -A
git commit --trailer "Made-with: Cursor" -m "Auto backup: %date% %time%" >nul 2>&1
if errorlevel 1 (
  echo [%date% %time%] WARN: Commit skipped (possibly no staged changes or missing git identity) >> "%LOG_FILE%"
)

git push -u origin main >> "%LOG_FILE%" 2>&1
if errorlevel 1 (
  echo [%date% %time%] ERROR: Push failed >> "%LOG_FILE%"
  exit /b 1
)

echo [%date% %time%] Backup success >> "%LOG_FILE%"
exit /b 0
