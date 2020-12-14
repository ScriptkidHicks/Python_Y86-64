"""
This class is used as an abstraction for the
memory writing phase of the Y86-64 processor
cycle.
"""
from ValBank import ValBank
from Memory import Memory


class Memorizer:

    def __init__(self, val_bank: ValBank, memory: Memory):
        self.ValBank = val_bank
        self.Memory = memory

        self.op_lib = {0x40: self.__rmmovq, 0x50: self.__mrmovq, 0x80: self.__call,
                       0x90: self.__ret, 0xA0: self.__pushq, 0xB: self.__popq}

        for key in [0x00, 0x10, 0x20, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27, 0x28, 0x60, 0x61,
                    0x62, 0x63, 0x64, 0x65, 0x70, 0x71, 0x72, 0x73, 0x74, 0x75, 0x76, 0x77, 0x78]:
            self.op_lib[key] = self.__nops

    def __nops(self):
        pass

    def __rmmovq(self):
        self.Memory.place_value(self.ValBank.valE, self.ValBank.valA, 8)

    def __mrmovq(self):
        self.ValBank.valM = self.Memory.pull_value(self.ValBank.valE, 8)

    def __pushq(self):
        self.Memory.place_value(self.ValBank.valE, self.ValBank.valA, 8)

    def __popq(self):
        self.ValBank.valM = self.Memory.pull_value(self.ValBank.valA, 8)

    def __call(self):
        self.Memory.place_value(self.ValBank.valE, self.ValBank.valP, 8)

    def __ret(self):
        self.ValBank.valM = self.Memory.pull_value(self.ValBank.valA, 8)

    def memory_write(self):
        self.op_lib[self.ValBank.OP]()
