import functools
import logging
from typing import Optional
from .flutter_bridge import FlutterBridge
from .flutter_driver import FlutterDriver

logger = logging.getLogger("u2_flutter.plugin")

class FlutterElement:
    def __init__(self, driver: FlutterDriver, finder: dict):
        self.driver = driver
        self.finder = finder

    def tap(self):
        """Tap this widget."""
        self.driver.tap(self.finder)
        return self

    def enter_text(self, text: str):
        """Enter text into this widget (e.g. a TextField)."""
        self.driver.enter_text(self.finder, text)
        return self

    def get_text(self) -> str:
        """Get the text of this widget (method wrapper)."""
        return self.text

    @property
    def text(self) -> str:
        """Get the text of this widget."""
        return self.driver.get_text(self.finder)

    def __len__(self):
        # Fallback length for list-like compatibility in tests
        return 1

    def __getitem__(self, index):
        if index == 0:
            return self
        raise IndexError("FlutterElement index out of range")

    def scroll(self, dx: int, dy: int, duration_ms: int = 500):
        """Scrolls this widget."""
        self.driver.scroll(self.finder, dx, dy, duration_ms)
        return self

    def wait_for(self, timeout_ms: int = 5000) -> bool:
        """Waits for this widget to appear."""
        return self.driver.wait_for(self.finder, timeout_ms)


class Flutter:
    def __init__(self, device, local_port: int = 8181):
        """
        Initialize the Flutter plugin.
        
        Args:
            device: A uiautomator2.Device instance.
            local_port: The local port for port forwarding.
        """
        self.device = device
        self.bridge = FlutterBridge(device, local_port=local_port)
        self.driver = FlutterDriver(self.bridge)

    def attach(self) -> "Flutter":
        """
        Establish connection to the Flutter VM service.
        """
        self.bridge.attach()
        return self

    def detach(self):
        """
        Close the connection to the Flutter VM service.
        """
        self.bridge.detach()

    def find_by_key(self, key: str) -> FlutterElement:
        """
        Find widget by key.
        """
        finder = self.driver.find_by_key(key)
        return FlutterElement(self.driver, finder)

    def find_by_text(self, text: str) -> FlutterElement:
        """
        Find widget by text.
        """
        finder = self.driver.find_by_text(text)
        return FlutterElement(self.driver, finder)

    def find_by_type(self, widget_type: str) -> FlutterElement:
        """
        Find widget by type.
        """
        finder = self.driver.find_by_type(widget_type)
        return FlutterElement(self.driver, finder)

    def get_diagnostics_tree(self, finder: Optional[dict] = None, subtree_depth=99, include_properties=True) -> dict:
        """
        Fetch the diagnostics tree from the Flutter app.
        """
        return self.driver.get_diagnostics_tree(finder=finder, subtree_depth=subtree_depth, include_properties=include_properties)

    def cache_widget_tree(self) -> dict:
        """
        Fetches and caches the full widget tree in memory.
        """
        return self.driver.cache_widget_tree()

    def get_cached_tree(self) -> Optional[dict]:
        """
        Returns the cached widget tree or None.
        """
        return self.driver.get_cached_tree()

    def scroll(self, finder: dict, dx: int, dy: int, duration_ms: int = 500):
        """Scrolls the target widget."""
        self.driver.scroll(finder, dx, dy, duration_ms)
        return self

    def wait_for(self, finder: dict, timeout_ms: int = 5000) -> bool:
        """Waits for the target widget to appear."""
        return self.driver.wait_for(finder, timeout_ms)


def with_flutter(local_port: int = 8181):
    """
    Decorator for test functions to handle Flutter bridge lifecycle.
    Assumes the first argument of the test function (or 'self') has a 'd' attribute 
    which is a uiautomator2 Device instance, and assigns a 'flutter' attribute to it.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Try to get the device instance from args
            # Typically used on test methods, where args[0] is 'self', and self.d is the u2 device
            test_obj = args[0] if args else None
            if not test_obj or not hasattr(test_obj, "d"):
                raise AttributeError("The decorated function must be a method of a class containing a uiautomator2 Device instance at 'self.d'.")
            
            # Instantiate Flutter plugin
            flutter_plugin = Flutter(test_obj.d, local_port=local_port)
            test_obj.flutter = flutter_plugin
            
            logger.info("Attaching Flutter driver...")
            flutter_plugin.attach()
            
            try:
                return func(*args, **kwargs)
            finally:
                logger.info("Detaching Flutter driver...")
                flutter_plugin.detach()
                
        return wrapper
    return decorator
