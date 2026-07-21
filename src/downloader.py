"""
Downloader module for Auto Downloader.
"""

from pathlib import Path
from typing import Optional

import httpx

from src.logger import logger
from src.display import OLEDDisplay


class Downloader:
    """Download files with progress tracking."""

    def __init__(
        self,
        display: Optional[OLEDDisplay] = None,
        download_dir: str = "downloads",
    ) -> None:

        self.display = display

        self.download_path = Path(download_dir)

        # Create download directory
        self.download_path.mkdir(
            parents=True,
            exist_ok=True,
        )

        # HTTP client
        self.client = httpx.Client(
            timeout=30.0,
            follow_redirects=True,
        )

        logger.info("Downloader initialized")

    def close(self) -> None:
        """Close HTTP client."""

        self.client.close()

        logger.info("Downloader closed")
