# Import necessary modules
from ili9341 import Display, color565
from xglcd_font import XglcdFont
from xpt2046 import Touch
from machine import SPI, Pin, I2C
import time

tolerate_threshold = 50  # 50*10 sec

# Global variables
CYAN = color565(0, 255, 255)
RED = color565(0, 0, 31)
BLUE = color565(31, 0, 0)
GREEN = color565(0, 63, 0)
PURPLE = color565(31, 0, 27)
WHITE = color565(255, 255, 255)

font = XglcdFont('fonts/Unispace12x24.c', 12, 24)
screen = 0
activity = True
duration = ""
display_status = True

PirSensor = Pin(28, Pin.IN, Pin.PULL_DOWN)

Trig = Pin(6, Pin.OUT)  # Include the Trig pin
Echo = Pin(7, Pin.IN)  # Include the Echo pin

# Get the distance
def distance():
    high, low = 0, 0
    Trig.value(0)
    time.sleep_us(4)
    Trig.value(1)
    time.sleep_us(10)
    Trig.value(0)

    while Echo.value() == 0:
        low = time.ticks_us()

    while Echo.value() == 1:
        high = time.ticks_us()

    t = high - low
    return t


def draw_screen_1():
    global screen, activity
    screen = 1
    activity = True
    display.draw_text(200, 280, "Please select option",
                      font, WHITE, 0, 1, 1)
    display.draw_text(150, 180, "Task",
                      font, BLUE, 0, 1, 1)
    display.draw_text(150, 120, "->",
                      font, CYAN, 0, 1, 1)
    display.draw_text(110, 190, "Break",
                      font, PURPLE, 0, 1, 1)
    display.draw_text(5, 60, "Back",
                      font, RED, 0, 1, 1)
    display.draw_text(5, 310, "Next",
                      font, GREEN, 0, 1, 1)


def draw_screen_2():
    global screen
    screen = 2
    display.draw_text(200, 280, "Duration (in minutes)",
                      font, WHITE, 0, 1, 1)
    for i in range(0, 10):
        x = 150 if i < 5 else 150 - 60
        y = 25 + 57 * (i % 5)
        display.draw_rectangle(x, y, 40, 40, WHITE)
        display.draw_text(x + 10, y + 25, str(i),
                          font, BLUE, 0, 1, 1)
    display.draw_text(5, 60, "Back",
                      font, RED, 0, 1, 1)
    display.draw_text(5, 190, "Clear",
                      font, WHITE, 0, 1, 1)
    display.draw_text(5, 310, "Next",
                      font, GREEN, 0, 1, 1)


def draw_screen_3():
    global screen
    screen = 3
    if activity:
        display.draw_text(200, 220, "Start Task",
                          font, WHITE, 0, 1, 1)
    else:
        display.draw_text(200, 220, "Start Break",
                          font, WHITE, 0, 1, 1)
    display.draw_rectangle(110, 80, 40, 60, GREEN)
    display.draw_text(118, 127, "YES",
                      font, GREEN, 0, 1, 1)
    display.draw_rectangle(110, 170, 40, 60, RED)
    display.draw_text(118, 210, "NO",
                      font, RED, 0, 1, 1)


def show_time(seconds):
    global display, font
    hrs = seconds // 3600
    mins = (seconds % 3600) // 60
    secs = (seconds % 3600) % 60
    time_str = "{:02d}:{:02d}:{:02d}".format(hrs, mins, secs)
    display.draw_text(110, 200, time_str,
                      font, WHITE, 0, 1, 10)


def draw_screen_4():
    global screen, display, font, duration
    mobile_present = True
    screen = 4
    display.draw_text(180, 185, "Timer",
                      font, PURPLE, 0, 1, 1)
    if duration == "":
        second = 0
    else:
        second = int(duration) * 60
    show_time(second)
    while second > 0:
        if activity:
            dis = distance()
            inch = dis / 74 / 2  # Time convert to the inch
            if 0 < inch <= 2:
                if not mobile_present:
                    display.draw_text8x8(10, 95, " Mobile Placed", GREEN, 0, 90)
                show_time(second)
                second -= 1
                mobile_present = True
            else:
                if mobile_present:
                    display.draw_text8x8(10, 95, "Mobile Removed", RED, 0, 90)
                mobile_present = False
        else:
            show_time(second)
            second -= 1
        time.sleep(1)

    duration = ''
    display.draw_text(110, 250, "COMPLETED (^_^)",
                      font, CYAN, 0, 1, 5)
    time.sleep(5)
    display.clear()
    draw_screen_1()


