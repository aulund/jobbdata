$BASE_URL = "https://data.macrogen-europe.com/~macroeu/hWGS/202603/EN00011332"

$MD5SUMS = @{
  "ngs_test_01_R1.fastq.gz" = "1e4f88cbcbdc2346675af3c87c312469"
  "ngs_test_01_R2.fastq.gz" = "d284db36afcdacc77f9f57a3edac77a7"
  "ngs_test_01_sorted.bam" = "b6ab6bd1afd9552547d77ecadafc07aa"
  "ngs_test_01_sorted.bam.bai" = "fa1ca7c5bd37e86cf54b3bb835938679"
  "ngs_test_01_sorted.genome.vcf.gz" = "3a6acfd85ad63032813fac705bb3c794"
  "ngs_test_01_sorted.genome.vcf.gz.tbi" = "6238552fb8f65b2f78e60011d6c9262b"
  "260323_Somia-Echelhi_EN00011332_1sample.zip" = "321772aea116e7471737b8ff6fa3cc70"
  "EN00011332_1samples_md5sum.xlsx" = "0fe9fe337096a314d0460cd728701599"
}

foreach ($FILE in $MD5SUMS.Keys) {
  Write-Host "Downloading $FILE..." -ForegroundColor Cyan
  
  # Download file
  $url = "$BASE_URL/$FILE"
  $output = Join-Path $PSScriptRoot $FILE
  
  try {
    Invoke-WebRequest -Uri $url -OutFile $output -UseBasicParsing
    
    # Verify MD5
    Write-Host "Verifying $FILE..." -ForegroundColor Yellow
    $hash = Get-FileHash -Path $output -Algorithm MD5
    $actual = $hash.Hash.ToLower()
    $expected = $MD5SUMS[$FILE]
    
    if ($actual -eq $expected) {
      Write-Host "OK: $FILE - checksum OK" -ForegroundColor Green
    } else {
      Write-Host "ERROR: $FILE - CHECKSUM MISMATCH! Expected: $expected, Got: $actual" -ForegroundColor Red
    }
  }
  catch {
    Write-Host "ERROR: Failed to download $FILE - $($_.Exception.Message)" -ForegroundColor Red
  }
  
  Write-Host ""
}

Write-Host "All done." -ForegroundColor Green
