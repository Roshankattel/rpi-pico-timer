"""ILI9341 demo (simple touch demo)."""
from ili9341 import Display, color565
from xpt2046 import Touch
from machine import idle, Pin, SPI  # type: ignore
from xglcd_font import XglcdFont
import time


class Show(object):
    """Count Down Timer and Interfaces."""
    # BGR format
    CYAN = color565(0, 255, 255)
    RED = color565(0, 0, 31)
    BLUE = color565(31, 0, 0)
    GREEN = color565(0, 63, 0)
    PURPLE = color565(31, 0, 27)
    WHITE = color565(255, 255, 255)

    # initialize font to be used
    font = XglcdFont('fonts/Unispace12x24.c', 12, 24)

    screen = 0
    activity = True
    duration = ""

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
        # self.display.draw_text8x8(self.display.width // 2 - 32,
        #                           self.display.height - 9,
        #                           "TOUCH ME",
        #                           self.WHITE,
        #                           background=self.PURPLE)

        self.draw_screen_1()

    def draw_screen_1(self):
        """Draw the contents of screen 1."""
        self.screen = 1
        self.display.draw_text(200, 280, "Please select option",
                               self.font, self.WHITE, 0, 1, 1)

        self.display.draw_text(150, 180, "Task",
                               self.font, self.BLUE, 0, 1, 1)

        # Select task at the beginning
        self.display.draw_text(150, 120, "->",
                               self.font, self.CYAN, 0, 1, 1)

        self.display.draw_text(110, 190, "Break",
                               self.font, self.PURPLE, 0, 1, 1)

        self.display.draw_text(5, 60, "Back",
                               self.font, self.RED, 0, 1, 1)

        self.display.draw_text(5, 310, "Next",
                               self.font, self.GREEN, 0, 1, 1)

    def draw_screen_2(self):
        """Draw the contents of screen 2"""
        self.screen = 2
        self.display.draw_text(200, 280, "Duration (in minutes)",
                               self.font, self.WHITE, 0, 1, 1)

        for i in range(0, 10):
            x = 150 if i < 5 else 150 - 60
            y = 25 + 57 * (i % 5)
            self.display.draw_rectangle(x, y, 40, 40, self.WHITE)
            self.display.draw_text(x + 10, y + 25, str(i),
                                   self.font, self.BLUE, 0, 1, 1)

        self.display.draw_text(5, 60, "Back",
                               self.font, self.RED, 0, 1, 1)

        self.display.draw_text(5, 190, "Clear",
                               self.font, self.WHITE, 0, 1, 1)

        self.display.draw_text(5, 310, "Next",
                               self.font, self.GREEN, 0, 1, 1)

    def draw_screen_3(self):
        """Draw the contents of screen 3"""
        self.screen = 3
        if self.activity:
            self.display.draw_text(200, 220, "Start Task",
                                   self.font, self.WHITE, 0, 1, 1)
        else:
            self.display.draw_text(200, 220, "Start Break",
                                   self.font, self.WHITE, 0, 1, 1)

        self.display.draw_rectangle(110, 80, 40, 60, self.GREEN)
        self.display.draw_text(118, 127, "YES",
                               self.font, self.GREEN, 0, 1, 1)

        self.display.draw_rectangle(110, 170, 40, 60, self.RED)
        self.display.draw_text(118, 210, "NO",
                               self.font, self.RED, 0, 1, 1)

    def show_time(self, seconds):
        hrs = seconds // 3600
        mins = (seconds % 3600) // 60
        secs = (seconds % 3600) % 60
        time_str = "{:02d}:{:02d}:{:02d}".format(hrs, mins, secs)
        self.display.draw_text(110, 200, time_str,
                               self.font, self.WHITE, 0, 1, 10)

    def draw_screen_4(self):
        """Draw the contents of screen 4"""
        self.screen = 4
        self.display.draw_text(180, 185, "Timer",
                               self.font, self.PURPLE, 0, 1, 1)
        if self.duration == "":
            second = 0
        else:
            second = int(self.duration) * 60

        while second > 0:
            self.show_time(second)
            time.sleep(1)
            second -= 1

        self.duration = ''
        self.display.draw_text(110, 250, "COMPLETED (^_^)",
                               self.font, self.CYAN, 0, 1, 5)
        time.sleep(5)
        self.display.clear()
        self.draw_screen_1()

    def touchscreen_press(self, x, y):
        """Process touchscreen press events."""
        # Adding an offset
        x = x - 10
        y = y - 10

        # Y needs to be flipped
        y = (self.display.height - 1) - y

        # Display coordinates in the board for Debugging
        # print(x, y)
        # self.display.draw_text8x8(self.display.width // 2 - 32,
        #                           self.display.height - 9,
        #                           "{0:03d}, {1:03d}".format(x, y),
        #                           self.CYAN)

        if self.screen == 1:
            # SCREEN-1 TASK
            if 120 <= x <= 200 and 160 <= y <= 200:
                self.activity = True
                self.display.draw_text(150, 120, "->", self.font, self.CYAN, 0, 1, 1)
                self.display.draw_text(110, 120, "->", self.font, 0, 0, 1, 1)
            # SCREEN-1 BREAK
            elif 100 <= x <= 120 and 160 <= y <= 200:
                self.activity = False
                self.display.draw_text(110, 120, "->", self.font, self.CYAN, 0, 1, 1)
                self.display.draw_text(150, 120, "->", self.font, 0, 0, 1, 1)
            # SCREEN-1 NEXT
            elif 0 <= x <= 20 and 280 <= y <= 320:
                self.display.clear()
                self.draw_screen_2()
                x, y = -1, -1

        elif self.screen == 2:

            for i in range(0, 10):
                bound_x = 150 if i < 5 else 150 - 60
                bound_y = 25 + 57 * (i % 5)
                if bound_x <= x <= bound_x + 40 and bound_y <= y <= bound_y + 40:
                    # Add number to duration variable
                    self.duration += str(i)
                    self.display.draw_text(50, 200, self.duration,
                                           self.font, self.CYAN, 0, 1, 1)

            # SCREEN-2 NEXT
            if 0 <= x <= 20 and 280 <= y <= 320:
                self.display.clear()
                self.draw_screen_3()
                x, y = -1, -1

            # SCREEN-2 Clear
            elif 0 <= x <= 20 and 160 <= y <= 220:
                self.duration = ''
                self.display.draw_text(50, 200, "00000000000",
                                       self.font, 0, 0, 1, 1)

            # SCREEN-2 BACK
            elif 0 <= x <= 30 and 0 <= y <= 100:
                self.display.clear()
                self.draw_screen_1()
                self.duration = ''
                x, y = -1, -1

        elif self.screen == 3:

            # SCREEN-3 YES BUTTON
            if 80 <= x <= 160 and 80 <= y <= 160:
                self.display.clear()
                self.draw_screen_4()
                x, y = -1, -1

            # SCREEN-3 NO BUTTON
            elif 80 <= x <= 150 and 170 <= y <= 240:
                self.display.clear()
                self.draw_screen_1()
                self.duration = ''
                x, y = -1, -1

        # elif self.screen == 4:
        #     # SCREEN-4 NEXT
        #     if 0 <= x <= 20 and 280 <= y <= 320:
        #         self.display.clear()
        #         self.draw_screen_1()
        #         x, y = -1, -1


def main():
    """main code."""
    spi1 = SPI(0, baudrate=20000000, sck=Pin(18), mosi=Pin(19))
    display = Display(spi1, dc=Pin(15), cs=Pin(17), rst=Pin(14))
    spi2 = SPI(1, baudrate=2000000, sck=Pin(10), mosi=Pin(11), miso=Pin(12))

    Show(display, spi2)

    try:
        while True:
            idle()

    except KeyboardInterrupt:
        print("\nCtrl-C pressed.  Cleaning up and exiting...")
    finally:
        display.cleanup()


main()
