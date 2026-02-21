# timing_algorithm.py

from constants import MIN_GREEN, MID_GREEN, MAX_GREEN

def get_green_time(vehicle_count):
    """
    Adaptive timing logic
    """

    if vehicle_count < 5:
        return MIN_GREEN
    elif vehicle_count <= 15:
        return MID_GREEN
    else:
        return MAX_GREEN