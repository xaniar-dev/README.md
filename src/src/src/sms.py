"""
SMS reader for EC25 modem.
"""

import re
from typing import Optional

from src.modem import Modem


class SMSReader:
    """Read SMS messages from EC25 modem."""

    def __init__(self, modem: Modem):
        self.modem = modem

    def initialize(self) -> None:
        """Configure modem for text mode SMS."""
        self.modem.send("ATE0")
        self.modem.send("AT+CMGF=1")

    def read_messages(self) -> str:
        """Read all SMS messages."""
        return self.modem.send('AT+CMGL="ALL"', delay=2)

    def extract_url(self, text: str) -> Optional[str]:
        """Extract the first HTTP or HTTPS URL."""
        match = re.search(r"https?://\\S+", text)

        if match:
            return match.group(0)

        return None
