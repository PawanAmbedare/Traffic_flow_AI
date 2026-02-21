from detection.realtime import start_realtime_detection
from shared_data import traffic_data
import threading
import time

# Start AI detection in background thread
threading.Thread(target=start_realtime_detection, daemon=True).start()

while True:
    density = traffic_data["density"]
    ambulance = traffic_data["ambulance"]

    if density:
        print("Live Density:", density)
        print("Ambulance:", ambulance)
        print("-----------------------")

    time.sleep(2)