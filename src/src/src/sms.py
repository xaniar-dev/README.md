import serial
import time


class SMSReader:
    def __init__(self, port="/dev/ttyUSB2", baudrate=115200):
        self.serial = serial.Serial(port, baudrate, timeout=1)

    def send_command(self, command):
        self.serial.write((command + "\r").encode())
        time.sleep(1)
        return self.serial.read_all().decode(errors="ignore")

    def initialize(self):
        print(self.send_command("AT"))
        print(self.send_command("ATE0"))
        print(self.send_command("AT+CMGF=1"))

    def list_messages(self):
        return self.send_command('AT+CMGL="ALL"')