def touchscreen_press(x, y):
    global screen, activity, duration, display
    x = x - 10
    y = y - 10
    y = (display.height - 1) - y

    # Display coordinates in the board for Debugging
    # print(x, y)
    # display.draw_text8x8(display.width // 2 - 32,
    #                      display.height - 9,
    #                      "{0:03d}, {1:03d}".format(x, y),
    #                      CYAN)

    if screen == 1:
        # SCREEN-1 TASK
        if 120 <= x <= 200 and 160 <= y <= 200:
            activity = True
            display.draw_text(150, 120, "->", font, CYAN, 0, 1, 1)  # show
            display.draw_text(110, 120, "->", font, 0, 0, 1, 1)  # hide

        # SCREEN-1 BREAK
        elif 100 <= x <= 120 and 160 <= y <= 200:
            activity = False
            display.draw_text(110, 120, "->", font, CYAN, 0, 1, 1)  # show
            display.draw_text(150, 120, "->", font, 0, 0, 1, 1)  # hide

        # SCREEN-1 NEXT
        elif 0 <= x <= 20 and 280 <= y <= 320:
            display.clear()
            draw_screen_2()

    elif screen == 2:
        # Touch Numbers
        for i in range(0, 10):
            bound_x = 150 if i < 5 else 150 - 60
            bound_y = 25 + 57 * (i % 5)
            if bound_x <= x <= bound_x + 40 and bound_y <= y <= bound_y + 40:
                duration += str(i)
                display.draw_text(50, 200, duration,
                                  font, CYAN, 0, 1, 1)

        # SCREEN-2 NEXT
        if 0 <= x <= 20 and 280 <= y <= 320:
            display.clear()
            draw_screen_3()

        # SCREEN-2 Clear
        elif 0 <= x <= 20 and 160 <= y <= 220:
            duration = ''
            display.draw_text(50, 200, "00000000000",
                              font, 0, 0, 1, 1)

        # SCREEN-2 BACK
        elif 0 <= x <= 30 and 0 <= y <= 100:
            display.clear()
            draw_screen_1()
            duration = ''

    elif screen == 3:
        # SCREEN-3 YES BUTTON
        if 80 <= x <= 160 and 80 <= y <= 160:
            display.clear()
            draw_screen_4()

        # SCREEN-3 NO BUTTON
        elif 80 <= x <= 150 and 170 <= y <= 240:
            display.clear()
            draw_screen_1()
            duration = ''


def main():
    global display, spi2, display_status
    spi1 = SPI(0, baudrate=20000000, sck=Pin(18), mosi=Pin(19))
    display = Display(spi1, dc=Pin(15), cs=Pin(17), rst=Pin(14))
    spi2 = SPI(1, baudrate=2000000, sck=Pin(10), mosi=Pin(11), miso=Pin(12))
    Touch(spi2, cs=Pin(16), int_pin=Pin(13), int_handler=touchscreen_press)
    tft_led = Pin(22, Pin.OUT)
    tft_led(1)  # Turn on display at first

    # Display initial message in screen
    # display.draw_text8x8(display.width // 2 - 32,
    #                      display.height - 9,
    #                      "TOUCH ME",
    #                      WHITE,
    #                      background=PURPLE)
    tolerate = 0
    draw_screen_1()
    start_time = time.ticks_us()
    try:
        while True:
            current_time = time.ticks_us()
            if not display_status:
                if time.ticks_diff(current_time, start_time) / 100000 > 5:
                    # check every 10 sec when display is off
                    if PirSensor.value():
                        print("Motion detected:")
                        display_status = True
                        tft_led(1)
                        print("Screen ON")
                    start_time = time.ticks_us()
            elif display_status and time.ticks_diff(current_time, start_time) / 100000 > 10:
                # check every 10 sec when display
                if PirSensor.value():
                    print("Motion detected, Continuing...")
                    tolerate = 0
                else:
                    tolerate = tolerate + 1
                    if tolerate > tolerate_threshold:
                        print("Motion no detected (secs):" + str(tolerate_threshold * 10))
                        display_status = False
                        tft_led(0)
                        print("Screen OFF")
                        tolerate = 0
                        time.sleep_ms(500)
                start_time = time.ticks_us()

    except KeyboardInterrupt:
        print("\nCtrl-C pressed.  Cleaning up and exiting...")
    finally:
        display.cleanup()


main()
