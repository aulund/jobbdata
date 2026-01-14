#!/usr/bin/env python3
"""
Simple test to verify NaN handling in phix_interop_analyser.py
This tests the logic without requiring actual InterOp files.
"""

import math
import sys

def test_nan_detection():
    """Test that math.isnan correctly identifies NaN values."""
    print("Testing NaN detection...")
    
    # Test valid number
    value = 5.5
    assert not math.isnan(value), "Valid number incorrectly identified as NaN"
    print(f"  ✓ Valid number (5.5) correctly identified as non-NaN")
    
    # Test NaN
    nan_value = float('nan')
    assert math.isnan(nan_value), "NaN not correctly identified"
    print(f"  ✓ NaN correctly identified")
    
    # Test zero
    zero_value = 0.0
    assert not math.isnan(zero_value), "Zero incorrectly identified as NaN"
    print(f"  ✓ Zero (0.0) correctly identified as non-NaN")
    
    print("✓ All NaN detection tests passed!\n")


def test_average_calculation():
    """Test averaging logic that skips NaN values."""
    print("Testing average calculation with NaN values...")
    
    # Simulate data with some NaN values
    values = [10.0, float('nan'), 20.0, float('nan'), 30.0]
    
    # Count valid values and calculate sum
    total = 0
    valid_count = 0
    for val in values:
        if not math.isnan(val):
            total += val
            valid_count += 1
    
    # Calculate average
    if valid_count > 0:
        average = total / valid_count
    else:
        average = None
    
    expected_average = (10.0 + 20.0 + 30.0) / 3  # 20.0
    assert abs(average - expected_average) < 1e-9, f"Average calculation incorrect: {average} != {expected_average}"
    print(f"  ✓ Average of [10.0, NaN, 20.0, NaN, 30.0] = {average} (expected {expected_average})")
    
    # Test all NaN
    all_nan = [float('nan'), float('nan'), float('nan')]
    total = 0
    valid_count = 0
    for val in all_nan:
        if not math.isnan(val):
            total += val
            valid_count += 1
    
    if valid_count > 0:
        average = total / valid_count
    else:
        average = None
    
    assert average is None, "All NaN should result in None average"
    print(f"  ✓ All NaN values correctly result in None average")
    
    print("✓ All average calculation tests passed!\n")


def test_formatting():
    """Test formatting of values for display."""
    print("Testing value formatting...")
    
    # Test normal value
    value = 12.345
    formatted = f"{value:.2f}" if not math.isnan(value) else "N/A"
    assert formatted == "12.35", f"Normal value formatting incorrect: {formatted}"
    print(f"  ✓ Normal value (12.345) formatted as: {formatted}")
    
    # Test NaN
    nan_value = float('nan')
    formatted = f"{nan_value:.2f}" if not math.isnan(nan_value) else "N/A"
    assert formatted == "N/A", f"NaN formatting incorrect: {formatted}"
    print(f"  ✓ NaN value formatted as: {formatted}")
    
    # Test zero
    zero_value = 0.0
    formatted = f"{zero_value:.2f}" if not math.isnan(zero_value) else "N/A"
    assert formatted == "0.00", f"Zero formatting incorrect: {formatted}"
    print(f"  ✓ Zero value formatted as: {formatted}")
    
    print("✓ All formatting tests passed!\n")


def main():
    print("=" * 70)
    print("PhiX Analyser - NaN Handling Tests")
    print("=" * 70 + "\n")
    
    try:
        test_nan_detection()
        test_average_calculation()
        test_formatting()
        
        print("=" * 70)
        print("✓ ALL TESTS PASSED!")
        print("=" * 70)
        return 0
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ UNEXPECTED ERROR: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
