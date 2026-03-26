$ErrorActionPreference = "Continue"
$repoDir = "D:\HuynhMinhTien\LAP TRINH NANG CAO DUA TREN DU AN\PROJECT"
$automationDir = Join-Path $repoDir ".automation"
$latestFile = Join-Path $automationDir "context-latest.json"
$historyFile = Join-Path $automationDir "context-history.jsonl"
$notesFile = Join-Path $automationDir "daily-notes.txt"
$logFile = Join-Path $automationDir "context.log"

Set-Location $repoDir

$timestamp = Get-Date
$dateKey = $timestamp.ToString("yyyy-MM-dd")

$branch = (git branch --show-current) 2>$null
if (-not $branch) { $branch = "main" }

$statusLines = @(git status --porcelain)
$changedFiles = @()
if ($statusLines.Count -gt 0) {
  $changedFiles = $statusLines | ForEach-Object {
    if ($_.Length -ge 4) { $_.Substring(3).Trim() }
  } | Where-Object { $_ -ne "" } | Sort-Object -Unique
}

$recentCommits = @()
$recentCommitsRaw = @(git log --since "1 day ago" --pretty=format:"%h|%an|%ad|%s" --date=iso-strict 2>$null)
if ($recentCommitsRaw.Count -gt 0) {
  $recentCommits = $recentCommitsRaw | ForEach-Object {
    $parts = $_ -split "\|", 4
    [PSCustomObject]@{
      hash = $parts[0]
      author = $parts[1]
      date = $parts[2]
      message = $parts[3]
    }
  }
}

$manualNotes = ""
if (Test-Path $notesFile) {
  $manualNotes = (Get-Content $notesFile -Raw)
}

$contextObj = [PSCustomObject]@{
  generatedAt = $timestamp.ToString("o")
  date = $dateKey
  repository = $repoDir
  branch = $branch
  workingTreeChanged = ($statusLines.Count -gt 0)
  changedFiles = $changedFiles
  commitsLast24h = $recentCommits
  manualNotes = $manualNotes.Trim()
}

$contextObj | ConvertTo-Json -Depth 8 | Set-Content -Path $latestFile -Encoding UTF8
($contextObj | ConvertTo-Json -Depth 8 -Compress) | Add-Content -Path $historyFile -Encoding UTF8

Add-Content -Path $logFile -Value ("[{0}] Context saved: {1}" -f (Get-Date), $latestFile)
exit 0
