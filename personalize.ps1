# Windows PowerShell version of personalize.sh
# Replace YOURNAME in every lab YAML with your own short name.
#
#   .\personalize.ps1 jsmith
#
# If PowerShell blocks the script, run once:  Set-ExecutionPolicy -Scope Process Bypass
param([Parameter(Mandatory = $true)][string]$Name)

if ($Name -cnotmatch '^[a-z][a-z0-9-]{0,19}$') {
    Write-Host "Use lowercase letters/digits/dashes, start with a letter, max 20 chars. e.g. .\personalize.ps1 jsmith"
    exit 1
}

Set-Location $PSScriptRoot
$count = 0
Get-ChildItem -Path labs -Recurse -Filter *.yaml | ForEach-Object {
    $text = Get-Content $_.FullName -Raw
    if ($text -match 'YOURNAME') {
        $text = $text -creplace 'YOURNAME', $Name
        # write UTF-8 without BOM so kubectl is happy
        [System.IO.File]::WriteAllText($_.FullName, $text, (New-Object System.Text.UTF8Encoding $false))
        $count++
    }
}
Write-Host "Updated $count YAML files for '$Name'."
Write-Host ""
Write-Host "Now set this in your terminal (used by the commands in the lab READMEs):"
Write-Host "  `$ME = `"$Name`""
