import gzip
from collections import Counter, defaultdict

vcf_file = r"H:\jobbdata\wgs_test\ngs_test_01_sorted.genome.vcf.gz"

print(f"Analyzing: {vcf_file}\n")

# Counters
total_variants = 0
variant_types = Counter()
chromosomes = Counter()
genotypes = Counter()
qualities = []
depths = []

with gzip.open(vcf_file, 'rt') as f:
    for line in f:
        if line.startswith('##'):
            continue
        
        if line.startswith('#CHROM'):
            header = line.strip().split('\t')
            print(f"Sample column: {header[9] if len(header) > 9 else 'N/A'}\n")
            continue
        
        total_variants += 1
        fields = line.strip().split('\t')
        
        chrom = fields[0]
        pos = fields[1]
        ref = fields[3]
        alt = fields[4]
        qual = fields[5]
        info = fields[7]
        
        # Chromosome
        chromosomes[chrom] += 1
        
        # Variant type
        if len(ref) == 1 and len(alt) == 1:
            variant_types['SNP'] += 1
        elif len(ref) != len(alt):
            variant_types['INDEL'] += 1
        else:
            variant_types['OTHER'] += 1
        
        # Quality
        if qual != '.':
            qualities.append(float(qual))
        
        # Depth from INFO field
        for item in info.split(';'):
            if item.startswith('DP='):
                depth = int(item.split('=')[1])
                depths.append(depth)
                break
        
        # Genotype (if available)
        if len(fields) > 9:
            fmt = fields[8].split(':')
            sample = fields[9].split(':')
            if 'GT' in fmt:
                gt_idx = fmt.index('GT')
                gt = sample[gt_idx]
                genotypes[gt] += 1

print("=" * 60)
print("VARIANT SUMMARY")
print("=" * 60)
print(f"Total variants: {total_variants:,}")
print()

print("Variant Types:")
for vtype, count in variant_types.most_common():
    print(f"  {vtype}: {count:,} ({count/total_variants*100:.1f}%)")
print()

print("Top 10 Chromosomes:")
for chrom, count in chromosomes.most_common(10):
    print(f"  {chrom}: {count:,} ({count/total_variants*100:.1f}%)")
print()

if genotypes:
    print("Genotypes:")
    for gt, count in genotypes.most_common():
        print(f"  {gt}: {count:,} ({count/total_variants*100:.1f}%)")
    print()

if qualities:
    print(f"Quality Scores:")
    print(f"  Min: {min(qualities):.1f}")
    print(f"  Max: {max(qualities):.1f}")
    print(f"  Mean: {sum(qualities)/len(qualities):.1f}")
    print()

if depths:
    print(f"Depth (DP):")
    print(f"  Min: {min(depths)}")
    print(f"  Max: {max(depths)}")
    print(f"  Mean: {sum(depths)/len(depths):.1f}")
    print()

print("=" * 60)
