from src.modem import Modem
from src.display import OLEDDisplay


def main():
    # Start application
    print("Starting Auto Downloader...")

    # Initialize OLED display
    display = OLEDDisplay()
    display.show_message("Starting...", "Please wait")

    # Initialize modem
    modem = Modem()

    # Check modem connection
    print(modem.test())

    # Read signal strength
    print(modem.signal())

    # Show ready status
    display.show_message("System Ready", "Waiting SMS")


if __name__ == "__main__":
    main()
