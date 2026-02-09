$badDir = Get-ChildItem | Where-Object { $_.Name -like "02_遶*" } | Select -First 1
if ($badDir) {
    Write-Host "Found garbled dir: $($badDir.Name)"
    Get-ChildItem $badDir.FullName | Move-Item -Destination "02_章別" -Force
    Remove-Item $badDir.FullName -Recurse -Force
    Write-Host "Moved files and removed garbled dir."
} else {
    Write-Host "No garbled dir found."
}
