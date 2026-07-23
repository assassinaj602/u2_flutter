# Contributing to u2_flutter

Thank you for your interest in contributing to `u2_flutter`! We welcome community contributions, bug reports, and feature suggestions to help make Flutter testing on Android faster and more reliable.

## Code of Conduct

Please be respectful, constructive, and professional in all communications, issue descriptions, and pull request discussions.

## How to Contribute

### 1. Reporting Bugs
* Search the existing issues list before opening a new one.
* Include detailed steps to reproduce the issue.
* Provide details about your environment:
  * OS (Windows/macOS/Linux)
  * Flutter SDK version
  * Python version
  * Connected device model and Android version
  * Logcat outputs or error stack traces if applicable.

### 2. Suggesting Enhancements
* Open an issue explaining the proposed feature and why it would be beneficial.
* Provide usage examples or API signature sketches if applicable.

### 3. Submitting Pull Requests
* Fork the repository and create your branch from `main`.
* Write clean, documented Python code matching the repository patterns.
* Add unit or integration tests under the `tests/` directory for any new features or bug fixes.
* Ensure all existing tests pass before submitting your PR.
* Keep your PR focused on a single change or issue.

---

## Local Development Setup

To set up your development environment locally:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/assassinaj602/u2_flutter.git
   cd u2_flutter
   ```

2. **Set Up a Virtual Environment:**
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   pip install pytest mock
   ```

4. **Run Unit Tests:**
   ```bash
   pytest
   ```

## Development Architecture Notes

* **Direct Dart VM Communication**: The core of `u2_flutter` communicates directly with the Dart VM WebSocket connection bypassing Appium's middle-man HTTP server. Keep changes performance-conscious.
* **Dynamic Ports**: Avoid hardcoding port mappings (such as `8181`). Utilize the dynamic port resolver configuration options when writing extensions or examples.
* **Compatibility Layer**: Ensure that modifications to helper decorators (like `@with_flutter`) preserve fallback capabilities for standard non-decorator test class setups.
