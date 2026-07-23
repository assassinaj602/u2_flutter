import time
import uiautomator2 as u2
from u2_flutter import with_flutter

class ManualTester:
    def __init__(self):
        print("[Device] Connecting to Android device...")
        self.d = u2.connect()
        print(f"[Device] Connected to device info: {self.d.info}")
        
        # Turn screen on and unlock the device
        print("[Device] Waking up screen and unlocking...")
        self.d.screen_on()
        self.d.unlock()
        
        print("[Device] Starting com.example.test_app...")
        self.d.app_start("com.example.test_app", stop=True)
        time.sleep(3) # Wait for logcat logs to populate
        
    @with_flutter(local_port=8181)
    def test_interactive(self):
        print("\n[Test] Testing Flutter interactions...")
        
        # Test 1: Find by key
        print("\n[Test 1] Finding widget by key...")
        username_field = self.flutter.find_by_key("username_input")
        print(f"   Success: Found username_input finder: {username_field}")
        
        # Test 2: Enter text
        print("\n[Test 2] Entering text...")
        username_field.enter_text("manual_test_user")
        print("   Success: Text entered")
        
        # Test 3: Find and tap button
        print("\n[Test 3] Finding and tapping button...")
        submit_btn = self.flutter.find_by_key("submit_btn")
        submit_btn.tap()
        print("   Success: Button tapped")
        
        # Wait a moment for UI to rebuild after tap
        time.sleep(1)
        
        # Test 4: Get text
        print("\n[Test 4] Getting text from widget...")
        greeting = self.flutter.find_by_key("greeting_text").get_text()
        print(f"   Success: Greeting: {greeting}")
        
        # Test 5: Find by text
        print("\n[Test 5] Finding widget by displayed text...")
        hello_widget = self.flutter.find_by_text("Hello")
        print(f"   Success: Found by text: {hello_widget}")
        
        # Test 6: Find by type
        print("\n[Test 6] Finding widget by type...")
        buttons = self.flutter.find_by_type("ElevatedButton")
        print(f"   Success: Found {len(buttons)} buttons")
        
        print("\nAll manual tests passed!")
        return True

if __name__ == "__main__":
    tester = ManualTester()
    tester.test_interactive()
