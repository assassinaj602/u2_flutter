import time
import json
import logging
import websocket
from typing import Dict, Any

logger = logging.getLogger("u2_flutter.driver")

class FlutterDriver:
    def __init__(self, bridge):
        """
        Initialize the Flutter Driver.
        
        Args:
            bridge: An instance of FlutterBridge.
        """
        self.bridge = bridge
        self._next_id = 1
        self._isolate_id = None
        self._cached_tree = None

    def _send_rpc(self, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sends a JSON-RPC request over the WebSocket with automatic retries on timeout.
        """
        if not self.bridge.ws:
            raise RuntimeError("Not attached to Flutter VM Service. Call attach() first.")
            
        rpc_id = self._next_id
        self._next_id += 1
        
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": rpc_id
        }
        
        request_str = json.dumps(payload)
        logger.debug(f"Sending JSON-RPC Request: {request_str}")
        
        response_str = ""
        for attempt in range(3):
            try:
                self.bridge.ws.send(request_str)
                response_str = self.bridge.ws.recv()
                break
            except (websocket.WebSocketTimeoutException, TimeoutError) as e:
                if attempt == 2:
                    logger.error(f"WebSocket operation timed out after 3 attempts: {e}")
                    raise RuntimeError(f"WebSocket operation timed out: {e}")
                logger.warning(f"WebSocket recv timed out, retrying attempt {attempt + 2}...")
                time.sleep(1)
                
        logger.debug(f"Received JSON-RPC Response: {response_str}")
        
        response = json.loads(response_str)
        if "error" in response:
            raise RuntimeError(f"JSON-RPC Error: {response['error']}")
            
        return response.get("result", {})

    def _send_driver_command(self, command: str, finder: Dict[str, Any], extra_params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Helper method to send a command to ext.flutter.driver.
        """
        params = {
            "command": command
        }
        if finder:
            params.update(finder)
        if extra_params:
            params.update(extra_params)
            
        # Get the isolate ID dynamically
        isolate_id = self._get_main_isolate_id()
        params["isolateId"] = isolate_id
        
        return self._send_rpc("ext.flutter.driver", params)

    def _get_main_isolate_id(self) -> str:
        """
        Retrieves the main isolate ID from the VM.
        """
        if self._isolate_id:
            return self._isolate_id
            
        # Call 'getVM' to list isolates
        vm_info = self._send_rpc("getVM", {})
        isolates = vm_info.get("isolates", [])
        if not isolates:
            raise RuntimeError("No isolates found in Dart VM.")
        # Return the first isolate ID (usually the main running app)
        self._isolate_id = isolates[0]["id"]
        return self._isolate_id

    def find_by_key(self, key: str) -> Dict[str, Any]:
        """
        Creates a finder dictionary for finding by Key value.
        """
        return {
            "finderType": "ByValueKey",
            "keyValueString": str(key),
            "keyValueType": "String"
        }

    def find_by_text(self, text: str) -> Dict[str, Any]:
        """
        Creates a finder dictionary for finding by text content.
        """
        return {
            "finderType": "ByText",
            "text": text
        }

    def find_by_type(self, widget_type: str) -> Dict[str, Any]:
        """
        Creates a finder dictionary for finding by widget type (class name).
        """
        return {
            "finderType": "ByType",
            "type": widget_type
        }

    def tap(self, finder: Dict[str, Any]):
        """
        Taps the widget found by the given finder.
        """
        logger.info(f"Tapping widget: {finder}")
        self._send_driver_command("tap", finder)

    def enter_text(self, finder: Dict[str, Any], text: str):
        """
        Enters text into the TextField found by the given finder.
        """
        logger.info(f"Entering text '{text}' into widget: {finder}")
        # First focus/tap the textfield
        self.tap(finder)
        # Then send enter_text command
        self._send_driver_command("enter_text", finder, {"text": text})

    def get_text(self, finder: Dict[str, Any]) -> str:
        """
        Retrieves the text of the widget found by the given finder.
        """
        logger.info(f"Getting text from widget: {finder}")
        result = self._send_driver_command("get_text", finder)
        response_data = result.get("response", {})
        return response_data.get("text", "")

    def get_diagnostics_tree(self, finder: Dict[str, Any] = None, subtree_depth=99, include_properties=True):
        """
        Fetches the diagnostics tree from the Flutter app.
        
        Args:
            finder (dict): Finder for the target widget to dump diagnostics for. Defaults to MyApp.
            subtree_depth (int): How deep to traverse the tree
            include_properties (bool): Include widget properties
        
        Returns:
            dict: The JSON tree structure with DiagnosticableTreeNode objects
        """
        logger.info("Fetching diagnostics tree from Flutter app...")
        if finder is None:
            finder = self.find_by_type("MyApp")
        params = {
            "subtreeDepth": subtree_depth,
            "includeProperties": include_properties,
            "diagnosticsType": "widget"
        }
        result = self._send_driver_command("get_diagnostics_tree", finder, params)
        response_data = result.get("response", {})
        if isinstance(response_data, str):
            try:
                return json.loads(response_data)
            except json.JSONDecodeError:
                pass
        return response_data

    def cache_widget_tree(self):
        """
        Fetches and caches the full widget tree in memory.
        Returns the cached tree for immediate use.
        """
        self._cached_tree = self.get_diagnostics_tree()
        return self._cached_tree

    def get_cached_tree(self):
        """Returns the cached widget tree or None if not cached."""
        return getattr(self, '_cached_tree', None)
