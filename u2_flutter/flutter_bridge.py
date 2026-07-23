import re
import time
import logging
import websocket
import adbutils
from typing import Optional

logger = logging.getLogger("u2_flutter.bridge")

class FlutterBridge:
    def __init__(self, device, local_port: int = 8181):
        """
        Initialize the Flutter Bridge.
        
        Args:
            device: A uiautomator2.Device instance.
            local_port: The local port to forward the Dart VM service to.
        """
        self.device = device
        self.local_port = local_port
        self.remote_port: Optional[int] = None
        self.ws: Optional[websocket.WebSocket] = None
        
        # Extract serial if available, or fall back to default
        self.serial = getattr(device, "_serial", None) or getattr(device, "serial", None)
        self.adb = adbutils.adb.device(serial=self.serial) if self.serial else adbutils.adb

    def find_observatory_port(self) -> int:
        """
        Finds the Dart VM Service / Observatory port from the device logcat.
        
        Returns:
            int: The remote VM service port.
        """
        logger.info("Scanning logcat for Dart VM Service URI...")
        # Clear logcat first or read the recent logs
        # We search logcat for the listening address
        logcat_lines = self.device.shell("logcat -d").output
        
        # Matches patterns like:
        # "The Dart VM service is listening on http://127.0.0.1:61234/..."
        # "Observatory listening on http://127.0.0.1:61234/..."
        pattern = re.compile(r"(?:The Dart VM service is listening on|Observatory listening on)\s+http://127.0.0.1:(\d+)/")
        
        for line in reversed(logcat_lines.splitlines()):
            match = pattern.search(line)
            if match:
                port = int(match.group(1))
                logger.info(f"Found Dart VM Service port: {port}")
                return port
                
        # If not found in logcat immediately, wait/check again
        raise RuntimeError("Could not find Dart VM Service port in logcat. Make sure the Flutter app is running in debug or profile mode.")

    def forward_port(self, remote_port: int):
        """
        Sets up ADB port forwarding from local_port to remote_port.
        """
        logger.info(f"Forwarding local tcp:{self.local_port} to remote tcp:{remote_port}")
        try:
            self.adb.forward(f"tcp:{self.local_port}", f"tcp:{remote_port}")
        except Exception as e:
            logger.error(f"Failed to forward port: {e}")
            raise

    def remove_forward(self):
        """
        Removes the ADB port forwarding.
        """
        if self.remote_port:
            logger.info(f"Removing port forwarding for local tcp:{self.local_port}")
            try:
                self.adb.forward_remove(f"tcp:{self.local_port}")
            except Exception as e:
                logger.debug(f"Error removing port forwarding: {e}")

    def attach(self) -> str:
        """
        Finds the VM service port, forwards it, and connects via WebSocket.
        
        Returns:
            str: The WebSocket URL.
        """
        self.remote_port = self.find_observatory_port()
        self.forward_port(self.remote_port)
        
        ws_url = f"ws://127.0.0.1:{self.local_port}/ws"
        logger.info(f"Connecting to WebSocket VM Service: {ws_url}")
        
        # Attempt WebSocket connection with retries
        for attempt in range(5):
            try:
                ws = websocket.WebSocket()
                ws.connect(ws_url, timeout=5)
                self.ws = ws
                logger.info("Successfully connected to Dart VM Service!")
                return ws_url
            except Exception as e:
                logger.warning(f"Connection attempt {attempt + 1} failed: {e}")
                time.sleep(1)
                
        self.remove_forward()
        raise ConnectionError("Failed to connect to Dart VM Service WebSocket after multiple attempts.")

    def detach(self):
        """
        Closes the WebSocket connection and removes port forwarding.
        """
        if self.ws:
            try:
                self.ws.close()
                logger.info("WebSocket connection closed.")
            except Exception as e:
                logger.debug(f"Error closing WebSocket: {e}")
            finally:
                self.ws = None
                
        self.remove_forward()
        self.remote_port = None
