class FlutterStaticChecker:
    """
    Static checker for Flutter widgets - mirrors U2StaticChecker.
    Used for fast precondition evaluation in Kea2's fuzzing loop.
    """
    
    def __init__(self, flutter_driver):
        """
        Args:
            flutter_driver: An instance of FlutterDriver from u2_flutter
        """
        self.driver = flutter_driver
        self._cached_tree = None
        self._widget_index = {}  # Index for fast lookups
    
    def set_hierarchy(self, tree_json):
        """
        Set the cached widget tree (like U2StaticChecker.setHierarchy).
        Builds an index for fast lookups.
        """
        self._cached_tree = tree_json
        self._build_index(tree_json)
        return True
    
    def refresh_hierarchy(self):
        """
        Fetch fresh tree from device and cache it.
        """
        tree = self.driver.get_diagnostics_tree()
        return self.set_hierarchy(tree)
    
    def _build_index(self, tree):
        """
        Build an index of widgets by key, text, and type for fast lookups.
        """
        self._widget_index = {
            'by_key': {},
            'by_text': {},
            'by_type': {}
        }
        self._traverse_tree(tree, [])
    
    def _traverse_tree(self, node, path):
        """Recursively traverse the JSON tree and index widgets."""
        if not node:
            return
        
        # Extract properties
        props = node.get('properties', [])
        key = None
        text = None
        widget_type = node.get('description', '')
        
        for prop in props:
            if prop.get('name') == 'key':
                key = prop.get('description')
            if prop.get('name') == 'text':
                text = prop.get('description')
            if prop.get('name') == 'type':
                widget_type = prop.get('description')
        
        # Index by key
        if key:
            self._widget_index['by_key'][key] = {'node': node, 'path': path}
        
        # Index by text
        if text:
            self._widget_index['by_text'][text] = {'node': node, 'path': path}
        
        # Index by type
        if widget_type:
            if widget_type not in self._widget_index['by_type']:
                self._widget_index['by_type'][widget_type] = []
            self._widget_index['by_type'][widget_type].append({'node': node, 'path': path})
        
        # Recurse into children
        for child in node.get('children', []):
            self._traverse_tree(child, path + [node.get('description', '')])
    
    def exists(self, key):
        """
        Check if a widget exists by key (like U2StaticChecker.exists).
        
        Returns:
            bool: True if widget exists
        """
        return key in self._widget_index.get('by_key', {})
    
    def exists_by_text(self, text):
        """
        Check if a widget exists by displayed text.
        
        Returns:
            bool: True if widget exists
        """
        return text in self._widget_index.get('by_text', {})
    
    def exists_by_type(self, widget_type):
        """
        Check if a widget exists by type (e.g., 'ElevatedButton').
        
        Returns:
            bool: True if any widget of this type exists
        """
        return len(self._widget_index.get('by_type', {}).get(widget_type, [])) > 0
    
    def get_text(self, key):
        """
        Get text from a widget by key.
        
        Returns:
            str: The text, or None if not found
        """
        widget_info = self._widget_index.get('by_key', {}).get(key)
        if not widget_info:
            return None
        
        # Look for text property
        props = widget_info['node'].get('properties', [])
        for prop in props:
            if prop.get('name') == 'text':
                return prop.get('description')
        return None
    
    def get_widget_count(self):
        """Return the total number of indexed widgets."""
        return len(self._widget_index.get('by_key', {}))
