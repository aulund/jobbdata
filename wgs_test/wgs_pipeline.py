"""
WGS Variant Analysis Pipeline
==============================
Step 1: Filter VCF → keep only non-ref, PASS variants
Step 2: Annotate with SnpEff (functional impact)
Step 3: Rank by clinical relevance
Step 4: Output top variants as CSV

Usage: py wgs_pipeline.py [--step N] [--all]
"""

import gzip
import csv
import os
import sys
import subprocess
import argparse
from collections import Counter

BASE_DIR = r"H:\jobbdata\wgs_test"
INPUT_VCF = os.path.join(BASE_DIR, "ngs_test_01_sorted.genome.vcf.gz")
FILTERED_VCF = os.path.join(BASE_DIR, "filtered_variants.vcf")
ANNOTATED_VCF = os.path.join(BASE_DIR, "annotated_variants.vcf")
OUTPUT_CSV = os.path.join(BASE_DIR, "ranked_variants.csv")
SNPEFF_DIR = os.path.join(BASE_DIR, "snpEff")
SNPEFF_JAR = os.path.join(SNPEFF_DIR, "snpEff.jar")


# =============================================================================
# STEP 1: Filter VCF - remove ref calls, low quality, non-PASS
# =============================================================================
def step1_filter(min_qual=20, min_dp=10, pass_only=False):
    """Filter VCF to non-ref, quality variants."""
    print("=" * 60)
    print("STEP 1: Filtering VCF")
    print(f"  Min QUAL: {min_qual}")
    print(f"  Min DP: {min_dp}")
    print(f"  PASS only: {pass_only}")
    print("=" * 60)

    skip_gt = {'0/0', '0|0', '.', './.', '.|.', '0'}
    kept = 0
    skipped = 0
    total = 0

    with gzip.open(INPUT_VCF, 'rt') as fin, open(FILTERED_VCF, 'w') as fout:
        for line in fin:
            if line.startswith('#'):
                fout.write(line)
                continue

            total += 1
            if total % 2_000_000 == 0:
                print(f"  Processed {total:,} lines, kept {kept:,}...")

            fields = line.split('\t')
            alt = fields[4]
            qual_str = fields[5]
            filt = fields[6]
            info = fields[7]

            # Skip ref-only
            if alt == '.':
                skipped += 1
                continue

            # Genotype filter
            fmt = fields[8].split(':')
            sample = fields[9].split(':')
            gt_idx = fmt.index('GT')
            gt = sample[gt_idx]
            if gt in skip_gt:
                skipped += 1
                continue

            # Quality filter
            qual = float(qual_str) if qual_str != '.' else 0.0
            if qual < min_qual:
                skipped += 1
                continue

            # PASS filter
            if pass_only and filt != 'PASS':
                skipped += 1
                continue

            # Depth filter
            dp = 0
            for item in info.split(';'):
                if item.startswith('DP='):
                    dp = int(item.split('=')[1])
                    break
            if dp > 0 and dp < min_dp:
                skipped += 1
                continue

            fout.write(line)
            kept += 1

    print(f"\n  Total lines: {total:,}")
    print(f"  Kept: {kept:,}")
    print(f"  Skipped: {skipped:,}")
    print(f"  Output: {FILTERED_VCF}")
    return kept


# =============================================================================
# STEP 2: Check/Download SnpEff and annotate
# =============================================================================
def step2_check_snpeff():
    """Check if SnpEff is available, provide download instructions."""
    print("\n" + "=" * 60)
    print("STEP 2: Variant Annotation with SnpEff")
    print("=" * 60)

    # Check for Java
    try:
        result = subprocess.run(['java', '-version'], capture_output=True, text=True)
        print(f"  Java found: OK")
    except FileNotFoundError:
        print("  ERROR: Java not found. Install Java JRE/JDK first.")
        print("  Download: https://adoptium.net/")
        return False

    if os.path.exists(SNPEFF_JAR):
        print(f"  SnpEff found at: {SNPEFF_JAR}")
        return True
    else:
        print(f"  SnpEff not found at: {SNPEFF_JAR}")
        print(f"\n  To download SnpEff:")
        print(f"  1. Download from: https://snpeff.blob.core.windows.net/versions/snpEff_latest_core.zip")
        print(f"  2. Extract to: {SNPEFF_DIR}")
        print(f"  3. Re-run this step")
        return False


def step2_annotate():
    """Run SnpEff annotation on filtered VCF."""
    if not step2_check_snpeff():
        print("\n  Skipping annotation. Running Step 3 without annotation...")
        return False

    print("  Running SnpEff annotation...")
    cmd = [
        'java', '-Xmx4g', '-jar', SNPEFF_JAR,
        'GRCh38.105',  # Human genome build
        '-csvStats', os.path.join(BASE_DIR, 'snpeff_stats.csv'),
        FILTERED_VCF
    ]

    with open(ANNOTATED_VCF, 'w') as fout:
        result = subprocess.run(cmd, stdout=fout, stderr=subprocess.PIPE, text=True)

    if result.returncode == 0:
        print(f"  Annotated VCF: {ANNOTATED_VCF}")
        return True
    else:
        print(f"  SnpEff error: {result.stderr[:500]}")
        return False


