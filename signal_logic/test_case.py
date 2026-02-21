# test_cases.py

from timing_algorithm import get_green_time
from state_machine import SignalStateMachine
from emergency_handler import EmergencyHandler
from resume_logic import resume_previous_state
from constants import ROADS


def test_timing_algorithm():
    print("\n=== Testing Timing Algorithm ===")

    total_area = 100

    test_values = [0, 20, 50, 80, 100]

    for occupied in test_values:
        time = get_green_time(occupied, total_area)
        print(f"Occupied Area: {occupied}% -> Green Time: {time}s")


def test_state_machine():
    print("\n=== Testing State Machine ===")

    sm = SignalStateMachine()

    sm.to_green()
    print("State:", sm.get_state())

    sm.to_yellow()
    print("State:", sm.get_state())

    sm.to_red()
    print("State:", sm.get_state())


def test_emergency_handler():
    print("\n=== Testing Emergency Handler ===")

    eh = EmergencyHandler()

    eh.activate(
        road=4,
        current_road=2,
        remaining_time=40
    )

    print("Emergency Active:", eh.is_active())

    saved = eh.clear()
    print("Emergency Active:", eh.is_active())

    return saved


def test_resume_logic(saved_state):
    print("\n=== Testing Resume Logic ===")

    road, time_left = resume_previous_state(saved_state)

    print(f"Resumed Road: {road}")
    print(f"Remaining Time: {time_left}s")


def test_all():

    print("🚦 RUNNING COMPLETE SYSTEM TEST 🚦")

    test_timing_algorithm()
    test_state_machine()

    saved = test_emergency_handler()
    test_resume_logic(saved)

    print("\n✅ ALL TESTS COMPLETED SUCCESSFULLY")


if __name__ == "__main__":
    test_all()