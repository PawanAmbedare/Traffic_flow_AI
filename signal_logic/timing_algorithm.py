# timing_algorithm.py

from constants import MIN_GREEN, MID_GREEN, MAX_GREEN

def get_green_time(vehicle_density):
    """
    Adaptive timing logic
    """

    if vehicle_density < 0.5:
        return MIN_GREEN
    elif vehicle_density <= 0.75:
        return MID_GREEN
    else:
        return MAX_GREEN