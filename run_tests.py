#!/usr/bin/env python3
"""
Test runner for GenX Trading Platform
Optimized for parallel execution, coverage reporting, and developer productivity.
"""

import os
import subprocess
import sys
import argparse
import time


def run_tests(parallel: bool = False, lint: bool = False, report: bool = False) -> bool:
    """
    Runs the complete test suite for the GenX Trading Platform.

    Args:
        parallel (bool): Whether to run tests in parallel using pytest-xdist.
        lint (bool): Whether to run linting before tests.
        report (bool): Whether to generate a coverage report.

    Returns:
        bool: True if all steps pass, False otherwise.
    """
    overall_start_time = time.time()

    if lint:
        print("🔍 Running Linting (npm run lint)...")
        try:
            # We use npm run lint which is configured in package.json
            lint_result = subprocess.run(["npm", "run", "lint"], capture_output=True, text=True)
            if lint_result.returncode != 0:
                print("❌ Linting failed!")
                print(lint_result.stdout)
                print(lint_result.stderr)
                return False
            print("✅ Linting passed.")
        except Exception as e:
            print(f"Error running lint: {e}")
            return False

    # Set test environment
    os.environ["TESTING"] = "1"
    os.environ["SECRET_KEY"] = "test-secret-key"
    os.environ["DATABASE_URL"] = "postgresql://test:test@localhost/test"
    os.environ["MONGODB_URL"] = "mongodb://localhost:27017/test"
    os.environ["REDIS_URL"] = "redis://localhost:6379"

    # Mock required Exness credentials for config validation
    os.environ["EXNESS_LOGIN"] = "12345678"
    os.environ["EXNESS_PASSWORD"] = "mock_password_123"
    os.environ["EXNESS_SERVER"] = "Exness-MT5Trial"

    print("\n🚀 Running GenX Trading Platform Tests...")
    mode_str = "Parallel (pytest-xdist)" if parallel else "Sequential"
    print(f"📊 Mode: {mode_str}")
    if report:
        print("📈 Coverage: Enabled")
    print("=" * 50)

    # Base pytest command
    # We target core/ and api/ for coverage to avoid noise from tests/ itself
    pytest_args = [sys.executable, "-m", "pytest", "tests/", "-v", "--tb=short"]

    # Add parallel execution if requested
    if parallel:
        pytest_args.extend(["-n", "auto"])

    # Add coverage if requested
    if report:
        pytest_args.extend(["--cov=core", "--cov=api", "--cov=ai_models", "--cov-report=term-missing"])

    # Run pytest
    try:
        test_start_time = time.time()
        result = subprocess.run(
            pytest_args,
            capture_output=True,
            text=True,
        )
        test_end_time = time.time()

        print(result.stdout)
        if result.stderr:
            # Filter out known xdist info messages from stderr if needed
            print("STDERR:", result.stderr)

        success = result.returncode == 0
        overall_end_time = time.time()

        print("=" * 50)
        if success:
            print(f"✨ All steps passed!")
        else:
            print(f"❌ Tests failed!")

        print(f"⏱️  Test execution: {test_end_time - test_start_time:.2f}s")
        print(f"⏱️  Total time: {overall_end_time - overall_start_time:.2f}s")

        return success

    except Exception as e:
        print(f"Error running tests: {e}")
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GenX Test Runner")
    parser.add_argument(
        "--parallel",
        action="store_true",
        help="Run tests in parallel using pytest-xdist"
    )
    parser.add_argument(
        "--lint",
        action="store_true",
        help="Run linting before tests"
    )
    parser.add_argument(
        "--report",
        action="store_true",
        help="Generate coverage report"
    )
    args = parser.parse_args()

    success = run_tests(parallel=args.parallel, lint=args.lint, report=args.report)
    sys.exit(0 if success else 1)
