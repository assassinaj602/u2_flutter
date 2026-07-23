import unittest
from unittest.mock import Mock
import sys
import os

# Add parent directory to sys.path so we can import kea2_integration locally
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kea2_integration.flutter_static_checker import FlutterStaticChecker

class TestFlutterStaticChecker(unittest.TestCase):
    def setUp(self):
        # Mock the FlutterDriver
        self.mock_driver = Mock()
        
        # Sample JSON tree (matching get_diagnostics_tree format)
        self.sample_tree = {
            "type": "DiagnosticableTreeNode",
            "description": "MaterialApp",
            "properties": [],
            "children": [
                {
                    "type": "DiagnosticableTreeNode",
                    "description": "Scaffold",
                    "properties": [],
                    "children": [
                        {
                            "type": "DiagnosticableTreeNode",
                            "description": "Column",
                            "properties": [],
                            "children": [
                                {
                                    "type": "DiagnosticableTreeNode",
                                    "description": "TextField",
                                    "properties": [
                                        {"name": "key", "description": "username_input"},
                                        {"name": "text", "description": ""},
                                        {"name": "type", "description": "TextField"}
                                    ],
                                    "children": []
                                },
                                {
                                    "type": "DiagnosticableTreeNode",
                                    "description": "ElevatedButton",
                                    "properties": [
                                        {"name": "key", "description": "submit_btn"},
                                        {"name": "text", "description": "Submit"},
                                        {"name": "type", "description": "ElevatedButton"}
                                    ],
                                    "children": []
                                },
                                {
                                    "type": "DiagnosticableTreeNode",
                                    "description": "Text",
                                    "properties": [
                                        {"name": "key", "description": "greeting_text"},
                                        {"name": "text", "description": "Hello, testuser!"},
                                        {"name": "type", "description": "Text"}
                                    ],
                                    "children": []
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        
        self.checker = FlutterStaticChecker(self.mock_driver)
    
    def test_set_hierarchy_and_index(self):
        """Test that hierarchy is properly set and indexed."""
        result = self.checker.set_hierarchy(self.sample_tree)
        self.assertTrue(result)
        self.assertEqual(self.checker.get_widget_count(), 3)
    
    def test_exists_by_key(self):
        """Test checking existence by key."""
        self.checker.set_hierarchy(self.sample_tree)
        self.assertTrue(self.checker.exists("username_input"))
        self.assertTrue(self.checker.exists("submit_btn"))
        self.assertTrue(self.checker.exists("greeting_text"))
        self.assertFalse(self.checker.exists("non_existent_key"))
    
    def test_exists_by_text(self):
        """Test checking existence by text."""
        self.checker.set_hierarchy(self.sample_tree)
        self.assertTrue(self.checker.exists_by_text("Submit"))
        self.assertTrue(self.checker.exists_by_text("Hello, testuser!"))
        self.assertFalse(self.checker.exists_by_text("Goodbye"))
    
    def test_exists_by_type(self):
        """Test checking existence by widget type."""
        self.checker.set_hierarchy(self.sample_tree)
        self.assertTrue(self.checker.exists_by_type("ElevatedButton"))
        self.assertTrue(self.checker.exists_by_type("TextField"))
        self.assertTrue(self.checker.exists_by_type("Text"))
        self.assertFalse(self.checker.exists_by_type("NonExistentWidget"))
    
    def test_get_text(self):
        """Test retrieving text from a widget by key."""
        self.checker.set_hierarchy(self.sample_tree)
        self.assertEqual(self.checker.get_text("submit_btn"), "Submit")
        self.assertEqual(self.checker.get_text("greeting_text"), "Hello, testuser!")
        self.assertEqual(self.checker.get_text("username_input"), "")
        self.assertIsNone(self.checker.get_text("non_existent"))

if __name__ == "__main__":
    unittest.main()
