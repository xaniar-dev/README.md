"""
EC25 modem driver.
"""

import time
import serial

from config import MODEM_BAUDRATE
from config import MODEM_PORT

from src.logger import logger


class Modem:
    """EC25 modem interface."""

    def __init__(self) -> None:

        self.serial = serial.Serial(
            port=MODEM_PORT,
            baudrate=MODEM_BAUDRATE,
            timeout=2,
        )

        logger.info("Modem initialized.")

    def send(
        self,
        command: str,
        delay: float = 0.5,
    ) -> str:
        """
        Send an AT command.
        """

        self.serial.reset_input_buffer()

        self.serial.write(
            f"{command}\r".encode()
        )

        self.serial.flush()

        time.sleep(delay)

        response = self.serial.read_all()

        return response.decode(
            errors="ignore"
        )

    def test(self) -> bool:
        """
        Check modem availability.
        """

        response = self.send("AT")

        return "OK" in response

    def signal(self) -> int:
        """
        Read signal strength (RSSI).
        """

        response = self.send("AT+CSQ")

        try:

            value = (
                response
                .split(":")[1]
                .split(",")[0]
                .strip()
            )

            return int(value)

        except Exception:

            return -1

    def operator(self) -> str:
        """
        Read network operator.
        """

        response = self.send(
            "AT+COPS?"
        )

        return response

    def network_registered(self) -> bool:
        """
        Check network registration.
        """

        response = self.send(
            "AT+CREG?"
        )

        return (
            ",1" in response
            or ",5" in response
        )

    def imei(self) -> str:
        """
        Read modem IMEI.
        """

        response = self.send(
            "AT+CGSN"
        )

        lines = [
            line.strip()
            for line in response.splitlines()
            if line.strip()
        ]

        for line in lines:

            if line.isdigit():

                return line

        return ""

    def close(self) -> None:
        """
        Close serial port.
        """

        if self.serial.is_open:

            self.serial.close()

            logger.info(
                "Modem closed."
            )
