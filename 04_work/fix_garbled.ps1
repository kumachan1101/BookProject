$target = "02_章別"
if (!(Test-Path $target)) { New-Item -ItemType Directory -Path $target }

$dirs = Get-ChildItem -Directory | Where-Object { $_.Name -like "02_*" -and $_.Name -ne "02_章別" }
foreach ($d in $dirs) {
    Write-Host "Found anomalous directory: $($d.Name)"
    $files = Get-ChildItem $d.FullName
    foreach ($f in $files) {
         $dest = Join-Path $target $f.Name
         if (!(Test-Path $dest)) {
             Move-Item $f.FullName $dest
             Write-Host "Moved $($f.Name)"
         } else {
             # File exists. Keep the larger one.
             $srcSize = $f.Length
             $dstSize = (Get-Item $dest).Length
             
             if ($srcSize -gt $dstSize) {
                 Move-Item $f.FullName $dest -Force
                 Write-Host "Overwrote $($f.Name) (larger version: $srcSize > $dstSize)"
             } else {
                 # If source is same size or smaller, likely identical or worse.
                 # But if source is same size, we can delete source (implied by directory removal later)
                 Write-Host "Skipped $($f.Name) (target is larger/same: $dstSize >= $srcSize)"
             }
         }
    }
    Remove-Item $d.FullName -Recurse -Force
    Write-Host "Removed directory $($d.Name)"
}
Write-Host "Cleanup complete."
