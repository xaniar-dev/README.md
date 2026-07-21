from luma.core.render import canvas
from luma.oled.device import ssd1306
from luma.core.interface.serial import i2c


class OLEDDisplay:
    def __init__(self):
        serial = i2c(port=1, address=0x3C)
        self.device = ssd1306(serial)

    def show_message(self, line1, line2=""):
        with canvas(self.device) as draw:
            draw.text((0, 0), line1, fill="white")
            draw.text((0, 20), line2, fill="white")
