# Kea2 Fuzzing Validation Report

This document reports the performance characteristics of Kea2's integration loops over 100 fuzzing cycles.

## Summary Results

| Metric | Measured Value | Target / Baseline | Status |
| :--- | :---: | :---: | :---: |
| **Fuzzing Iterations** | 100 | 100 | Completed |
| **Success Rate** | 100.0% | 100% | **PASSED** |
| **Avg Precondition Evaluation Time** | 0.00 ms | <1 ms (local check) | **PASSED** (local parsing) |
| **Avg Action Latency (Tap)** | 667.25 ms | N/A | Evaluated |

## Performance Breakdown (ms)

### Precondition (Hierarchy parsing & local match)
- **Mean**: 0.00 ms
- **Min**: 0.00 ms
- **Max**: 0.01 ms

### Action Execution (Dart VM tap action)
- **Mean**: 667.25 ms
- **Min**: 393.55 ms
- **Max**: 735.61 ms

## Reliability Assessment
- **Errors/Failures**: No exceptions or connection errors occurred.
- **Overall Rating**: High stability under recurrent Flutter static checker loads.
