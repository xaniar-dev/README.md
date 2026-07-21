"""
Main entry point for Auto Downloader.
"""

from src.logger import logger
from src.modem import Modem
from src.display import OLEDDisplay


def main():
    """Start the application."""

    logger.info("Application started")

    # Initialize OLED display
    display = OLEDDisplay()
    display.show_message("Starting...", "Please wait")

    # Initialize modem
    modem = Modem()

    # Check modem connection
    modem_status = modem.test()
    logger.info(modem_status)

    # Read signal strength
    signal = modem.signal()
    logger.info(signal)

    # Show ready message
    display.show_message("System Ready", "Waiting SMS")

    logger.info("System is ready")


if __name__ == "__main__":
    main()
