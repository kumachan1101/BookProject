# Dynamically find the source directory starting with "01_"
$srcDirObj = Get-ChildItem | Where-Object { $_.Name -like "01_*" } | Select-Object -First 1
if (-not $srcDirObj) {
    Write-Error "Source directory (01_...) not found."
    exit 1
}
$srcDir = $srcDirObj.FullName
Write-Host "Source Directory: $srcDir"

$destDir = "02_章別"
if (!(Test-Path $destDir)) { New-Item -ItemType Directory -Path $destDir | Out-Null }

$files = Get-ChildItem -Path $srcDir -Filter "*.md"
foreach ($file in $files) {
    try {
        $content = Get-Content -LiteralPath $file.FullName -Raw -Encoding UTF8
        
        # Application of Rules
        # Fix 1: Remove empty line between filename and code block
        $content = [regex]::Replace($content, '(\*\*ファイル名\*\*: [^\r\n]+)\r?\n\r?\n(```c)', { 
            param($match) 
            return $match.Groups[1].Value + "`r`n" + $match.Groups[2].Value 
        })
        
        $destName = $file.Name.Replace(".md", "_reviewed.md")
        $destPath = Join-Path -Path $destDir -ChildPath $destName
        
        [System.IO.File]::WriteAllText($destPath, $content, [System.Text.Encoding]::UTF8)
        Write-Host "Processed: $destName"
    }
    catch {
        Write-Error "Failed to process $($file.Name): $_"
    }
}
