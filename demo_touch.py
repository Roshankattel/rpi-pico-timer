"""ILI9341 demo (simple touch demo)."""
from ili9341 import Display, color565
from xpt2046 import Touch
from machine import idle, Pin, SPI  # type: ignore


class Demo(object):
    """Touchscreen simple demo."""
    CYAN = color565(0, 255, 255)
    PURPLE = color565(255, 0, 255)
    WHITE = color565(255, 255, 255)

    def __init__(self, display, spi2):
        """Initialize box.

        Args:
            display (ILI9341): display object
            spi2 (SPI): SPI bus
        """
        self.display = display
        self.touch = Touch(spi2, cs=Pin(16), int_pin=Pin(13),
                           int_handler=self.touchscreen_press)
        # Display initial message
        self.display.draw_text8x8(self.display.width // 2 - 32,
                                  self.display.height - 9,
                                  "TOUCH ME",
                                  self.WHITE,
                                  background=self.PURPLE)

        # A small 5x5 sprite for the dot
        self.dot = bytearray(b'\x00\x00\x07\xE0\xF8\x00\x07\xE0\x00\x00\x07\xE0\xF8\x00\xF8\x00\xF8\x00\x07\xE0\xF8\x00\xF8\x00\xF8\x00\xF8\x00\xF8\x00\x07\xE0\xF8\x00\xF8\x00\xF8\x00\x07\xE0\x00\x00\x07\xE0\xF8\x00\x07\xE0\x00\x00')

    # def touchscreen_press(self, x, y):
    #     """Process touchscreen press events."""
    #     # Y needs to be flipped
    #     y = (self.display.height - 1) - y
    #     # Display coordinates
    #     self.display.draw_text8x8(self.display.width // 2 - 32,
    #                               self.display.height - 9,
    #                               "{0:03d}, {1:03d}".format(x, y),
    #                               self.CYAN)
    #     # Draw dot
    #     self.display.draw_sprite(self.dot, x - 2, y - 2, 5, 5)

    def touchscreen_press(self, x, y):
        """Process touchscreen press events."""
        # Y needs to be flipped
        y = (self.display.height - 1) - y
        # Display coordinates
        self.display.draw_text8x8(self.display.width // 2 - 32,
                                  self.display.height - 9,
                                  "{0:03d}, {1:03d}".format(x, y),
                                  self.CYAN)
        # Draw dot
        self.display.draw_sprite(self.dot, x - 2, y - 2, 5, 5)


def test():
    """Test code."""
    spi1 = SPI(0, baudrate=10000000, sck=Pin(18), mosi=Pin(19))
    display = Display(spi1, dc=Pin(15), cs=Pin(17), rst=Pin(14))
    spi2 = SPI(1, baudrate=1000000, sck=Pin(10), mosi=Pin(11), miso=Pin(12))

    Demo(display, spi2)

    try:
        while True:
            idle()

    except KeyboardInterrupt:
        print("\nCtrl-C pressed.  Cleaning up and exiting...")
    finally:
        display.cleanup()


test()
