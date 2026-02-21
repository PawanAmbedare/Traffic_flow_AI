# resume_logic.py

def resume_previous_state(saved_state):
    """
    Resume from interrupted road
    """
    if saved_state:
        road, time_left = saved_state
        print(f"Resuming Road {road} with {time_left}s left")
        return road, time_left

    return None, None