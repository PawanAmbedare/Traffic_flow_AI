import time
from detect import get_traffic_data

def start_realtime_detection():

    while True:

        density, ambulance = get_traffic_data()

        if density:
            print("Live Lane Density:", density)
            print("Ambulance:", ambulance)
            print("---------------------------")

        time.sleep(2)   # update every 2 seconds