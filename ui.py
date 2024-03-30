"""ILI9341 demo (simple touch demo)."""
from ili9341 import Display, color565
from xpt2046 import Touch
from machine import idle, Pin, SPI  # type: ignore
from xglcd_font import XglcdFont

class Demo(object):
    """Touchscreen simple demo."""
    #BGR format
    CYAN = color565(0, 255, 255)
    RED = color565(0, 0, 31)
    BLUE = color565(31, 0, 0)
    GREEN = color565(0, 63, 0)
    PURPLE = color565(31, 0, 27)
    WHITE = color565(255, 255, 255)

    # initialize font to be used
    unispace = XglcdFont('fonts/Unispace12x24.c', 12, 24)


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
        self.draw_screen_4()

    def draw_screen_1(self):
        """Draw the contents of screen 1."""
        self.display.draw_text8x8(200,
                                  20,
                                  "Please choose the following options",
                                  self.WHITE, 0, 90)

        self.display.draw_text8x8(170,
                                  142,
                                  "Task",
                                  self.BLUE, 0, 90)

        self.display.draw_text8x8(140,
                                  140,
                                  "Break",
                                  self.PURPLE, 0, 90)

        self.display.draw_text8x8(10,
                                  20,
                                  "Back",
                                  self.RED, 0, 90)

        self.display.draw_text8x8(8,
                                  270,
                                  "Next",
                                  self.GREEN, 0, 90)
        
    def draw_screen_2(self):
        """Draw the contents of screen 2"""
        self.display.draw_text8x8(200,
                                  80,
                                  "Duration (in minutes)",
                                  self.WHITE, 0, 90)

        for i in range(0, 10):
            x = 130 if i < 5 else 130 - 60
            y = 25 + 57 * (i % 5)
            self.display.draw_rectangle(x, y, 40, 40, self.WHITE)
            self.display.draw_text8x8(x + 18, y + 17, str(i), self.BLUE, 0, 90)

        self.display.draw_text8x8(10,
                                  20,
                                  "Back",
                                  self.RED, 0, 90)

        self.display.draw_text8x8(8,
                                  270,
                                  "Next",
                                  self.GREEN, 0, 90)

    def draw_screen_3(self):
        """Draw the contents of screen 3"""
        self.display.draw_text8x8(200,
                                  80,
                                  "Start [Task/Break]?",
                                  self.WHITE, 0, 90)


        self.display.draw_rectangle(120, 90, 30, 50, self.GREEN)
        self.display.draw_text8x8(130, 100, "YES", self.GREEN, 0, 90)

        self.display.draw_rectangle(120, 160, 30, 50, self.RED)
        self.display.draw_text8x8(130, 176, "NO", self.RED, 0, 90)

    def draw_screen_4(self):
        """Draw the contents of screen 4"""
        self.display.draw_text(10, 290, "Show CountDown Timer", self.unispace,
                                  self.PURPLE, 0, True, True)

    def touchscreen_press(self, x, y):
        """Process touchscreen press events."""
        # Y needs to be flipped
        y = (self.display.height - 1) - y
        # Display coordinates
        self.display.draw_text8x8(self.display.width // 2 - 32,
                                  self.display.height - 9,
                                  "{0:03d}, {1:03d}".format(x, y),
                                  self.CYAN)



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
