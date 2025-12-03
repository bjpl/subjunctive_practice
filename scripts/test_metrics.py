#!/usr/bin/env python3
"""
Test Metrics Tracker

This script analyzes test results and generates daily metrics for tracking
test health and progress over time.

Usage:
    python scripts/test_metrics.py [--output FILE]
"""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List


def run_tests_and_collect_metrics() -> Dict[str, Any]:
    """
    Run the test suite and collect comprehensive metrics.

    Returns:
        Dict containing test metrics
    """
    print("Running test suite...")

    # Run pytest with JSON output
    result = subprocess.run(
        [
            "python3", "-m", "pytest",
            "tests/",
            "--tb=no",
            "-q",
            "--no-cov",
            "-v",
            "--json-report",
            "--json-report-file=.test-report.json"
        ],
        capture_output=True,
        text=True
    )

    # Parse test output
    output_lines = result.stdout.split('\n')

    # Extract summary line
    summary_line = None
    for line in output_lines:
        if 'passed' in line or 'failed' in line:
            summary_line = line
            break

    # Parse summary
    metrics = {
        'timestamp': datetime.utcnow().isoformat(),
        'total_tests': 0,
        'passed': 0,
        'failed': 0,
        'skipped': 0,
        'errors': 0,
        'warnings': 0,
        'duration_seconds': 0.0,
        'pass_rate': 0.0,
        'exit_code': result.returncode
    }

    if summary_line:
        # Parse summary line
        import re

        # Extract counts
        passed_match = re.search(r'(\d+) passed', summary_line)
        failed_match = re.search(r'(\d+) failed', summary_line)
        skipped_match = re.search(r'(\d+) skipped', summary_line)
        warnings_match = re.search(r'(\d+) warnings', summary_line)

        if passed_match:
            metrics['passed'] = int(passed_match.group(1))
        if failed_match:
            metrics['failed'] = int(failed_match.group(1))
        if skipped_match:
            metrics['skipped'] = int(skipped_match.group(1))
        if warnings_match:
            metrics['warnings'] = int(warnings_match.group(1))

        # Calculate total
        metrics['total_tests'] = metrics['passed'] + metrics['failed'] + metrics['skipped']

        # Calculate pass rate
        if metrics['total_tests'] > 0:
            metrics['pass_rate'] = round(
                (metrics['passed'] / metrics['total_tests']) * 100, 2
            )

        # Extract duration
        duration_match = re.search(r'in ([\d.]+)s', summary_line)
        if duration_match:
            metrics['duration_seconds'] = float(duration_match.group(1))

    # Get failed test names
    failed_tests = []
    capturing_failures = False
    for line in output_lines:
        if 'FAILED' in line:
            # Extract test name
            test_match = re.search(r'FAILED (tests/[^\s]+)', line)
            if test_match:
                failed_tests.append(test_match.group(1))

    metrics['failed_tests'] = failed_tests

    return metrics


def save_metrics(metrics: Dict[str, Any], output_file: str = "test_metrics.json"):
    """Save metrics to JSON file."""
    output_path = Path(output_file)

    # Load existing metrics if file exists
    all_metrics = []
    if output_path.exists():
        with open(output_path, 'r') as f:
            all_metrics = json.load(f)

    # Append new metrics
    all_metrics.append(metrics)

    # Keep only last 30 days of metrics
    if len(all_metrics) > 30:
        all_metrics = all_metrics[-30:]

    # Save updated metrics
    with open(output_path, 'w') as f:
        json.dump(all_metrics, f, indent=2)

    print(f"\nMetrics saved to {output_file}")


def print_summary(metrics: Dict[str, Any]):
    """Print human-readable summary."""
    print("\n" + "="*60)
    print(" TEST METRICS SUMMARY")
    print("="*60)
    print(f"\nTimestamp: {metrics['timestamp']}")
    print(f"\nTotal Tests:  {metrics['total_tests']}")
    print(f"  Passed:     {metrics['passed']} ({metrics['pass_rate']:.1f}%)")
    print(f"  Failed:     {metrics['failed']}")
    print(f"  Skipped:    {metrics['skipped']}")
    print(f"\nWarnings:     {metrics['warnings']}")
    print(f"Duration:     {metrics['duration_seconds']:.2f}s")

    if metrics['failed'] > 0:
        print(f"\nFailed Tests ({metrics['failed']}):")
        for test in metrics['failed_tests'][:10]:  # Show first 10
            print(f"  - {test}")
        if len(metrics['failed_tests']) > 10:
            print(f"  ... and {len(metrics['failed_tests']) - 10} more")

    print("\n" + "="*60)

    # Status indicator
    if metrics['failed'] == 0:
        print("\nStatus: ALL TESTS PASSING!")
    elif metrics['pass_rate'] >= 90:
        print(f"\nStatus: Good ({metrics['pass_rate']:.1f}% passing)")
    elif metrics['pass_rate'] >= 75:
        print(f"\nStatus: Needs attention ({metrics['failed']} failing)")
    else:
        print(f"\nStatus: Critical ({metrics['failed']} failing)")

    print("="*60 + "\n")


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Track test metrics")
    parser.add_argument(
        '--output', '-o',
        default='test_metrics.json',
        help='Output file for metrics (default: test_metrics.json)'
    )
    parser.add_argument(
        '--no-save',
        action='store_true',
        help='Do not save metrics to file'
    )

    args = parser.parse_args()

    # Collect metrics
    metrics = run_tests_and_collect_metrics()

    # Print summary
    print_summary(metrics)

    # Save metrics
    if not args.no_save:
        save_metrics(metrics, args.output)

    # Exit with test result code
    sys.exit(metrics['exit_code'])


if __name__ == '__main__':
    main()
