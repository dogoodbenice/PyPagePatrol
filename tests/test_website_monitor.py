import unittest
import os
import json
import pandas as pd
from datetime import datetime
from unittest.mock import patch, MagicMock
from website_monitor import WebsiteMonitor

class TestWebsiteMonitor(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test."""
        self.test_state_file = 'test_state.json'
        self.test_history_file = 'test_history.csv'
        self.monitor = WebsiteMonitor()
        self.monitor.state_file = self.test_state_file
        self.monitor.history_file = self.test_history_file
        
    def tearDown(self):
        """Clean up test files after each test."""
        if os.path.exists(self.test_state_file):
            os.remove(self.test_state_file)
        if os.path.exists(self.test_history_file):
            os.remove(self.test_history_file)
            
    def test_add_websites(self):
        """Test adding websites to the monitor."""
        urls = ['example.com', 'https://test.com']
        self.monitor.add_websites(urls)
        
        # Check if websites were added correctly
        self.assertEqual(len(self.monitor.websites), 2)
        self.assertIn('https://example.com', self.monitor.websites)
        self.assertIn('https://test.com', self.monitor.websites)
        
        # Check if state was saved
        self.assertTrue(os.path.exists(self.test_state_file))
        
    def test_duplicate_websites(self):
        """Test handling of duplicate website entries."""
        urls = ['example.com', 'example.com']
        self.monitor.add_websites(urls)
        self.assertEqual(len(self.monitor.websites), 1)
        
    @patch('requests.get')
    def test_scan_websites_success(self, mock_get):
        """Test successful website scanning."""
        # Mock successful response
        mock_response = MagicMock()
        mock_response.text = '<html>Test content</html>'
        mock_get.return_value = mock_response
        
        # Add test website
        self.monitor.add_websites(['example.com'])
        
        # Perform scan
        changes = self.monitor.scan_websites()
        
        # Verify results
        self.assertEqual(len(changes), 0)  # First scan should not detect changes
        self.assertEqual(self.monitor.websites['https://example.com']['status'], 'Initial scan')
        
    @patch('requests.get')
    def test_scan_websites_changes(self, mock_get):
        """Test detection of website changes."""
        # Add test website
        self.monitor.add_websites(['example.com'])
        
        # Mock first scan
        mock_response1 = MagicMock()
        mock_response1.text = '<html>Original content</html>'
        mock_get.return_value = mock_response1
        self.monitor.scan_websites()
        
        # Mock second scan with different content
        mock_response2 = MagicMock()
        mock_response2.text = '<html>Changed content</html>'
        mock_get.return_value = mock_response2
        changes = self.monitor.scan_websites()
        
        # Verify changes were detected
        self.assertEqual(len(changes), 1)
        self.assertEqual(self.monitor.websites['https://example.com']['changes'], 1)
        
    @patch('requests.get')
    def test_scan_websites_error(self, mock_get):
        """Test handling of website scanning errors."""
        # Mock failed request
        mock_get.side_effect = Exception('Connection error')
        
        # Add test website
        self.monitor.add_websites(['example.com'])
        
        # Perform scan
        changes = self.monitor.scan_websites()
        
        # Verify error handling
        self.assertEqual(self.monitor.websites['https://example.com']['status'], 'Error')
        
    def test_history_tracking(self):
        """Test CSV history file creation and updates."""
        # Add test website
        self.monitor.add_websites(['example.com'])
        
        # Perform scan
        self.monitor.scan_websites()
        
        # Verify history file
        self.assertTrue(os.path.exists(self.test_history_file))
        df = pd.read_csv(self.test_history_file)
        self.assertEqual(len(df), 1)
        self.assertEqual(df['total_websites'].iloc[0], 1)
        
    def test_state_persistence(self):
        """Test saving and loading of website state."""
        # Add test website
        self.monitor.add_websites(['example.com'])
        
        # Create new monitor instance
        new_monitor = WebsiteMonitor()
        new_monitor.state_file = self.test_state_file
        new_monitor.load_state()
        
        # Verify state was loaded correctly
        self.assertEqual(len(new_monitor.websites), 1)
        self.assertIn('https://example.com', new_monitor.websites)

if __name__ == '__main__':
    unittest.main() 