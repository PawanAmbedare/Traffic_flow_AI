import time
from detection.detect import get_traffic_data
from shared_data import traffic_data

def start_realtime_detection():

    while True:

        density, ambulance = get_traffic_data()

        if density:
            traffic_data["density"] = density
            traffic_data["ambulance"] = ambulance
            print("---------------------------")

        time.sleep(2)   # update every 2 seconds