# =============================================================================
# STEP 3: Rank variants
# =============================================================================
# Impact severity scores
IMPACT_SCORE = {
    'HIGH': 4,        # Stop gained, frameshift, splice donor/acceptor
    'MODERATE': 3,    # Missense, in-frame indel
    'LOW': 2,         # Synonymous, splice region
    'MODIFIER': 1,    # Intergenic, intronic, UTR
}

# Variant type scores (when no annotation available)
VARTYPE_SCORE = {
    'frameshift': 10,
    'stopgain': 10,
    'stoploss': 8,
    'splicing': 8,
    'nonsynonymous': 6,
    'indel_coding': 5,
    'synonymous': 2,
    'intronic': 1,
    'intergenic': 0,
}


def classify_variant_simple(ref, alt):
    """Simple classification without annotation."""
    ref_len = len(ref)
    alt_len = len(alt)

    if ref_len == 1 and alt_len == 1:
        return 'SNP'
    elif ref_len > alt_len:
        return 'DEL'
    elif ref_len < alt_len:
        return 'INS'
    else:
        return 'MNV'


def calculate_rank_score(qual, gt, dp, filt, vtype, ann_impact=None):
    """Calculate a composite rank score."""
    score = 0.0

    # Quality component (0-30 points)
    if qual != '.':
        q = float(qual)
        score += min(q / 100.0, 30.0)

    # Genotype component (0-10 points)
    # Homozygous alt more impactful for recessive diseases
    if gt in ('1/1', '1|1'):
        score += 10
    elif gt in ('0/1', '0|1', '1|0'):
        score += 5
    elif '/' in gt or '|' in gt:
        score += 3

    # Filter component (0-10 points)
    if filt == 'PASS':
        score += 10
    elif filt == '.':
        score += 5

    # Depth component (0-10 points)
    if dp > 0:
        score += min(dp / 3.0, 10.0)

    # Variant type component (0-10 points)
    if vtype in ('DEL', 'INS', 'MNV'):
        score += 8  # Indels more likely functional
    else:
        score += 4  # SNPs

    # Annotation impact (0-40 points) - biggest contributor
    if ann_impact:
        score += IMPACT_SCORE.get(ann_impact, 0) * 10

    return round(score, 2)


def parse_snpeff_ann(info):
    """Parse SnpEff ANN field from INFO."""
    for field in info.split(';'):
        if field.startswith('ANN='):
            ann = field[4:]
            # First annotation is highest impact
            parts = ann.split('|')
            if len(parts) >= 4:
                return {
                    'allele': parts[0],
                    'effect': parts[1],
                    'impact': parts[2],
                    'gene': parts[3],
                    'gene_id': parts[4] if len(parts) > 4 else '',
                    'feature_type': parts[5] if len(parts) > 5 else '',
                    'feature_id': parts[6] if len(parts) > 6 else '',
                    'hgvs_c': parts[9] if len(parts) > 9 else '',
                    'hgvs_p': parts[10] if len(parts) > 10 else '',
                }
    return None


