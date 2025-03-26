import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                           QHBoxLayout, QPushButton, QTextEdit, QLabel,
                           QTableWidget, QTableWidgetItem, QMessageBox)
from PySide6.QtCore import Qt
from website_monitor import WebsiteMonitor
import pandas as pd
from datetime import datetime

class WebsiteMonitorGUI(QMainWindow):
    """
    Main GUI application for the Website Monitor.
    
    This class provides a graphical interface for:
    - Adding websites to monitor
    - Scanning websites for changes
    - Displaying monitoring results
    - Managing the monitoring process
    
    The interface consists of:
    - A text area for entering URLs
    - Add and Scan buttons
    - A status label
    - A results table
    """
    
    def __init__(self):
        """
        Initialize the GUI application.
        
        Creates the main window and initializes the website monitor.
        """
        super().__init__()
        self.monitor = WebsiteMonitor()
        self.init_ui()
        
    def init_ui(self):
        """
        Set up the user interface components.
        
        Creates and arranges all GUI elements including:
        - URL input area
        - Control buttons
        - Status display
        - Results table
        """
        self.setWindowTitle('Website Change Monitor')
        self.setGeometry(100, 100, 800, 600)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Website input section
        input_layout = QHBoxLayout()
        self.url_input = QTextEdit()
        self.url_input.setPlaceholderText("Enter websites (one per line)")
        self.url_input.setMaximumHeight(100)
        input_layout.addWidget(self.url_input)
        
        # Buttons
        button_layout = QVBoxLayout()
        self.add_button = QPushButton('Add Websites')
        self.add_button.clicked.connect(self.add_websites)
        self.scan_button = QPushButton('Scan Websites')
        self.scan_button.clicked.connect(self.scan_websites)
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.scan_button)
        input_layout.addLayout(button_layout)
        
        layout.addLayout(input_layout)
        
        # Status label
        self.status_label = QLabel('Ready')
        layout.addWidget(self.status_label)
        
        # Results table
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(4)
        self.results_table.setHorizontalHeaderLabels(['Website', 'Last Scan', 'Changes Detected', 'Status'])
        layout.addWidget(self.results_table)
        
    def add_websites(self):
        """
        Add websites from the input area to the monitor.
        
        Processes the text input, splits it into URLs, and adds them
        to the website monitor. Updates the display and shows appropriate
        feedback messages.
        """
        urls = self.url_input.toPlainText().strip().split('\n')
        urls = [url.strip() for url in urls if url.strip()]
        if urls:
            self.monitor.add_websites(urls)
            self.status_label.setText(f'Added {len(urls)} websites')
            self.update_table()
        else:
            QMessageBox.warning(self, 'Warning', 'Please enter at least one website URL')
            
    def scan_websites(self):
        """
        Trigger a scan of all monitored websites.
        
        Disables the scan button during the process, performs the scan,
        updates the display, and shows a summary of changes detected.
        """
        self.status_label.setText('Scanning websites...')
        self.scan_button.setEnabled(False)
        changes = self.monitor.scan_websites()
        self.update_table()
        self.scan_button.setEnabled(True)
        self.status_label.setText('Scan complete')
        
        if changes:
            QMessageBox.information(self, 'Changes Detected', 
                                  f'Changes detected in {len(changes)} websites. Check the table for details.')
            
    def update_table(self):
        """
        Update the results table with current monitoring data.
        
        Populates the table with website information including:
        - Website URL
        - Last scan time
        - Number of changes detected
        - Current status
        """
        self.results_table.setRowCount(len(self.monitor.websites))
        for i, (url, data) in enumerate(self.monitor.websites.items()):
            self.results_table.setItem(i, 0, QTableWidgetItem(url))
            self.results_table.setItem(i, 1, QTableWidgetItem(data.get('last_scan', 'Never')))
            self.results_table.setItem(i, 2, QTableWidgetItem(str(data.get('changes', 0))))
            self.results_table.setItem(i, 3, QTableWidgetItem(data.get('status', 'Unknown')))
        self.results_table.resizeColumnsToContents()

def main():
    """
    Main entry point for the application.
    
    Creates and runs the Qt application with the WebsiteMonitorGUI.
    """
    app = QApplication(sys.argv)
    window = WebsiteMonitorGUI()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main() 