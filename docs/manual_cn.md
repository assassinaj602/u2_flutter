# 用户手册

- [高级功能 5：支持 Flutter 操作](#高级功能-5支持-flutter-操作)

## 高级功能 5：支持 Flutter 操作

**简介**

u2_flutter 是一个独立插件，扩展了 Kea2，使其能够对 Flutter 应用进行测试。它提供了高级的 Flutter 驱动，抽象了 Flutter 的 widget 树，允许你编写基于属性的测试直接与 Flutter UI 元素交互。

**代码仓库**

- GitHub: https://github.com/assassinaj602/u2_flutter

**前置条件**

- Flutter SDK (3.16+)
- Flutter 应用的调试构建（APK 或 IPA）
- Python 3.7+ 与已安装的 u2_flutter

**Flutter 应用准备**

`dart
import 'package:flutter_driver/flutter_driver.dart';

void main() async {
  enableFlutterDriverExtension();
  runApp(MyApp());
}
`

**安装方式**

`ash
pip install -e .
`

**使用示例**

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

**运行测试**

`ash
python -m unittest examples/basic_usage.py
`

**在 Kea2 中使用**

- 在 Kea2 脚本中导入 Flutter 和 with_flutter 装饰器。
- 在 @precondition/@prob 装饰的方法中使用 self.flutter，类似使用 Device 驱动。

**已知限制**

- 目前仅支持 Android 调试版。
- UI 元素定位依赖 widget 的 key，请在 Flutter 代码中为需要交互的控件设置 Key。
