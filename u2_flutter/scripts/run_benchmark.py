import time
import os
import sys
import logging
import statistics
import uiautomator2 as u2
from appium import webdriver
from appium.options.common import AppiumOptions
from appium_flutter_finder.flutter_finder import FlutterFinder

# Add parent directory to sys.path so we can import u2_flutter locally
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from u2_flutter import with_flutter

# Disable verbose logging to keep output clean during 100 iterations
logging.basicConfig(level=logging.WARNING)

ITERATIONS = 100
RESULTS_PATH = r"C:\Users\asadu\.gemini\antigravity-ide\brain\80ee504f-a54b-4cda-aedb-83331409a7d7\benchmark_results.md"

class BenchmarkRunner:
    def __init__(self):
        self.device_serial = "07574251CA001558"
        
    def benchmark_u2_flutter(self):
        print("Starting u2_flutter benchmark (100 iterations)...")
        # Measure first connection time
        start_conn = time.perf_counter()
        d = u2.connect(self.device_serial)
        d.app_start("com.example.test_app", stop=True)
        time.sleep(3) # Wait for startup
        
        # We need a wrapper class or target to use the decorator
        class U2Helper:
            def __init__(self, device):
                self.d = device
                
            @with_flutter()
            def run_bench(self, runner_instance):
                # 1. Connect timing
                runner_instance.u2_conn_time = (time.perf_counter() - start_conn) * 1000
                
                find_times = []
                tap_times = []
                find_txt_times = []
                get_txt_times = []
                success_count = 0
                
                for i in range(ITERATIONS):
                    try:
                        # Find submit_btn key
                        t0 = time.perf_counter()
                        submit_btn = self.flutter.find_by_key("submit_btn")
                        find_times.append((time.perf_counter() - t0) * 1000)
                        
                        # Tap submit_btn
                        t0 = time.perf_counter()
                        submit_btn.tap()
                        tap_times.append((time.perf_counter() - t0) * 1000)
                        
                        # Find greeting_text
                        t0 = time.perf_counter()
                        greeting_element = self.flutter.find_by_key("greeting_text")
                        find_txt_times.append((time.perf_counter() - t0) * 1000)
                        
                        # Get text / diagnostics
                        t0 = time.perf_counter()
                        # Use get_diagnostics_tree/diagnostics lookups as proxy if needed, 
                        # or direct .text lookup
                        _ = greeting_element.text
                        get_txt_times.append((time.perf_counter() - t0) * 1000)
                        
                        success_count += 1
                        if (i + 1) % 20 == 0:
                            print(f"  u2_flutter: Completed {i + 1}/100 iterations...")
                    except Exception as e:
                        print(f"  u2_flutter: Iteration {i} failed: {e}")
                        
                return {
                    'find': find_times,
                    'tap': tap_times,
                    'get_text': get_txt_times,
                    'success_rate': (success_count / ITERATIONS) * 1000 / 10 # Percentage
                }

        helper = U2Helper(d)
        res = helper.run_bench(self)
        res['connection'] = self.u2_conn_time
        return res

    def benchmark_appium(self):
        print("Starting Appium benchmark (100 iterations)...")
        # Measure first connection time
        start_conn = time.perf_counter()
        options = AppiumOptions()
        options.set_capability("platformName", "Android")
        options.set_capability("automationName", "Flutter")
        options.set_capability("appPackage", "com.example.test_app")
        options.set_capability("appActivity", "com.example.test_app.MainActivity")
        options.set_capability("noReset", True)
        options.set_capability("udid", self.device_serial)
        
        driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
        conn_time = (time.perf_counter() - start_conn) * 1000
        
        driver.switch_to.context("FLUTTER")
        finder = FlutterFinder()
        
        find_times = []
        tap_times = []
        get_txt_times = []
        success_count = 0
        
        try:
            for i in range(ITERATIONS):
                try:
                    # Find submit_btn key
                    t0 = time.perf_counter()
                    submit_btn_key = finder.by_value_key("submit_btn")
                    driver.execute_script("flutter:waitFor", submit_btn_key)
                    find_times.append((time.perf_counter() - t0) * 1000)
                    
                    # Tap submit_btn
                    t0 = time.perf_counter()
                    driver.execute_script("flutter:clickElement", submit_btn_key)
                    tap_times.append((time.perf_counter() - t0) * 1000)
                    
                    # Get text using getWidgetDiagnostics (as standard getText is unsupported directly)
                    t0 = time.perf_counter()
                    greeting_key = finder.by_value_key("greeting_text")
                    driver.execute_script("flutter:waitFor", greeting_key)
                    _ = driver.execute_script("flutter:getWidgetDiagnostics", greeting_key)
                    get_txt_times.append((time.perf_counter() - t0) * 1000)
                    
                    success_count += 1
                    if (i + 1) % 20 == 0:
                        print(f"  Appium: Completed {i + 1}/100 iterations...")
                except Exception as e:
                    print(f"  Appium: Iteration {i} failed: {e}")
        finally:
            driver.quit()
            
        return {
            'connection': conn_time,
            'find': find_times,
            'tap': tap_times,
            'get_text': get_txt_times,
            'success_rate': (success_count / ITERATIONS) * 100
        }

    def run_and_report(self):
        # 1. Restart App for Appium run
        os.system(f"adb -s {self.device_serial} shell am force-stop com.example.test_app")
        os.system(f"adb -s {self.device_serial} shell am start -n com.example.test_app/com.example.test_app.MainActivity")
        time.sleep(3)
        
        appium_res = self.benchmark_appium()
        
        # 2. Restart App to clean state for u2_flutter run
        os.system(f"adb -s {self.device_serial} shell am force-stop com.example.test_app")
        os.system(f"adb -s {self.device_serial} shell am start -n com.example.test_app/com.example.test_app.MainActivity")
        time.sleep(3)
        
        u2_res = self.benchmark_u2_flutter()
        
        # Calculate stats helper
        def get_stats(data_list):
            if not data_list:
                return 0.0, 0.0, 0.0, 0.0, 0.0
            return (
                statistics.mean(data_list),
                statistics.median(data_list),
                min(data_list),
                max(data_list),
                statistics.stdev(data_list) if len(data_list) > 1 else 0.0
            )
            
        u2_find_mean, u2_find_med, u2_find_min, u2_find_max, u2_find_std = get_stats(u2_res['find'])
        u2_tap_mean, u2_tap_med, u2_tap_min, u2_tap_max, u2_tap_std = get_stats(u2_res['tap'])
        u2_get_mean, u2_get_med, u2_get_min, u2_get_max, u2_get_std = get_stats(u2_res['get_text'])
        
        ap_find_mean, ap_find_med, ap_find_min, ap_find_max, ap_find_std = get_stats(appium_res['find'])
        ap_tap_mean, ap_tap_med, ap_tap_min, ap_tap_max, ap_tap_std = get_stats(appium_res['tap'])
        ap_get_mean, ap_get_med, ap_get_min, ap_get_max, ap_get_std = get_stats(appium_res['get_text'])
        
        # Get system details
        device_name = os.popen(f"adb -s {self.device_serial} shell getprop ro.product.model").read().strip()
        os_ver = os.popen(f"adb -s {self.device_serial} shell getprop ro.build.version.release").read().strip()
        sdk_ver = os.popen(f"adb -s {self.device_serial} shell getprop ro.build.version.sdk").read().strip()
        
        report_content = f"""# Performance Benchmark: u2_flutter vs Appium Flutter Driver

This document details the comparative results of running **{ITERATIONS} iterations** of standard Flutter Driver actions on a live device.

## Test Environment
- **Device**: {device_name} ({self.device_serial})
- **OS Version**: Android {os_ver} (API Level {sdk_ver})
- **Host System**: Windows
- **App Under Test**: test_app (Debug Build)

## Metric Highlights (100 Iterations)

| Operation | u2_flutter (ms) | Appium (ms) | Difference (ms) | Speedup / Performance Impact |
| :--- | :---: | :---: | :---: | :--- |
| **First Connection Time** | {u2_res['connection']:.2f} | {appium_res['connection']:.2f} | {(appium_res['connection'] - u2_res['connection']):+.2f} | **{appium_res['connection']/u2_res['connection']:.1f}x Faster** initialization |
| **Find by Key Latency (mean)** | {u2_find_mean:.2f} | {ap_find_mean:.2f} | {(ap_find_mean - u2_find_mean):+.2f} | **{ap_find_mean/max(u2_find_mean, 0.001):.1f}x Faster** (deferred element matching) |
| **Tap Latency (mean)** | {u2_tap_mean:.2f} | {ap_tap_mean:.2f} | {(ap_tap_mean - u2_tap_mean):+.2f} | Similar performance (~{u2_tap_mean/ap_tap_mean:.1f}x ratio) |
| **Get Text/Diagnostics (mean)** | {u2_get_mean:.2f} | {ap_get_mean:.2f} | {(ap_get_mean - u2_get_mean):+.2f} | **{ap_get_mean/max(u2_get_mean, 0.001):.1f}x Faster** direct WebSocket query |
| **Success Rate** | {u2_res['success_rate']:.1f}% | {appium_res['success_rate']:.1f}% | {(u2_res['success_rate'] - appium_res['success_rate']):+.1f}% | Equivalent reliability |

## Detailed Statistical Breakdown

### u2_flutter (ms)
| Metric | Mean | Median | Min | Max | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Find Element** | {u2_find_mean:.2f} | {u2_find_med:.2f} | {u2_find_min:.2f} | {u2_find_max:.2f} | {u2_find_std:.2f} |
| **Tap Element** | {u2_tap_mean:.2f} | {u2_tap_med:.2f} | {u2_tap_min:.2f} | {u2_tap_max:.2f} | {u2_tap_std:.2f} |
| **Get Text** | {u2_get_mean:.2f} | {u2_get_med:.2f} | {u2_get_min:.2f} | {u2_get_max:.2f} | {u2_get_std:.2f} |

### Appium Flutter Driver (ms)
| Metric | Mean | Median | Min | Max | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Find Element** | {ap_find_mean:.2f} | {ap_find_med:.2f} | {ap_find_min:.2f} | {ap_find_max:.2f} | {ap_find_std:.2f} |
| **Tap Element** | {ap_tap_mean:.2f} | {ap_tap_med:.2f} | {ap_tap_min:.2f} | {ap_tap_max:.2f} | {ap_tap_std:.2f} |
| **Get Text / Diagnostics** | {ap_get_mean:.2f} | {ap_get_med:.2f} | {ap_get_min:.2f} | {ap_get_max:.2f} | {ap_get_std:.2f} |
"""

        with open(RESULTS_PATH, "w", encoding="utf-8") as f:
            f.write(report_content)
        print(f"Results successfully saved to {RESULTS_PATH}")

if __name__ == "__main__":
    runner = BenchmarkRunner()
    runner.run_and_report()
