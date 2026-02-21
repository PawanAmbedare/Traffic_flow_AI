from detection.realtime import start_realtime_detection
from shared_data import traffic_data
import threading
import time

threading.Thread(target=start_realtime_detection, daemon=True).start()

while True:
    print("Shared Data:", traffic_data)
    time.sleep(3)