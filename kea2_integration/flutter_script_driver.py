class FlutterScriptDriver:
    """
    Script driver for Flutter widgets - mirrors U2ScriptDriver.
    Used for actions and assertions in Kea2's fuzzing loop.
    """
    
    def __init__(self, flutter_driver):
        """
        Args:
            flutter_driver: An instance of FlutterDriver/Flutter from u2_flutter
        """
        self.driver = flutter_driver
    
    def tap(self, finder):
        """
        Tap a widget using the provided finder.
        
        Args:
            finder (dict): Finder configuration e.g.,
                {"type": "key", "value": "submit_btn"}
        """
        key = self._extract_key(finder)
        if key:
            # If our driver is the wrapper Flutter class, it exposes find_by_key directly.
            # Otherwise we use find_by_key and tap.
            if hasattr(self.driver, 'find_by_key'):
                self.driver.find_by_key(key).tap()
            else:
                finder_dict = self.driver.find_by_key(key)
                self.driver.tap(finder_dict)
        else:
            raise ValueError(f"Invalid finder: {finder}")
    
    def input(self, finder, text):
        """
        Enter text into a TextField.
        
        Args:
            finder (dict): Finder configuration
            text (str): Text to enter
        """
        key = self._extract_key(finder)
        if key:
            if hasattr(self.driver, 'find_by_key'):
                self.driver.find_by_key(key).enter_text(text)
            else:
                finder_dict = self.driver.find_by_key(key)
                self.driver.enter_text(finder_dict, text)
        else:
            raise ValueError(f"Invalid finder: {finder}")
    
    def get_text(self, finder):
        """
        Get text from a widget.
        
        Args:
            finder (dict): Finder configuration
        
        Returns:
            str: The text content of the widget
        """
        key = self._extract_key(finder)
        if key:
            if hasattr(self.driver, 'find_by_key'):
                return self.driver.find_by_key(key).text
            else:
                finder_dict = self.driver.find_by_key(key)
                return self.driver.get_text(finder_dict)
        else:
            raise ValueError(f"Invalid finder: {finder}")
    
    def scroll(self, finder, dx=0, dy=-100, duration=500):
        """
        Scroll a list or scrollable widget.
        
        Args:
            finder (dict): Finder configuration
            dx (int): Horizontal scroll amount
            dy (int): Vertical scroll amount
            duration (int): Scroll duration in milliseconds
        """
        key = self._extract_key(finder)
        if key:
            if hasattr(self.driver, 'find_by_key'):
                self.driver.find_by_key(key).scroll(dx, dy, duration)
            else:
                finder_dict = self.driver.find_by_key(key)
                self.driver.scroll(finder_dict, dx, dy, duration)
        else:
            raise ValueError(f"Invalid finder: {finder}")
    
    def wait_for(self, finder, timeout=5000):
        """
        Wait for a widget to appear.
        
        Args:
            finder (dict): Finder configuration
            timeout (int): Timeout in milliseconds
        
        Returns:
            bool: True if widget appeared, False if timeout
        """
        key = self._extract_key(finder)
        if key:
            if hasattr(self.driver, 'find_by_key'):
                return self.driver.find_by_key(key).wait_for(timeout)
            else:
                finder_dict = self.driver.find_by_key(key)
                return self.driver.wait_for(finder_dict, timeout)
        else:
            return False
    
    def _extract_key(self, finder):
        """Extract the key from a finder dict."""
        if finder.get('type') == 'key':
            return finder.get('value')
        elif finder.get('type') == 'text':
            # For text finder, map 'value' directly
            return finder.get('value')
        elif finder.get('type') == 'type':
            # For type finder, map 'value' directly
            return finder.get('value')
        return None
