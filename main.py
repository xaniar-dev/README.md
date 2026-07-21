"""
Main entry point for Auto Downloader.
"""

import time

from src.display import OLEDDisplay
from src.logger import logger
from src.modem import Modem
from src.sms import SMSReader
from src.downloader import Downloader
from download_queue import DownloadQueue


def main():
    """Start Auto Downloader."""

    logger.info("Application started")

    # Initialize display
    display = OLEDDisplay()
    display.show_message("Starting...", "Please wait")

    # Initialize modem
    modem = Modem()

    logger.info(modem.test())
    logger.info(modem.signal())

    # Initialize downloader
    downloader = Downloader(display=display)

    # Initialize download queue
    download_queue = DownloadQueue(downloader)
    download_queue.start()

    # Initialize SMS reader
    sms = SMSReader(modem)
    sms.initialize()

    display.show_message("System Ready", "Waiting SMS")
    logger.info("System is ready")

    while True:
        try:
            messages = sms.read_messages()

            message_id = sms.extract_message_id(messages)

            if (
                message_id is not None
                and not sms.is_processed(message_id)
            ):

                url = sms.extract_url(messages)

                if url:

                    download_queue.add(url)

                    sms.mark_processed(message_id)

                    sms.delete_message(message_id)

                    logger.info(f"URL queued: {url}")

                    display.show_message(
                        "Queued",
                        f"{download_queue.pending()} File(s)"
                    )

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
