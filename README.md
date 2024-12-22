# System Performance Monitoring Script

## Overview
This Python script monitors system performance and generates a report. It provides insights into:
- CPU usage percentage
- Memory usage (total, used, free, and percentage)
- Disk space usage (total, used, free, and percentage for each mounted filesystem)
- Top 5 CPU-consuming processes

The script also includes an alert mechanism to notify users of high resource utilization and supports customization of monitoring intervals and output formats.

---

## Features
- **Real-Time Monitoring**: Continuously tracks system performance at user-defined intervals.
- **Alerts**:
  - CPU usage > 80%
  - Memory usage > 75%
  - Disk space usage > 90%

- **Customizable Output**:
  - Formats: Text, JSON, or CSV
  - User-defined file names
- **Error Handling**: Handles invalid inputs, permission issues, and system interruptions gracefully.

---

## Prerequisites
1. **Python 3.x**: Ensure Python is installed on your system.
   python3 --version
2. **Install Required Library**:
   pip install psutil

---

## Usage
### Basic Execution
Run the script with default settings:

python3 monitor_system.py

- Default interval: 5 seconds
- Default format: Text
- Default file name: `system_report.txt`

#### Examples:
1. Monitor every 10 seconds and output a JSON file:

    python monitor_system.py --interval 10 --format csv --output system_report  

   - Output: `system_report.json`

2. Monitor every 15 seconds and output a CSV file:

    python monitor_system.py --interval 15 --format json --output system_report

   - Output: `system_report.csv`

---

## Stopping the Script
To stop monitoring, press:
```plaintext
Ctrl + C
```
The script will terminate gracefully.

---





