$srcDir = "01_原稿"
$destDir = "02_章別"
if (!(Test-Path $destDir)) { New-Item -ItemType Directory -Path $destDir | Out-Null }

$files = Get-ChildItem -Path $srcDir -Filter "*.md"
foreach ($file in $files) {
    Write-Host "Processing $($file.Name)..."
    try {
        $content = Get-Content -LiteralPath $file.FullName -Raw -Encoding UTF8
        
        # Fix 1: Remove empty line between filename and code block
        # Pattern: **ファイル名**: ... followed by empty line then ```c
        $content = [regex]::Replace($content, '(\*\*ファイル名\*\*: [^\r\n]+)\r?\n\r?\n(```c)', { 
            param($match) 
            return $match.Groups[1].Value + "`r`n" + $match.Groups[2].Value 
        })
        
        $destName = $file.Name.Replace(".md", "_reviewed.md")
        $destPath = Join-Path -Path $destDir -ChildPath $destName
        
        [System.IO.File]::WriteAllText($destPath, $content, [System.Text.Encoding]::UTF8)
    }
    catch {
        Write-Error "Failed to process $($file.Name): $_"
    }
}
