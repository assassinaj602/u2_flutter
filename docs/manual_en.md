# User Manual

- [Advanced Feature 5: Support for Flutter Interaction](#advanced-feature-5-support-for-flutter-interaction)

## Advanced Feature 5: Support for Flutter Interaction

**Introduction**

u2_flutter is a standalone plugin that extends Kea2 to support testing Flutter applications. It provides a high-level Flutter driver that abstracts the Flutter widget tree, allowing you to write property-based tests that interact directly with Flutter UI elements.

**Repository**

- GitHub: https://github.com/assassinaj602/u2_flutter

**Prerequisites**

- Flutter SDK (3.16+)
- Debug build of your Flutter app (APK or IPA)
- Python 3.7+ with u2_flutter installed

**Flutter App Preparation**

`dart
import 'package:flutter_driver/flutter_driver.dart';

void main() async {
  enableFlutterDriverExtension();
  runApp(MyApp());
}
`

**Installation**

`ash
pip install -e .
`

**Usage Example**

`python
import unittest
from u2_flutter import Flutter, with_flutter

class TestFlutterApp(unittest.TestCase):
    @with_flutter
    def test_login(self):
        self.flutter.find_by_key('username').enter_text('alice')
        self.flutter.find_by_key('password').enter_text('secret')
        self.flutter.find_by_key('login_btn').tap()
        assert self.flutter.find_by_key('welcome_msg').text == 'Welcome, alice!'
`

**Running Tests**

`ash
python -m unittest examples/basic_usage.py
`

**Using with Kea2**

- Import Flutter and with_flutter decorator in your Kea2 scripts
- Use self.flutter in @precondition/@prob decorated methods

**Known Limitations**

- Currently only supports Android debug builds
- UI element location depends on widget key
