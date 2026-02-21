from shared_data import traffic_data
from signal_logic.timing_algorithm import get_green_time
from signal_logic.state_machine import SignalStateMachine
from signal_logic.emergency_handler import EmergencyHandler
from signal_logic.resume_logic import resume_previous_state
from detection.realtime import start_realtime_detection
import threading
import time

def test_real_time_signal_logic():

    print("\n🚦 RUNNING REAL-TIME SYSTEM 🚦")

    sm = SignalStateMachine()
    eh = EmergencyHandler()

    total_area = 100

    # Start detection thread
    threading.Thread(target=start_realtime_detection, daemon=True).start()

    time.sleep(3)  # wait for first detection

    while True:

        density_data = traffic_data["density"]
        ambulance_positions = traffic_data["ambulance"]

        if not density_data:
            continue

        print("\n=== LIVE TIMING FROM DETECTION ===")

        for lane, occupied in density_data.items():

            green_time = get_green_time(occupied, total_area)

            print(f"{lane} Occupied: {occupied}% -> Green Time: {green_time}s")

        # Emergency Check
        if len(ambulance_positions) > 0:

            saved = eh.activate(
                road=2,
                current_road=1,
                remaining_time=30
            )

            print("Emergency Active:", eh.is_active())

            saved_state = eh.clear()

            road, time_left = resume_previous_state(saved_state)

            print(f"Resumed Road: {road}")
            print(f"Remaining Time: {time_left}s")

        time.sleep(5)


if __name__ == "__main__":
    test_real_time_signal_logic()