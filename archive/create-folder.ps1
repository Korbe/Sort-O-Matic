$startDate = Get-Date "1996-01-01"
$endDate = Get-Date "2024-01-01"

$months = "Jän","Feb","Mär","Apr","Mai","Jun","Jul","Aug","Sep","Okt","Nov","Dez"

while ($startDate < $endDate) {
    $year = $startDate.Year
    $folderName = $year.ToString("D4")

    if (-not (Test-Path -Path $folderName -PathType Container)) {
        New-Item -ItemType Directory -Name $folderName
        Write-Host "Created folder: $folderName"
    } else {
        Write-Host "Skipped existing folder: $folderName"
    }

    Set-Location -Path $folderName

    for ($i = 0; $i -lt 12; $i++) {
        $num = ($i + 1).ToString("D2")
        $monthFolderName = "$num-$($months[$i])"

        if (-not (Test-Path -Path $monthFolderName -PathType Container)) {
            New-Item -ItemType Directory -Name $monthFolderName
            Write-Host "Created folder: $monthFolderName"
        } else {
            Write-Host "Skipped existing folder: $monthFolderName"
        }
    }

    Set-Location -Path ..
    $startDate = $startDate.AddYears(1)
}

Write-Host "Script finished."
Read-Host "Press Enter to exit."
