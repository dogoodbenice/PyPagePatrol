# PyPagePatrol

A Python-based website change monitoring tool with a graphical user interface. This tool allows you to track changes across multiple websites and maintain a history of detected changes.

## Development Status

⚠️ **ALPHA VERSION** - This is an unstable development version. Not recommended for production use.

### Known Issues
- Website change detection may be unstable due to:
  - Dynamic content loading
  - Anti-bot measures on some websites
  - Rate limiting from target websites
  - SSL certificate verification issues
- GUI may freeze during long scans
- Some websites may block automated requests
- State persistence may occasionally fail
- Memory usage can grow with large websites

## System Requirements

### Operating System
- macOS 10.14 or later (tested on macOS 14.3)
- Other operating systems are not currently supported

### Hardware Requirements
- Minimum 4GB RAM
- 500MB free disk space
- Internet connection for website monitoring

### Software Requirements
- Python 3.8 or higher
- PySide6 (Qt bindings)
- requests
- beautifulsoup4
- pandas

## Features

- Add multiple websites to monitor
- Scan websites for changes
- Track change history in a CSV file
- Graphical user interface for easy interaction
- Persistent storage of website states
- Automatic HTTPS protocol handling

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/PyPagePatrol.git
cd PyPagePatrol
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the application:
```bash
python main.py
```

2. Enter the websites you want to monitor (one per line) in the text area
3. Click "Add Websites" to add them to the monitoring list
4. Click "Scan Websites" to check for changes
5. View the results in the table below

## Data Storage

The tool maintains two files:
- `website_state.json`: Stores the current state of monitored websites
- `website_history.csv`: Contains a history of all scans and detected changes

## Developer Guide

### Project Structure

```
PyPagePatrol/
├── main.py              # Main GUI application
├── website_monitor.py   # Core monitoring logic
├── tests/              # Test suite
│   └── test_website_monitor.py
├── requirements.txt    # Project dependencies
└── README.md          # Project documentation
```

### Running Tests

The project includes a comprehensive test suite. To run the tests:

```bash
python -m unittest tests/test_website_monitor.py
```

### Key Components

#### WebsiteMonitor Class
- Core class handling website monitoring logic
- Manages website state and history
- Detects changes using MD5 hashing
- Persists data between sessions

#### WebsiteMonitorGUI Class
- PySide6-based graphical interface
- Handles user input and display
- Manages the monitoring process
- Provides real-time feedback

### Adding New Features

1. **Modifying the Core Logic**
   - Add new methods to `WebsiteMonitor` class
   - Update state management as needed
   - Add appropriate tests

2. **Extending the GUI**
   - Add new UI elements in `WebsiteMonitorGUI`
   - Connect new functionality to existing methods
   - Update the table display if needed

3. **Data Storage**
   - Modify state and history file formats as needed
   - Update save/load methods accordingly

### Best Practices

1. **Code Style**
   - Follow PEP 8 guidelines
   - Use type hints where appropriate
   - Document all public methods

2. **Testing**
   - Write tests for new features
   - Use mocking for external dependencies
   - Maintain test coverage

3. **Error Handling**
   - Use appropriate exception handling
   - Provide user-friendly error messages
   - Log errors when necessary

### Common Issues

1. **Website Access**
   - Some websites may block automated requests
   - Consider adding user-agent headers
   - Handle SSL certificate issues

2. **Performance**
   - Large websites may slow down scanning
   - Consider implementing rate limiting
   - Cache results when appropriate

3. **State Management**
   - Handle corrupted state files
   - Implement backup mechanisms
   - Version control for state format

## Future Development

### Planned Features
- Support for more operating systems
- Improved change detection algorithms
- Better handling of dynamic content
- Rate limiting and request queuing
- User authentication for protected websites
- Email notifications for changes
- Custom change detection rules

### Contributing
Contributions are welcome! Please read the developer guide and submit pull requests for any improvements.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
