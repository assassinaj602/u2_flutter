# Capability Matrix: u2_flutter vs Appium Flutter Driver

This document outlines the functional features, platform support, and architectural differences between **u2_flutter** and **Appium Flutter Driver**.

| Capability | u2_flutter | Appium Flutter Driver | Notes / Differences |
| :--- | :---: | :---: | :--- |
| **Find by key** | ✅ | ✅ | `u2_flutter` parses keys in deferred locators, resulting in near 0ms local lookup latency. Appium performs a blocking VM check. |
| **Find by text** | ✅ | ✅ | Both support basic text matching against the widget tree. |
| **Find by type** | ✅ | ✅ | Both support widget runtime type filtering (e.g. `ElevatedButton`). |
| **Find by tooltip** | ❌ | ✅ | Appium supports tooltip finder lookups natively. `u2_flutter` requires direct diagnostics queries as a workaround. |
| **Find by semantics** | ❌ | ✅ | Appium utilizes semantic labels. `u2_flutter` does not implement semantic property resolution. |
| **Tap** | ✅ | ✅ | `u2_flutter` sends events directly via WebSocket RPC. Appium translates through an HTTP command loop. |
| **Enter text** | ✅ | ✅ | Standard text input support for text fields. |
| **Get text** | ✅ | ✅ | `u2_flutter` queries properties directly. Appium requires custom VM diagnostics extensions for standard elements. |
| **Scroll** | ✅ | ✅ | Both support view scrolling using translation vectors. |
| **Wait for** | ✅ | ✅ | Element visibility/existence wait loops. |
| **Screenshot** | ❌ | ✅ | `u2_flutter` relies on native `uiautomator2` screenshot capabilities rather than custom Dart VM screen captures. |
| **iOS support** | ❌ | ✅ | `u2_flutter` is designed exclusively for Android ADB-driven environments. Appium supports both iOS (XCUITest wrapper) and Android. |
| **Multi-device** | ✅ | ✅ | `u2_flutter` dynamically allocates local ADB ports (8181+), enabling simultaneous execution without conflicts. |
| **uiautomator2 native** | ✅ | ❌ | `u2_flutter` allows seamless hybrid switching between native Android views and Flutter views without restarting sessions. |
| **Kea2 integration** | ✅ | ❌ | Built-in support for Kea2 static checks and fast fuzzing validation loops. |
| **Zero middle layers** | ✅ | ❌ | `u2_flutter` communicates directly with the Dart VM WebSocket without intermediary Appium Nodes. |

### Summary Key:
* ✅ Supported
* ❌ Not supported
* 🔄 In progress
