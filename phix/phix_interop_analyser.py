#!/usr/bin/env python3
"""
Script to extract PhiX alignment statistics from Illumina run folders using InterOp. 
This uses the built-in PhiX metrics that Illumina software generates during sequencing.
"""

import argparse
import sys
from pathlib import Path


def parse_interop_stats(run_folder):
    """
    Parse Illumina InterOp files to get PhiX alignment statistics.
    Requires: pip install interop
    """
    try:
        from interop import py_interop_run_metrics, py_interop_run, py_interop_summary
    except ImportError:
        print("Error: interop library not found.")
        print("Install with: pip install interop")
        sys.exit(1)
    
    run_folder_path = Path(run_folder)
    
    if not run_folder_path.exists():
        print(f"Error: Run folder not found: {run_folder}")
        sys.exit(1)
    
    # Check for InterOp directory
    interop_dir = run_folder_path / "InterOp"
    if not interop_dir.exists():
        print(f"Error: InterOp directory not found in {run_folder}")
        print("This doesn't appear to be a valid Illumina run folder.")
        sys.exit(1)
    
    try:
        # Initialize run metrics
        run_metrics = py_interop_run_metrics.run_metrics()
        
        # Specify which metrics to load
        valid_to_load = py_interop_run.uchar_vector(py_interop_run.MetricCount, 0)
        py_interop_run.list_summary_metrics_to_load(valid_to_load)
        
        # Read the run metrics
        run_metrics.read(str(run_folder_path), valid_to_load)
        
        # Generate summary
        summary = py_interop_summary.run_summary()
        py_interop_summary.summarize_run_metrics(run_metrics, summary)
        
        # Extract PhiX statistics
        results = {
            'run_folder': run_folder,
            'reads': [],
            'overall': {}
        }
        
        total_phix = 0
        total_error = 0
        lane_count = 0
        
        for read_idx in range(summary.size()):
            read_summary = summary.at(read_idx)
            read_data = {
                'read_number': read_idx + 1,
                'lanes': []
            }
            
            for lane_idx in range(read_summary.size()):
                lane_summary = read_summary.at(lane_idx)
                
                lane_data = {
                    'lane': lane_idx + 1,
                    'percent_aligned_phix': lane_summary.percent_aligned().mean(),
                    'error_rate': lane_summary.error_rate().mean(),
                    'density': lane_summary.density().mean() / 1000,  # K/mm²
                    'cluster_count': lane_summary.reads(),
                    'percent_pf': lane_summary.percent_pf().mean()
                }
                
                read_data['lanes'].append(lane_data)
                total_phix += lane_data['percent_aligned_phix']
                total_error += lane_data['error_rate']
                lane_count += 1
            
            results['reads'].append(read_data)
        
        if lane_count > 0:
            results['overall']['average_phix_aligned'] = total_phix / lane_count
            results['overall']['average_error_rate'] = total_error / lane_count
        
        return results
    
    except Exception as e: 
        print(f"Error parsing InterOp data: {e}")
        sys.exit(1)


def print_results(results, verbose=False):
    """Print formatted results."""
    print(f"\n{'='*70}")
    print(f"PhiX Analysis for: {results['run_folder']}")
    print(f"{'='*70}\n")
    
    # Overall summary
    if results['overall']:
        print("OVERALL SUMMARY:")
        print(f"  Average PhiX Aligned: {results['overall']['average_phix_aligned']:.2f}%")
        print(f"  Average Error Rate:    {results['overall']['average_error_rate']:.3f}%")
        print()
    
    # Per-read and per-lane details
    for read_data in results['reads']:
        print(f"READ {read_data['read_number']}:")
        print(f"  {'Lane':<6} {'PhiX %':<10} {'Error %':<10} {'Density':<12} {'Clusters':<15} {'%PF':<8}")
        print(f"  {'-'*65}")
        
        for lane in read_data['lanes']:
            print(f"  {lane['lane']:<6} "
                  f"{lane['percent_aligned_phix']:<10.2f} "
                  f"{lane['error_rate']:<10.3f} "
                  f"{lane['density']:<12.1f} "
                  f"{lane['cluster_count']:<15,} "
                  f"{lane['percent_pf']:<8.1f}")
        print()


def export_csv(results, output_file):
    """Export results to CSV file."""
    import csv
    
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['Read', 'Lane', 'PhiX_Percent', 'Error_Rate', 
                     'Density_K_per_mm2', 'Cluster_Count', 'Percent_PF']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for read_data in results['reads']:
            for lane in read_data['lanes']:
                writer.writerow({
                    'Read': read_data['read_number'],
                    'Lane': lane['lane'],
                    'PhiX_Percent': f"{lane['percent_aligned_phix']:.2f}",
                    'Error_Rate': f"{lane['error_rate']:.3f}",
                    'Density_K_per_mm2': f"{lane['density']:.1f}",
                    'Cluster_Count': lane['cluster_count'],
                    'Percent_PF': f"{lane['percent_pf']:.1f}"
                })
    
    print(f"Results exported to: {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description='Extract PhiX alignment statistics from Illumina run folders',
        epilog='Example: python phix_interop_analyser.py /path/to/run/folder'
    )
    parser.add_argument(
        'run_folder',
        nargs='?',
        help='Path to Illumina run folder (contains InterOp directory)'
    )
    parser.add_argument(
        '-o', '--output',
        help='Export results to CSV file'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Verbose output'
    )
    
    args = parser.parse_args()
    
    # If no run_folder provided, prompt the user
    run_folder = args.run_folder
    if not run_folder:
        print("No run folder specified.")
        run_folder = input("Please enter the path to the Illumina sequencing run folder: ").strip()
        
        # Handle empty input
        if not run_folder:
            print("Error: No path provided.")
            sys.exit(1)
    
    # Parse InterOp data
    results = parse_interop_stats(run_folder)
    
    # Print results
    print_results(results, verbose=args.verbose)
    
    # Export if requested
    if args.output:
        export_csv(results, args.output)


if __name__ == '__main__':
    main()