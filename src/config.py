"""
Application configuration.
"""

from pathlib import Path

# Project information
APP_NAME = "Auto Downloader"
APP_VERSION = "1.0.0"

# Download settings
DOWNLOAD_PATH = Path("downloads")
RETRY_COUNT = 3
DOWNLOAD_TIMEOUT = 30

# SMS settings
SMS_CHECK_INTERVAL = 5
DELETE_SMS_AFTER_DOWNLOAD = True

# Display settings
OLED_ENABLED = True

# Log settings
LOG_DIRECTORY = Path("logs")
LOG_LEVEL = "INFO"

# Network settings
NETWORK_CHECK_INTERVAL = 10

# Modem settings
MODEM_PORT = "/dev/ttyUSB2"
MODEM_BAUDRATE = 115200
