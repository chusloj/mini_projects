import time
import math
from curses import wrapper

def main(stdscr):
    # Clear screen
    stdscr.clear()

    for i in range(100):
        stdscr.addstr(0, 0, str(i % 4))
        stdscr.refresh()
        sleep_time = 3 / (100 - i)
        if sleep_time >= 0.8:
            stdscr.addstr(0, 0, f"Your number is: {i % 4}")
            break
        time.sleep(sleep_time)

    # stdscr.refresh()
    stdscr.getkey()

wrapper(main)