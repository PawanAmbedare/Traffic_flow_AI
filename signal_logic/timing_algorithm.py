# timing_algorithm.py

from signal_logic.constants import MIN_GREEN, MAX_GREEN

def get_green_time(occupied_area, total_road_area):
    """
    Adaptive timing using road occupancy ratio.
    """

    # prevent division error
    if total_road_area <= 0:
        return MIN_GREEN

    # density calculation
    density = occupied_area / total_road_area

    # keep density between 0 and 1
    density = max(0.0, min(density, 1.0))

    # scale timing
    green_time = MIN_GREEN + (
        density * (MAX_GREEN - MIN_GREEN)
    )

    return int(green_time)