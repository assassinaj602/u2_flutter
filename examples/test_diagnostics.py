import sys
import os
import uiautomator2 as u2

# Add parent directory to sys.path so we can import u2_flutter locally
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from u2_flutter import Flutter, with_flutter

class DiagnosticsTester:
    def __init__(self):
        print("Connecting to device...")
        self.d = u2.connect()
        print("Waking screen and starting app...")
        self.d.screen_on()
        self.d.unlock()
        self.d.app_start("com.example.test_app", stop=True)
        import time
        time.sleep(3)

    @with_flutter(local_port=8181)
    def test_tree(self):
        # This should print the full widget tree as JSON
        tree = self.flutter.get_diagnostics_tree()
        print("Tree fetched successfully!")
        print(f"Tree keys: {list(tree.keys()) if tree else 'None'}")
        
        # Test caching
        self.flutter.cache_widget_tree()
        cached = self.flutter.get_cached_tree()
        print(f"Cache exists: {cached is not None}")

if __name__ == "__main__":
    tester = DiagnosticsTester()
    tester.test_tree()
