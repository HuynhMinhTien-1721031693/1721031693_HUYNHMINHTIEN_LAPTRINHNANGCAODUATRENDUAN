$ErrorActionPreference = "Stop"
$repoDir = "D:\HuynhMinhTien\LAP TRINH NANG CAO DUA TREN DU AN\PROJECT"
$logFile = Join-Path $repoDir ".automation\backup.log"

Set-Location $repoDir

$status = git status --porcelain
if ([string]::IsNullOrWhiteSpace(($status -join ""))) {
  Add-Content -Path $logFile -Value ("[{0}] No changes to backup" -f (Get-Date))
  exit 0
}

git add -A
try {
  git commit --trailer "Made-with: Cursor" -m ("Auto backup: {0}" -f (Get-Date -Format "yyyy-MM-dd HH:mm:ss")) | Out-Null
} catch {
  Add-Content -Path $logFile -Value ("[{0}] WARN: Commit skipped" -f (Get-Date))
}

git push -u origin main *>> $logFile
if ($LASTEXITCODE -ne 0) {
  Add-Content -Path $logFile -Value ("[{0}] ERROR: Push failed" -f (Get-Date))
  exit 1
}

Add-Content -Path $logFile -Value ("[{0}] Backup success" -f (Get-Date))
exit 0
