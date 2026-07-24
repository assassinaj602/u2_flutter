# Reproducible Benchmark: u2_flutter vs Appium Flutter Driver

This guide explains how to run the performance benchmark comparing **u2_flutter** and **Appium Flutter Driver** side-by-side.

## Prerequisites

1. **Android Device**: A physical Android device or emulator running with Developer Options and USB Debugging enabled.
2. **ADB Installed**: The standard Android Debug Bridge tool must be available in your system path.
3. **Flutter Test App**:
   * Build and run the `test_app` under your device:
     ```bash
     cd test_app
     flutter run
     ```
   * Ensure it is running in debug mode so that the Dart Observatory port is active and discoverable.

## Dependencies

Install the required Python and platform dependencies:

```bash
# Activate your virtual environment
venv\Scripts\activate

# Install testing utilities
pip install uiautomator2 Appium-Python-Client
```

## Running the Benchmark

Execute the benchmark script directly:

```bash
python scripts/run_benchmark.py
```

## How It Works

The benchmark conducts 100 sequential iterations of:
1. **Locate**: Resolving the widget `submit_btn` by its key.
2. **Tap**: Actuating a click/touch event on the button.
3. **Query**: Fetching greeting text attributes from the widget tree.

The script records latencies for each operation, aggregates statistical metrics (Mean, Median, Min, Max, Standard Deviation), and output results to `benchmark_results.md`.
