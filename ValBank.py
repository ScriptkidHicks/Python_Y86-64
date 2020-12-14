"""
This module ended up being necessary as a way to avoid circular
references. I don't love it, but I haven't found a way around it
"""


class ValBank:

    def __init__(self):
        self.OP = 0
        self.valP = 0
        self.rA = 0
        self.rB = 0
        self.valA = 0
        self.valB = 0
        self.valC = 0
        self.valE = 0
        self.valM = 0
        self.CND = False