def step3_rank(top_n=500):
    """Rank variants and output CSV."""
    print("\n" + "=" * 60)
    print(f"STEP 3: Ranking variants (top {top_n})")
    print("=" * 60)

    # Determine input file
    if os.path.exists(ANNOTATED_VCF):
        input_file = ANNOTATED_VCF
        has_annotation = True
        print(f"  Using annotated VCF: {input_file}")
    elif os.path.exists(FILTERED_VCF):
        input_file = FILTERED_VCF
        has_annotation = False
        print(f"  Using filtered VCF (no annotation): {input_file}")
    else:
        print("  ERROR: No filtered VCF found. Run step 1 first.")
        return

    import heapq
    heap = []
    count = 0

    with open(input_file, 'r') as f:
        for line in f:
            if line.startswith('#'):
                continue

            count += 1
            if count % 500_000 == 0:
                print(f"  Ranked {count:,} variants...")

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

            gt = sample[fmt.index('GT')]
            qual = float(qual_str) if qual_str != '.' else 0.0

            # Depth
            dp = 0
            for item in info.split(';'):
                if item.startswith('DP='):
                    dp = int(item.split('=')[1])
                    break

            vtype = classify_variant_simple(ref, alt)

            # Parse annotation if available
            ann = None
            ann_impact = None
            gene = ''
            effect = ''
            hgvs_p = ''
            if has_annotation:
                ann = parse_snpeff_ann(info)
                if ann:
                    ann_impact = ann.get('impact')
                    gene = ann.get('gene', '')
                    effect = ann.get('effect', '')
                    hgvs_p = ann.get('hgvs_p', '')

            rank_score = calculate_rank_score(qual, gt, dp, filt, vtype, ann_impact)

            entry = (rank_score, count, chrom, pos, ref, alt, gt, qual,
                     dp, filt, vtype, gene, effect, hgvs_p, ann_impact or '')

            if len(heap) < top_n:
                heapq.heappush(heap, entry)
            elif rank_score > heap[0][0]:
                heapq.heapreplace(heap, entry)

    results = sorted(heap, key=lambda x: -x[0])

    # Write CSV
    print(f"\n  Writing {len(results)} ranked variants to CSV...")
    with open(OUTPUT_CSV, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Rank', 'Score', 'Chr', 'Pos', 'Ref', 'Alt', 'Type',
                        'GT', 'QUAL', 'DP', 'Filter', 'Gene', 'Effect',
                        'HGVS_p', 'Impact'])
        for i, entry in enumerate(results, 1):
            score, _, chrom, pos, ref, alt, gt, qual, dp, filt, vtype, gene, effect, hgvs_p, impact = entry
            writer.writerow([i, score, chrom, pos, ref, alt, vtype, gt, qual,
                           dp, filt, gene, effect, hgvs_p, impact])

    print(f"  Output: {OUTPUT_CSV}")

    # Print top 20
    print(f"\n  Top 20 variants:")
    print(f"  {'Rank':<5} {'Score':<7} {'Chr':<5} {'Pos':<12} {'Ref':<6} {'Alt':<6} {'Type':<5} {'GT':<6} {'QUAL':<8} {'DP':<6} {'Filter':<10} {'Gene':<12} {'Impact'}")
    print("  " + "-" * 110)
    for i, entry in enumerate(results[:20], 1):
        score, _, chrom, pos, ref, alt, gt, qual, dp, filt, vtype, gene, effect, hgvs_p, impact = entry
        ref_d = ref[:5] + '..' if len(ref) > 5 else ref
        alt_d = alt[:5] + '..' if len(alt) > 5 else alt
        print(f"  {i:<5} {score:<7} {chrom:<5} {pos:<12} {ref_d:<6} {alt_d:<6} {vtype:<5} {gt:<6} {qual:<8.0f} {dp:<6} {filt:<10} {gene:<12} {impact}")

    return results


# =============================================================================
# STEP 4: Summary statistics on ranked variants
# =============================================================================
def step4_summary():
    """Print summary of ranked variants from CSV."""
    print("\n" + "=" * 60)
    print("STEP 4: Summary of ranked variants")
    print("=" * 60)

    if not os.path.exists(OUTPUT_CSV):
        print("  No ranked CSV found. Run steps 1-3 first.")
        return

    chroms = Counter()
    types = Counter()
    gts = Counter()
    filters = Counter()
    genes = Counter()
    impacts = Counter()

    with open(OUTPUT_CSV, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    for row in rows:
        chroms[row['Chr']] += 1
        types[row['Type']] += 1
        gts[row['GT']] += 1
        filters[row['Filter']] += 1
        if row.get('Gene'):
            genes[row['Gene']] += 1
        if row.get('Impact'):
            impacts[row['Impact']] += 1

    print(f"\n  Total ranked variants: {len(rows)}")
    print(f"\n  By chromosome: {dict(chroms.most_common(10))}")
    print(f"  By type: {dict(types)}")
    print(f"  By genotype: {dict(gts)}")
    print(f"  By filter: {dict(filters)}")
    if genes:
        print(f"  Top genes: {dict(genes.most_common(20))}")
    if impacts:
        print(f"  By impact: {dict(impacts)}")


# =============================================================================
# Main
# =============================================================================
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='WGS Variant Analysis Pipeline')
    parser.add_argument('--step', type=int, help='Run specific step (1-4)')
    parser.add_argument('--all', action='store_true', help='Run all steps')
    parser.add_argument('--min-qual', type=float, default=20, help='Min QUAL score (step 1)')
    parser.add_argument('--min-dp', type=int, default=10, help='Min depth (step 1)')
    parser.add_argument('--pass-only', action='store_true', help='Keep only PASS variants (step 1)')
    parser.add_argument('--top', type=int, default=500, help='Number of top variants (step 3)')
    args = parser.parse_args()

    if args.all or args.step is None:
        step1_filter(args.min_qual, args.min_dp, args.pass_only)
        step2_annotate()
        step3_rank(args.top)
        step4_summary()
    elif args.step == 1:
        step1_filter(args.min_qual, args.min_dp, args.pass_only)
    elif args.step == 2:
        step2_annotate()
    elif args.step == 3:
        step3_rank(args.top)
    elif args.step == 4:
        step4_summary()
    else:
        print(f"Unknown step: {args.step}")

    print("\nDone!")
