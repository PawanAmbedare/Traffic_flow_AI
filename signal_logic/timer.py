# timer.py

import time

def start_timer(seconds):
    """
    Simulation timer
    """

    while seconds > 0:
        print(f"Time left: {seconds}s")
        time.sleep(1)
        seconds -= 1