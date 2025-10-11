#!/usr/bin/env python
"""
Test Runner Script

Provides convenient ways to run different test suites:
- All tests
- Unit tests only
- Integration tests only
- API tests only
- Tests by marker
- Coverage reports
"""

import sys
import subprocess
from pathlib import Path
from typing import List, Optional


class TestRunner:
    """Test runner with various configuration options."""

    def __init__(self):
        self.backend_dir = Path(__file__).parent.parent
        self.tests_dir = Path(__file__).parent

    def run_pytest(
        self,
        args: List[str],
        description: str,
        show_output: bool = True
    ) -> int:
        """Run pytest with given arguments."""
        print(f"\n{'='*70}")
        print(f"Running: {description}")
        print(f"{'='*70}\n")

        cmd = ["pytest"] + args

        if show_output:
            print(f"Command: {' '.join(cmd)}\n")

        result = subprocess.run(
            cmd,
            cwd=str(self.backend_dir)
        )

        return result.returncode

    def run_all_tests(self, verbose: bool = False) -> int:
        """Run all tests with coverage."""
        args = []
        if verbose:
            args.append("-vv")

        return self.run_pytest(
            args,
            "All Tests with Coverage"
        )

    def run_unit_tests(self, verbose: bool = False) -> int:
        """Run only unit tests."""
        args = ["-m", "unit"]
        if verbose:
            args.append("-vv")

        return self.run_pytest(
            args,
            "Unit Tests Only"
        )

    def run_integration_tests(self, verbose: bool = False) -> int:
        """Run only integration tests."""
        args = ["-m", "integration"]
        if verbose:
            args.append("-vv")

        return self.run_pytest(
            args,
            "Integration Tests Only"
        )

    def run_api_tests(self, verbose: bool = False) -> int:
        """Run only API tests."""
        args = ["-m", "api"]
        if verbose:
            args.append("-vv")

        return self.run_pytest(
            args,
            "API Tests Only"
        )

    def run_by_marker(self, marker: str, verbose: bool = False) -> int:
        """Run tests with specific marker."""
        args = ["-m", marker]
        if verbose:
            args.append("-vv")

        return self.run_pytest(
            args,
            f"Tests with marker: {marker}"
        )

    def run_fast_tests(self) -> int:
        """Run tests excluding slow ones."""
        return self.run_pytest(
            ["-m", "not slow"],
            "Fast Tests (excluding slow)"
        )

    def run_single_file(self, file_path: str, verbose: bool = False) -> int:
        """Run tests in a single file."""
        args = [file_path]
        if verbose:
            args.append("-vv")

        return self.run_pytest(
            args,
            f"Single File: {file_path}"
        )

    def run_failed_tests(self) -> int:
        """Re-run previously failed tests."""
        return self.run_pytest(
            ["--lf"],
            "Previously Failed Tests"
        )

    def run_with_coverage_report(self) -> int:
        """Run all tests and generate HTML coverage report."""
        return self.run_pytest(
            ["--cov=backend", "--cov-report=html", "--cov-report=term"],
            "All Tests with HTML Coverage Report"
        )

    def run_specific_test(self, test_name: str) -> int:
        """Run a specific test by name."""
        return self.run_pytest(
            ["-k", test_name, "-vv"],
            f"Specific Test: {test_name}"
        )

    def check_coverage(self) -> int:
        """Run tests and check coverage meets minimum threshold."""
        return self.run_pytest(
            ["--cov=backend", "--cov-fail-under=80"],
            "Coverage Check (minimum 80%)"
        )


def print_usage():
    """Print usage information."""
    print("""
Test Runner for Subjunctive Practice Backend

Usage:
    python run_tests.py [command] [options]

Commands:
    all             Run all tests (default)
    unit            Run unit tests only
    integration     Run integration tests only
    api             Run API tests only
    fast            Run fast tests (exclude slow)
    failed          Re-run previously failed tests
    coverage        Run tests with HTML coverage report
    check           Run tests and verify 80% coverage

Markers:
    -m <marker>     Run tests with specific marker
                    (e.g., conjugation, exercise, learning, auth)

Options:
    -v, --verbose   Verbose output
    -f <file>       Run specific test file
    -k <name>       Run tests matching name pattern

Examples:
    python run_tests.py all
    python run_tests.py unit -v
    python run_tests.py -m conjugation
    python run_tests.py -k test_conjugate_regular
    python run_tests.py -f tests/unit/test_conjugation.py
    """)


def main():
    """Main entry point."""
    runner = TestRunner()

    if len(sys.argv) == 1 or sys.argv[1] in ["-h", "--help", "help"]:
        print_usage()
        return 0

    command = sys.argv[1]
    verbose = "-v" in sys.argv or "--verbose" in sys.argv

    try:
        if command == "all":
            return runner.run_all_tests(verbose)

        elif command == "unit":
            return runner.run_unit_tests(verbose)

        elif command == "integration":
            return runner.run_integration_tests(verbose)

        elif command == "api":
            return runner.run_api_tests(verbose)

        elif command == "fast":
            return runner.run_fast_tests()

        elif command == "failed":
            return runner.run_failed_tests()

        elif command == "coverage":
            return runner.run_with_coverage_report()

        elif command == "check":
            return runner.check_coverage()

        elif command == "-m" and len(sys.argv) > 2:
            marker = sys.argv[2]
            return runner.run_by_marker(marker, verbose)

        elif command == "-f" and len(sys.argv) > 2:
            file_path = sys.argv[2]
            return runner.run_single_file(file_path, verbose)

        elif command == "-k" and len(sys.argv) > 2:
            test_name = sys.argv[2]
            return runner.run_specific_test(test_name)

        else:
            print(f"Unknown command: {command}")
            print_usage()
            return 1

    except KeyboardInterrupt:
        print("\n\nTests interrupted by user")
        return 130

    except Exception as e:
        print(f"\n\nError running tests: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
