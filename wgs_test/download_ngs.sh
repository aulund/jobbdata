#!/bin/bash

BASE_URL="https://data.macrogen-europe.com/~macroeu/hWGS/202603/EN00011332"

declare -A MD5SUMS=(
  ["ngs_test_01_R1.fastq.gz"]="1e4f88cbcbdc2346675af3c87c312469"
  ["ngs_test_01_R2.fastq.gz"]="d284db36afcdacc77f9f57a3edac77a7"
  ["ngs_test_01_sorted.bam"]="b6ab6bd1afd9552547d77ecadafc07aa"
  ["ngs_test_01_sorted.bam.bai"]="fa1ca7c5bd37e86cf54b3bb835938679"
  ["ngs_test_01_sorted.genome.vcf.gz"]="3a6acfd85ad63032813fac705bb3c794"
  ["ngs_test_01_sorted.genome.vcf.gz.tbi"]="6238552fb8f65b2f78e60011d6c9262b"
  ["260323_Somia-Echelhi_EN00011332_1sample.zip"]="321772aea116e7471737b8ff6fa3cc70"
  ["EN00011332_1samples_md5sum.xlsx"]="0fe9fe337096a314d0460cd728701599"
)

for FILE in "${!MD5SUMS[@]}"; do
  echo "Downloading $FILE..."
  wget -c "$BASE_URL/$FILE" -O "$FILE"

  echo "Verifying $FILE..."
  ACTUAL=$(md5sum "$FILE" | awk '{print $1}')
  EXPECTED="${MD5SUMS[$FILE]}"

  if [ "$ACTUAL" == "$EXPECTED" ]; then
    echo "✓ $FILE — checksum OK"
  else
    echo "✗ $FILE — CHECKSUM MISMATCH! Expected: $EXPECTED, Got: $ACTUAL"
  fi
  echo ""
done

echo "All done."