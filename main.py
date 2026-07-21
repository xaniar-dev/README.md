"""
Main entry point for Auto Downloader.
"""

import time

from src.display import OLEDDisplay
from src.logger import logger
from src.modem import Modem
from src.queue_manager import DownloadQueue
from src.sms import SMSReader


def main():
    """Start Auto Downloader."""

    logger.info("Application started")

    # Initialize display
    display = OLEDDisplay()
    display.show_message("Starting...", "Please wait")

    # Initialize modem
    modem = Modem()

    # Initialize SMS reader
    sms = SMSReader(modem)
    sms.initialize()

    # Initialize download queue
    download_queue = DownloadQueue()

    display.show_message("System Ready", "Waiting SMS")

    logger.info("Waiting for SMS")

    while True:

        messages = sms.read_messages()

        url = sms.extract_url(messages)

        if url:

            download_queue.add(url)

            logger.info(f"URL added: {url}")

            display.show_message(
                "Queued",
                f"{download_queue.size()} File(s)"
            )

        time.sleep(5)


if __name__ == "__main__":
    main()
