"""
Main entry point for Auto Downloader.
"""

import time

from src.display import OLEDDisplay
from src.logger import logger
from src.modem import Modem
from src.queue_manager import DownloadQueue
from src.sms import SMSReader
from download_queue import DownloadQueue

def main():
    """Start Auto Downloader."""

    logger.info("Application started")

    # Initialize display
    display = OLEDDisplay()
    display.show_message("Starting...", "Please wait")

    # Initialize modem
    modem = Modem()

    # Check modem status
    logger.info(modem.test())
    logger.info(modem.signal())

    # Initialize SMS reader
    sms = SMSReader(modem)
    sms.initialize()

    # Initialize download queue
    download_queue = DownloadQueue()

    display.show_message("System Ready", "Waiting SMS")
    logger.info("System is ready")

    while True:
        try:
            # Read all SMS messages
            messages = sms.read_messages()

            # Get SMS index
            message_id = sms.extract_message_id(messages)

            if (
                message_id is not None
                and not sms.is_processed(message_id)
            ):

                # Extract download URL
                url = sms.extract_url(messages)

                if url:

                    # Add URL to queue
                    download_queue.add(url)

                    # Mark SMS as processed
                    sms.mark_processed(message_id)

                    # Delete SMS from modem
                    sms.delete_message(message_id)

                    logger.info(f"URL queued: {url}")

                    display.show_message(
                        "Queued",
                        f"{download_queue.size()} File(s)"
                    )

            # Check for new SMS every 5 seconds
            time.sleep(5)

        except Exception as error:

            logger.error(f"Main loop error: {error}")

            display.show_message(
                "System Error",
                "Check Logs"
            )

            time.sleep(5)


if __name__ == "__main__":
    main()
