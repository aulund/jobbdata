import gzip
import heapq

vcf_file = r"H:\jobbdata\wgs_test\ngs_test_01_sorted.genome.vcf.gz"

print(f"Finding top 100 ranked variants from: {vcf_file}\n")
print("Filtering: non-reference genotypes only (excluding 0/0, ./., .)\n")

# Use a min-heap of size 100 to track top variants by QUAL
top_n = 100
heap = []  # (qual, line_data_tuple)
count = 0

with gzip.open(vcf_file, 'rt') as f:
    for line in f:
        if line.startswith('#'):
            if line.startswith('#CHROM'):
                header = line.strip().split('\t')
            continue

        fields = line.strip().split('\t')
        chrom = fields[0]
        pos = fields[1]
        ref = fields[3]
        alt = fields[4]
        qual_str = fields[5]
        filt = fields[6]
        info = fields[7]
        fmt = fields[8].split(':')
        sample = fields[9].split(':')

        # Skip if no alt allele
        if alt == '.':
            continue

        # Get genotype
        gt_idx = fmt.index('GT')
        gt = sample[gt_idx]

        # Skip hom-ref and missing
        if gt in ('0/0', '0|0', '.', './.', '.|.', '0'):
            continue

        # Quality
        if qual_str == '.':
            qual = 0.0
        else:
            qual = float(qual_str)

        # Depth
        dp = '.'
        for item in info.split(';'):
            if item.startswith('DP='):
                dp = item.split('=')[1]
                break

        # Variant type
        if len(ref) == 1 and len(alt) == 1:
            vtype = 'SNP'
        elif len(ref) < len(alt):
            vtype = 'INS'
        elif len(ref) > len(alt):
            vtype = 'DEL'
        else:
            vtype = 'MNV'

        entry = (qual, count, chrom, pos, ref, alt, gt, dp, filt, vtype)
        count += 1

        if len(heap) < top_n:
            heapq.heappush(heap, entry)
        elif qual > heap[0][0]:
            heapq.heapreplace(heap, entry)

# Sort descending by quality
results = sorted(heap, key=lambda x: -x[0])

print(f"Total non-ref variants scanned: {count:,}\n")
print(f"{'Rank':<5} {'Chr':<5} {'Pos':<12} {'Ref':<8} {'Alt':<8} {'Type':<5} {'GT':<6} {'QUAL':<10} {'DP':<8} {'Filter'}")
print("-" * 90)

for i, (qual, _, chrom, pos, ref, alt, gt, dp, filt, vtype) in enumerate(results, 1):
    # Truncate long ref/alt
    ref_disp = ref[:6] + '..' if len(ref) > 6 else ref
    alt_disp = alt[:6] + '..' if len(alt) > 6 else alt
    print(f"{i:<5} {chrom:<5} {pos:<12} {ref_disp:<8} {alt_disp:<8} {vtype:<5} {gt:<6} {qual:<10.1f} {dp:<8} {filt}")
