"""
Logging configuration for Auto Downloader.
"""

import logging
from pathlib import Path

# Create log directory if it does not exist
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

# Configure logging
logging.basicConfig(
    filename=LOG_DIR / "auto_downloader.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger("AutoDownloader")
