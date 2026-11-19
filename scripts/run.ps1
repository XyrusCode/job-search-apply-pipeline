<#
.SYNOPSIS
  Job Search & Apply Pipeline runner / scheduler entry point.

.DESCRIPTION
  Default action: launch the configured AI CLI headless against prompts/daily-run.md, so it runs the
  full discover -> tailor -> apply -> log workflow defined in AGENTS.md. Honors the PAUSE kill switch.

  -Install    Register a Windows Task Scheduler job (weekdays 09:00 by default) that runs this script.
  -Uninstall  Remove that scheduled task.

.NOTES
  Set $CLI below to choose the driving CLI: 'claude', 'gemini' or 'opencode'. Other harnesses can be
  invoked directly with prompts/daily-run.md (see the entry-point files in the README).
  Auto-submit requires dryRun:false in config/preferences.json AND a configured browser / Gmail.
#>

[CmdletBinding()]
param(
  [switch]$Install,
  [switch]$Uninstall
)

# --- Configuration ---------------------------------------------------------
$CLI       = 'claude'                         # 'claude' | 'gemini' | 'opencode'
$TaskName  = 'JobPipeline-Daily'
$Cadence   = 'weekdays'                       # informational; schedule set in -Install below
$RunTime   = '09:00'

# --- Paths -----------------------------------------------------------------
$ProjectDir = Split-Path -Parent $PSScriptRoot
$PromptFile = Join-Path $ProjectDir 'prompts\daily-run.md'
$PauseFile  = Join-Path $ProjectDir 'PAUSE'
$EnvFile    = Join-Path $ProjectDir '.env'
$DataDir    = Join-Path $ProjectDir 'data'
$LogFile    = Join-Path $DataDir ('run-{0}.log' -f (Get-Date -Format 'yyyy-MM-dd'))

function Write-Log {
  param([string]$Message)
  $line = ('[{0}] {1}' -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'), $Message)
  Write-Host $line
  if (-not (Test-Path $DataDir)) { New-Item -ItemType Directory -Path $DataDir -Force | Out-Null }
  Add-Content -Path $LogFile -Value $line -Encoding utf8
}

# --- Install / Uninstall the scheduled task --------------------------------
if ($Install) {
  $pwshPath = (Get-Command pwsh -ErrorAction SilentlyContinue).Source
  if (-not $pwshPath) { $pwshPath = (Get-Command powershell).Source }
  $action  = New-ScheduledTaskAction -Execute $pwshPath `
             -Argument ('-NoProfile -ExecutionPolicy Bypass -File "{0}"' -f $PSCommandPath)
  $trigger = New-ScheduledTaskTrigger -Weekly `
             -DaysOfWeek Monday,Tuesday,Wednesday,Thursday,Friday `
             -At $RunTime
  $settings = New-ScheduledTaskSettingsSet -StartWhenAvailable `
              -DontStopOnIdleEnd -AllowStartIfOnBatteries
  Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger $trigger `
    -Settings $settings -Description 'Job Search & Apply Pipeline daily run' -Force | Out-Null
  Write-Host "Installed scheduled task '$TaskName' (weekdays at $RunTime)."
  return
}

if ($Uninstall) {
  Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false -ErrorAction SilentlyContinue
  Write-Host "Removed scheduled task '$TaskName' (if it existed)."
  return
}

# --- Kill switch -----------------------------------------------------------
if (Test-Path $PauseFile) {
  Write-Log 'PAUSE file present. Aborting run without applying.'
  return
}

# --- Load .env (KEY=VALUE lines) into the process env ----------------------
if (Test-Path $EnvFile) {
  Get-Content $EnvFile | ForEach-Object {
    $t = $_.Trim()
    if ($t -and -not $t.StartsWith('#') -and $t.Contains('=')) {
      $k, $v = $t.Split('=', 2)
      [Environment]::SetEnvironmentVariable($k.Trim(), $v.Trim(), 'Process')
    }
  }
}

if (-not (Test-Path $PromptFile)) { Write-Log "Prompt file missing: $PromptFile"; return }
$prompt = Get-Content $PromptFile -Raw

# --- Launch the CLI headless -----------------------------------------------
Write-Log "Starting pipeline via '$CLI'."
Push-Location $ProjectDir
try {
  # Headless runs need a flag to auto-approve tool use, otherwise they block on a permission prompt.
  # Attach the prompt file where the CLI supports it. Check each CLI's --help for current flag names.
  switch ($CLI) {
    'opencode' {
      $opencodeArgs = 'run --dangerously-skip-permissions --format json "Follow the attached daily-run.md instructions exactly." -f "{0}"' -f $PromptFile
      $tmpStdout = [System.IO.Path]::GetTempFileName()
      $tmpStderr = [System.IO.Path]::GetTempFileName()
      try {
        Start-Process -FilePath 'opencode' -NoNewWindow -Wait `
          -RedirectStandardOutput $tmpStdout -RedirectStandardError $tmpStderr `
          -ArgumentList $opencodeArgs
        Get-Content -Path $tmpStdout, $tmpStderr -Encoding utf8 | Add-Content -Path $LogFile -Encoding utf8
      } finally {
        Remove-Item -LiteralPath $tmpStdout, $tmpStderr -ErrorAction SilentlyContinue -Force
      }
    }
    'claude'   { & claude -p $prompt --dangerously-skip-permissions *>> $LogFile }
    'gemini'   { & gemini -p $prompt --yolo                         *>> $LogFile }
    default    { Write-Log "Unknown CLI '$CLI'. Set `$CLI to claude|gemini|opencode, or invoke prompts/daily-run.md directly with your harness." }
  }
}
catch { Write-Log ("Run failed: {0}" -f $_.Exception.Message) }
finally { Pop-Location }

Write-Log 'Run finished.'
