"""
SMS reader for EC25 modem.
"""

import re
from typing import Optional, Set

from src.modem import Modem


class SMSReader:
    """Read SMS messages from EC25 modem."""

    def __init__(self, modem: Modem):
        self.modem = modem
        self.processed_messages: Set[int] = set()

    def initialize(self) -> None:
        """Configure modem for text mode SMS."""
        self.modem.send("ATE0")
        self.modem.send("AT+CMGF=1")

    def read_messages(self) -> str:
        """Read all SMS messages."""
        return self.modem.send('AT+CMGL="ALL"', delay=2)

    def extract_url(self, text: str) -> Optional[str]:
        """Extract first HTTP or HTTPS URL."""
        match = re.search(r"https?://\S+", text)
        return match.group(0) if match else None

    def extract_message_id(self, text: str) -> Optional[int]:
        """Extract SMS index from modem response."""
        match = re.search(r"\+CMGL:\s*(\d+)", text)

        if match:
            return int(match.group(1))

        return None

    def is_processed(self, message_id: int) -> bool:
        """Check whether SMS has already been processed."""
        return message_id in self.processed_messages

    def mark_processed(self, message_id: int) -> None:
        """Mark SMS as processed."""
        self.processed_messages.add(message_id)

    def delete_message(self, message_id: int) -> None:
        """Delete SMS from modem memory."""
        self.modem.send(f"AT+CMGD={message_id}")
        def initialize(self) -> bool:
    """
    Initialize modem.
    """

    commands = [
        "ATE0",
        "AT+CMGF=1",
        "AT+CPMS=\"ME\",\"ME\",\"ME\"",
        "AT+CNMI=2,1,0,0,0",
    ]

    for command in commands:

        response = self.send(command)

        if "OK" not in response:

            logger.error(
                f"Initialization failed: {command}"
            )

            return False

    logger.info(
        "Modem initialized successfully."
    )

    return True
    def sim_ready(self) -> bool:
    """
    Check SIM card status.
    """

    response = self.send(
        "AT+CPIN?"
    )

    return "READY" in response
    def list_sms(self) -> str:
    """
    Read all SMS messages.
    """

    return self.send(
        'AT+CMGL="ALL"',
        delay=2,
    )def delete_sms(
    self,
    index: int,
) -> bool:
    """
    Delete SMS by index.
    """

    response = self.send(
        f"AT+CMGD={index}"
    )

    return "OK" in response
    
