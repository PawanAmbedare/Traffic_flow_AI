# emergency_handler.py

class EmergencyHandler:

    def __init__(self):
        self.active = False
        self.emergency_road = None
        self.saved_state = None

    def activate(self, road, current_road, remaining_time):
        self.active = True
        self.emergency_road = road
        self.saved_state = (current_road, remaining_time)

        print(f"🚑 Emergency on Road {road}")

    def clear(self):
        self.active = False
        road = self.emergency_road
        self.emergency_road = None
        print("Emergency cleared")
        return self.saved_state

    def is_active(self):
        return self.active