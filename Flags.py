"""
These objects are used to represent condition flags,
and state flags for the processor
"""


class CCFlag:

    def __init__(self, name: str):
        self.Name = name
        self.State = False

    def __bool__(self):
        return self.State

    def flip(self):
        self.State = not self.State


class StateFlag:

    def __init__(self, name: str, state_dict: dict):
        self.name = name
        self.StateLib = state_dict
        self.State = 0

    def set_state(self, state: int):
        self.State = state

