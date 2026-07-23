# u2_flutter 🚀

[![PyPI version](https://img.shields.io/badge/pypi-v0.1.0-blue.svg)](https://pypi.org/project/u2-flutter/)
[![Python versions](https://img.shields.io/badge/python-3.7+-blue.svg)](https://pypi.org/project/u2-flutter/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/assassinaj602/u2_flutter/blob/main/LICENSE)

A standalone Python package and plugin for `uiautomator2` designed to find, inspect, and interact with Flutter widgets. It connects to the Dart VM Service over a WebSocket connection using ADB port forwarding to send JSON-RPC commands directly to Flutter's Driver extension.

> [!NOTE]
> This project is inspired by the `u2_webview` extension pattern and is built to integrate as a core driver option in **Kea2** fuzzing environments.

---

## 🛠️ Status: Phase 1 & 2 Completed (Phase 3 Integration in Progress)

We have successfully built and verified the core standalone implementation and Pytest unit test suite.

- **WebSocket connection over ADB**: Parses the modern Flutter VM auth token automatically from `logcat` to bypass `403 Forbidden` restriction.
- **Fluent & Chainable Element API**: Interact with widgets easily using patterns like `self.flutter.find_by_key("submit_btn").tap()`.
- **Lifecycle Decorator**: Managed connection state using `@with_flutter` to guarantee automated attach and detach logic.
- **Isolate ID Caching**: Minimizes unnecessary VM queries, caching the Isolate ID for fast execution.
- **Diagnostics Tree Caching (Phase 3)**: Fetches and caches the full Widget diagnostics tree (`get_diagnostics_tree()` & `cache_widget_tree()`) for fast static checker lookups.

---

## 🏗️ How it Works Under the Hood

The communication pipeline runs as follows:

```mermaid
graph TD
    A[Python Test Script] -->|1. decorator: with_flutter| B(FlutterBridge)
    B -->|2. scans logcat| C{Find VM Port & Auth Token}
    C -->|3. adb forward| D[Local Port tcp:8181]
    D -->|4. establish WebSocket| E[Dart VM Service WebSocket]
    A -->|5. self.flutter.find_by_key| F(FlutterDriver)
    F -->|6. JSON-RPC ext.flutter.driver| E
    E -->|7. Executes action| G[Running Flutter Test App]
```

1. **Service Registration**: The Flutter application is built with the `flutter_driver` dependency and starts the VM service using `enableFlutterDriverExtension()`.
2. **Bridge Handshake**: `u2_flutter` parses the `logcat` output of the device to capture the dynamic VM Service port and the required security `auth token`.
3. **Port Forwarding**: Standard ADB commands map the local port (`8181`) to the dynamic device VM port.
4. **WebSocket Transport**: Opens a WebSocket connection directly into the Dart VM Service (`ws://127.0.0.1:8181/<token>/ws`).
5. **Command Dispatch**: Constructs JSON-RPC 2.0 requests with driver-specific payloads (e.g. `tap`, `enter_text`, `get_text`) and routes them directly to the active Dart isolate.

---

## 📦 Project Structure

```text
u2_flutter/
├── u2_flutter/
│   ├── __init__.py           # Package entry point
│   ├── flutter_bridge.py     # Logcat scanning, port forwarding, socket connection
│   ├── flutter_driver.py     # JSON-RPC command assembly, isolate caching, finders
│   └── flutter_plugin.py     # Plugin wrapper and @with_flutter decorator
├── test_app/                 # Example Flutter test application
├── examples/
│   └── test_script.py        # Complete execution test scenario
├── tests/                    # Project unit tests
├── requirements.txt
└── setup.py
```

---

## 🚀 Getting Started

### 1. Prerequisites
Ensure you have the Flutter SDK and Python 3.7+ installed.

### 2. Setting Up the Flutter App
The Flutter application must enable the Driver extension inside `lib/main.dart`:

```dart
import 'package:flutter/material.dart';
import 'package:flutter_driver/driver_extension.dart';

void main() {
  enableFlutterDriverExtension(); // Register ext.flutter.driver service
  runApp(const MyApp());
}
```

Add the `flutter_driver` dependency to your `pubspec.yaml`:
```yaml
dev_dependencies:
  flutter_driver:
    sdk: flutter
```

Build the debug APK (debug builds automatically expose the VM Service):
```bash
cd test_app
flutter build apk --debug
```

### 3. Running the Python Test Script
Set up the python virtual environment, install dependencies, and run:

```bash
# Set up venv
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt

# Run the test script
python examples/test_script.py
```

---

## 📝 Example Usage

Here is a quick look at how you can write a test case using the `@with_flutter` decorator:

```python
import uiautomator2 as u2
from u2_flutter import with_flutter

class MyTestClass:
    def __init__(self):
        self.d = u2.connect() # uiautomator2 device instance at self.d

    @with_flutter(local_port=8181)
    def test_my_app(self):
        # Find a TextField by Key and enter text
        self.flutter.find_by_key("username_input").enter_text("testuser")
        
        # Tap the Submit button
        self.flutter.find_by_key("submit_btn").tap()
        
        # Read the updated greeting text
        greeting = self.flutter.find_by_key("greeting_text").text
        print(f"Result: {greeting}")
        assert greeting == "Hello, testuser!"
```

---

## 🛣️ Roadmap

- [x] **Phase 1**: Standalone plugin with bridge, driver, and decorators.
- [x] **Phase 2**: Align APIs and write comprehensive unit tests.
- [/] **Phase 3**: Integrate `FlutterStaticChecker` and `FlutterScriptDriver` into **Kea2**.

---

## 🤝 Acknowledgments & Credits

- [uiautomator2](https://github.com/openatx/uiautomator2) - The underlying Android UI automation engine used.
- [u2_webview](https://github.com/openatx/u2_webview) - The Flask-extension pattern that inspired this plugin architecture.

