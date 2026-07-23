import unittest
from unittest.mock import Mock, patch
import sys
import os

# Add parent directory to sys.path so we can import kea2_integration locally
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kea2_integration.flutter_script_driver import FlutterScriptDriver

class TestFlutterScriptDriver(unittest.TestCase):
    def setUp(self):
        self.mock_driver = Mock()
        self.script_driver = FlutterScriptDriver(self.mock_driver)

    def test_tap_key(self):
        finder = {"type": "key", "value": "submit_btn"}
        # Mock find_by_key to return a mock element
        mock_element = Mock()
        self.mock_driver.find_by_key.return_value = mock_element

        self.script_driver.tap(finder)
        
        self.mock_driver.find_by_key.assert_called_once_with("submit_btn")
        mock_element.tap.assert_called_once()

    def test_input_key(self):
        finder = {"type": "key", "value": "username_input"}
        mock_element = Mock()
        self.mock_driver.find_by_key.return_value = mock_element

        self.script_driver.input(finder, "hello")

        self.mock_driver.find_by_key.assert_called_once_with("username_input")
        mock_element.enter_text.assert_called_once_with("hello")

    def test_get_text_key(self):
        finder = {"type": "key", "value": "greeting"}
        mock_element = Mock()
        mock_element.text = "welcome"
        self.mock_driver.find_by_key.return_value = mock_element

        val = self.script_driver.get_text(finder)
        
        self.assertEqual(val, "welcome")
        self.mock_driver.find_by_key.assert_called_once_with("greeting")

    def test_scroll_key(self):
        finder = {"type": "key", "value": "list_view"}
        mock_element = Mock()
        self.mock_driver.find_by_key.return_value = mock_element

        self.script_driver.scroll(finder, dx=0, dy=-50, duration=300)

        self.mock_driver.find_by_key.assert_called_once_with("list_view")
        mock_element.scroll.assert_called_once_with(0, -50, 300)

    def test_wait_for_key(self):
        finder = {"type": "key", "value": "submit_btn"}
        mock_element = Mock()
        mock_element.wait_for.return_value = True
        self.mock_driver.find_by_key.return_value = mock_element

        result = self.script_driver.wait_for(finder, timeout=4000)
        
        self.assertTrue(result)
        self.mock_driver.find_by_key.assert_called_once_with("submit_btn")
        mock_element.wait_for.assert_called_once_with(4000)

if __name__ == "__main__":
    unittest.main()
