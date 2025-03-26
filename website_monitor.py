import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import os
import hashlib
import json

class WebsiteMonitor:
    """
    A class to monitor websites for content changes.
    
    This class provides functionality to:
    - Track multiple websites
    - Detect changes in website content
    - Maintain a history of changes
    - Persist state between sessions
    
    Attributes:
        websites (dict): Dictionary containing website data
        history_file (str): Path to the CSV file storing scan history
        state_file (str): Path to the JSON file storing current state
    """
    
    def __init__(self):
        """
        Initialize the WebsiteMonitor.
        
        Creates empty website tracking dictionary and sets up file paths
        for state persistence and history tracking.
        """
        self.websites = {}
        self.history_file = 'website_history.csv'
        self.state_file = 'website_state.json'
        self.load_state()
        
    def load_state(self):
        """
        Load the current state from the state file.
        
        If the state file exists, it loads the website data from it.
        If the file doesn't exist, it starts with an empty state.
        """
        if os.path.exists(self.state_file):
            with open(self.state_file, 'r') as f:
                self.websites = json.load(f)
                
    def save_state(self):
        """
        Save the current state to the state file.
        
        Persists the current website data to a JSON file for future sessions.
        """
        with open(self.state_file, 'w') as f:
            json.dump(self.websites, f)
            
    def add_websites(self, urls):
        """
        Add websites to the monitoring list.
        
        Args:
            urls (list): List of website URLs to monitor
            
        Note:
            - Automatically adds 'https://' if protocol is missing
            - Skips duplicate URLs
            - Initializes tracking data for new websites
        """
        for url in urls:
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            if url not in self.websites:
                self.websites[url] = {
                    'last_scan': None,
                    'changes': 0,
                    'status': 'Pending',
                    'last_hash': None
                }
        self.save_state()
        
    def get_page_content(self, url):
        """
        Fetch the content of a webpage.
        
        Args:
            url (str): The URL to fetch
            
        Returns:
            str: The webpage content as text, or None if the request fails
            
        Note:
            - Uses a 10-second timeout for requests
            - Handles various types of request errors
        """
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.text
        except Exception as e:
            return None
            
    def calculate_hash(self, content):
        """
        Calculate MD5 hash of webpage content.
        
        Args:
            content (str): The webpage content to hash
            
        Returns:
            str: MD5 hash of the content, or None if content is None
        """
        if content is None:
            return None
        return hashlib.md5(content.encode()).hexdigest()
        
    def scan_websites(self):
        """
        Scan all monitored websites for changes.
        
        Returns:
            list: URLs of websites where changes were detected
            
        Note:
            - Updates status and change count for each website
            - Records scan time and detected changes
            - Saves state and updates history after scanning
        """
        changes = []
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        for url in self.websites:
            content = self.get_page_content(url)
            if content is None:
                self.websites[url]['status'] = 'Error'
                continue
                
            current_hash = self.calculate_hash(content)
            last_hash = self.websites[url]['last_hash']
            
            if last_hash is None:
                self.websites[url]['last_hash'] = current_hash
                self.websites[url]['status'] = 'Initial scan'
                self.websites[url]['last_scan'] = current_time
                continue
                
            if current_hash != last_hash:
                self.websites[url]['changes'] += 1
                self.websites[url]['last_hash'] = current_hash
                self.websites[url]['status'] = 'Changed'
                changes.append(url)
            else:
                self.websites[url]['status'] = 'No changes'
                
            self.websites[url]['last_scan'] = current_time
            
        self.save_state()
        self.update_history(changes)
        return changes
        
    def update_history(self, changed_urls):
        """
        Update the history file with scan results.
        
        Args:
            changed_urls (list): URLs of websites where changes were detected
            
        Note:
            - Creates new history file if it doesn't exist
            - Appends new scan results to existing history
            - Records timestamp, changed websites, and total websites
        """
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Create new history entry
        history_data = {
            'timestamp': current_time,
            'changed_websites': ','.join(changed_urls),
            'total_websites': len(self.websites)
        }
        
        # Load existing history or create new DataFrame
        if os.path.exists(self.history_file):
            df = pd.read_csv(self.history_file)
        else:
            df = pd.DataFrame(columns=['timestamp', 'changed_websites', 'total_websites'])
            
        # Append new data
        df = pd.concat([df, pd.DataFrame([history_data])], ignore_index=True)
        
        # Save updated history
        df.to_csv(self.history_file, index=False) 