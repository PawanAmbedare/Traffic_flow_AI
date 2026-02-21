# main_controller.py

from constants import ROADS, YELLOW_TIME
from timing_algorithm import get_green_time
from state_machine import SignalStateMachine
from emergency_handler import EmergencyHandler
from resume_logic import resume_previous_state
from Timer import start_timer

import random

class TrafficController:

    def __init__(self):
        self.current_index = 0
        self.state_machine = SignalStateMachine()
        self.emergency = EmergencyHandler()

    def get_current_road(self):
        return ROADS[self.current_index]

    def next_road(self):
        self.current_index = (self.current_index + 1) % len(ROADS)

    def run(self):

        while True:

            road = self.get_current_road()

            # simulate traffic density
            vehicles = random.randint(1, 20)
            green_time = get_green_time(vehicles)

            print(f"\nRoad {road} GREEN for {green_time}s")
            self.state_machine.to_green()

            # RANDOM EMERGENCY SIMULATION
            if random.randint(1, 10) == 1:
                emergency_road = random.choice(ROADS)

                self.emergency.activate(
                    emergency_road,
                    road,
                    green_time
                )

                print(f"Switching to Emergency Road {emergency_road}")
                start_timer(10)

                saved = self.emergency.clear()
                road, green_time = resume_previous_state(saved)

            start_timer(green_time)

            print(f"Road {road} YELLOW")
            self.state_machine.to_yellow()
            start_timer(YELLOW_TIME)

            print(f"Road {road} RED")
            self.state_machine.to_red()

            self.next_road()


if __name__ == "__main__":
    controller = TrafficController()
    controller.run()