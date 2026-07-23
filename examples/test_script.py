import os
import sys
import logging
import uiautomator2 as u2

# Add parent directory to sys.path so we can import u2_flutter locally
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from u2_flutter import Flutter, with_flutter

# Configure logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("test_script")

# Path to the compiled APK
APK_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "test_app",
    "build",
    "app",
    "outputs",
    "flutter-apk",
    "app-debug.apk"
)
PACKAGE_NAME = "com.example.test_app"

class FlutterAppTest:
    def __init__(self):
        # Connect to device (automatically picks the connected device/emulator)
        logger.info("Connecting to Android device...")
        self.d = u2.connect()
        logger.info(f"Connected to device: {self.d.device_info}")

    def setup_app(self):
        if not os.path.exists(APK_PATH):
            raise FileNotFoundError(f"Could not find APK at {APK_PATH}. Run 'flutter build apk --debug' first.")
            
        logger.info("Waking screen and unlocking...")
        self.d.screen_on()
        self.d.unlock()

        logger.info(f"Installing {APK_PATH}...")
        self.d.app_install(APK_PATH)
        
        logger.info(f"Starting {PACKAGE_NAME}...")
        self.d.app_start(PACKAGE_NAME, stop=True)
        
        # Wait a moment for the app to initialize and VM service port to print in logcat
        import time
        time.sleep(3)

    # Use the with_flutter decorator to automatically attach/detach
    @with_flutter(local_port=8181)
    def run_test_scenario(self):
        logger.info("Starting test scenario...")
        
        # 1. Find the TextField by key 'username_input' and enter text
        logger.info("Entering text 'testuser' into username_input...")
        username_field = self.flutter.find_by_key("username_input")
        username_field.enter_text("testuser")
        
        # 2. Find the Submit Button by key 'submit_btn' and tap it
        logger.info("Tapping submit button...")
        submit_btn = self.flutter.find_by_key("submit_btn")
        submit_btn.tap()
        
        # Allow time for UI state update
        import time
        time.sleep(1)
        
        # 3. Verify the text changed to 'Hello, testuser!'
        greeting_text = self.flutter.find_by_key("greeting_text").text
        logger.info(f"Greeting text found: '{greeting_text}'")
        assert greeting_text == "Hello, testuser!", f"Expected 'Hello, testuser!' but got '{greeting_text}'"
        
        # 4. Verify the counter incremented to 1
        counter_text = self.flutter.find_by_key("counter_text").text
        logger.info(f"Counter text found: '{counter_text}'")
        assert "1 times" in counter_text, f"Expected '1 times' in counter text but got '{counter_text}'"
        
        logger.info("All assertions passed successfully!")

def main():
    test = FlutterAppTest()
    try:
        test.setup_app()
        test.run_test_scenario()
        logger.info("Test Run Completed: SUCCESS")
    except Exception as e:
        logger.error(f"Test Run Completed: FAILED with error: {e}", exc_info=True)

if __name__ == "__main__":
    main()
