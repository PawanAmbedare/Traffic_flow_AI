# state_machine.py

from constants import STATE_GREEN, STATE_YELLOW, STATE_RED

class SignalStateMachine:

    def __init__(self):
        self.state = STATE_RED

    def to_green(self):
        self.state = STATE_GREEN

    def to_yellow(self):
        self.state = STATE_YELLOW

    def to_red(self):
        self.state = STATE_RED

    def get_state(self):
        return self.state