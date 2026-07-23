import pytest
from unittest.mock import MagicMock, patch
from u2_flutter import FlutterBridge, FlutterDriver, Flutter, with_flutter
from u2_flutter.flutter_plugin import FlutterElement

class Testu2Flutter:
    @pytest.fixture
    def mock_device(self):
        device = MagicMock()
        device._serial = "12345"
        device.shell.return_value.output = "The Dart VM service is listening on http://127.0.0.1:8181/auth_token_123/"
        return device

    @pytest.fixture
    def mock_bridge(self, mock_device):
        bridge = FlutterBridge(mock_device)
        bridge.ws = MagicMock()
        return bridge

    @pytest.fixture
    def driver(self, mock_bridge):
        # We also mock _get_main_isolate_id to return a fixed isolate ID
        driver = FlutterDriver(mock_bridge)
        driver._isolate_id = "isolates/main"
        return driver

    def test_find_by_key(self, driver):
        finder = driver.find_by_key("submit_btn")
        assert finder["finderType"] == "ByValueKey"
        assert finder["keyValueString"] == "submit_btn"
        assert finder["keyValueType"] == "String"

    def test_find_by_text(self, driver):
        finder = driver.find_by_text("Click Me")
        assert finder["finderType"] == "ByText"
        assert finder["text"] == "Click Me"

    def test_find_by_type(self, driver):
        finder = driver.find_by_type("ElevatedButton")
        assert finder["finderType"] == "ByType"
        assert finder["type"] == "ElevatedButton"

    def test_tap_sends_correct_rpc(self, driver, mock_bridge):
        finder = {"finderType": "ByText", "text": "Click"}
        
        # Mock the recv response for tap
        mock_bridge.ws.recv.return_value = '{"jsonrpc": "2.0", "result": {"isError": false, "response": {}}, "id": 1}'
        
        driver.tap(finder)
        
        # Verify correct payload was sent
        mock_bridge.ws.send.assert_called_once()
        sent_payload = mock_bridge.ws.send.call_args[0][0]
        assert '"command": "tap"' in sent_payload
        assert '"text": "Click"' in sent_payload

    def test_enter_text_sends_correct_rpc(self, driver, mock_bridge):
        finder = {"finderType": "ByValueKey", "keyValueString": "input", "keyValueType": "String"}
        
        # Mock responses for tap and enter_text
        mock_bridge.ws.recv.side_effect = [
            '{"jsonrpc": "2.0", "result": {"isError": false, "response": {}}, "id": 1}', # tap response
            '{"jsonrpc": "2.0", "result": {"isError": false, "response": {}}, "id": 2}'  # enter_text response
        ]
        
        driver.enter_text(finder, "mytext")
        
        # Verify enter_text sent correct parameters
        assert mock_bridge.ws.send.call_count == 2
        enter_text_payload = mock_bridge.ws.send.call_args_list[1][0][0]
        assert '"command": "enter_text"' in enter_text_payload
        assert '"text": "mytext"' in enter_text_payload

    def test_get_text_success(self, driver, mock_bridge):
        finder = {"finderType": "ByValueKey", "keyValueString": "label", "keyValueType": "String"}
        mock_bridge.ws.recv.return_value = '{"jsonrpc": "2.0", "result": {"isError": false, "response": {"text": "hello"}}, "id": 1}'
        
        text = driver.get_text(finder)
        assert text == "hello"

    def test_rpc_error_handling(self, driver, mock_bridge):
        finder = {"finderType": "ByValueKey", "keyValueString": "invalid", "keyValueType": "String"}
        
        # Mock an error response from the VM Service
        mock_bridge.ws.recv.return_value = '{"jsonrpc": "2.0", "error": {"code": -32603, "message": "Widget not found"}, "id": 1}'
        
        with pytest.raises(RuntimeError) as exc_info:
            driver.tap(finder)
            
        assert "JSON-RPC Error" in str(exc_info.value)
        assert "Widget not found" in str(exc_info.value)

    @patch("u2_flutter.flutter_plugin.Flutter")
    def test_decorator_lifecycle(self, mock_flutter_class):
        mock_flutter_instance = MagicMock()
        mock_flutter_class.return_value = mock_flutter_instance
        
        class FakeTestClass:
            def __init__(self):
                self.d = MagicMock()
            
            @with_flutter(local_port=1234)
            def test_method(self):
                assert self.flutter == mock_flutter_instance
                self.test_called = True
        
        obj = FakeTestClass()
        obj.test_called = False
        
        # Invoke decorated method
        obj.test_method()
        
        # Assert lifecycle methods were called
        mock_flutter_class.assert_called_once_with(obj.d, local_port=1234)
        mock_flutter_instance.attach.assert_called_once()
        mock_flutter_instance.detach.assert_called_once()
        assert obj.test_called is True

    @patch("u2_flutter.flutter_plugin.Flutter")
    def test_decorator_cleanup_on_failure(self, mock_flutter_class):
        mock_flutter_instance = MagicMock()
        mock_flutter_class.return_value = mock_flutter_instance
        
        class FakeTestClass:
            def __init__(self):
                self.d = MagicMock()
            
            @with_flutter(local_port=1234)
            def test_method_fails(self):
                raise ValueError("Test failed intentionally")
        
        obj = FakeTestClass()
        
        # Assert error is raised but detach() is still executed
        with pytest.raises(ValueError, match="Test failed intentionally"):
            obj.test_method_fails()
            
        mock_flutter_instance.attach.assert_called_once()
        mock_flutter_instance.detach.assert_called_once()
