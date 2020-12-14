"""
This object is an abstraction for the fetching process used
by Y86-64 ValBanks.
"""
from ValBank import ValBank
from Memory import Memory
from Registers import RegisterBank
from Flags import StateFlag


class Fetcher:

    def __init__(self, val_bank: ValBank, register_bank: RegisterBank, memory: Memory, state_flag: StateFlag,
                 error_flag: StateFlag):
        self.ValBank =val_bank
        self.RegisterBank = register_bank
        self.Memory = memory
        self.State = state_flag
        self.ErrorFlag = error_flag

        self.op_lib = {0x00: self.__halt, 0x10: self.__nop}
        for key in [0x20, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x60, 0x61, 0x62, 0x63, 0xA0, 0xB0]:
            self.op_lib[key] = self.__two_op
        for key in [0x30, 0x40, 0x50, 0x64, 0x65]:
            self.op_lib[key] = self.__ten_op
        for key in [0x70, 0x71, 0x72, 0x73, 0x74, 0x75, 0x76, 0x80]:
            self.op_lib[key] = self.__nine_op

    def __op_pull(self):
        self.ValBank.valP = self.RegisterBank.get_reg_val(15)
        self.ValBank.OP = self.Memory.pull_byte(self.ValBank.valP)

    def __halt(self):
        self.State.set_state(1)

    def __nop(self):
        self.ValBank.valP += 1

    def __two_op(self):
        self.ValBank.rA = self.Memory.pull_byte(self.ValBank.valP + 1) >> 4
        self.ValBank.rB = self.Memory.pull_byte(self.ValBank.valP + 1) & 0xF
        self.ValBank.valP += 2

    def __nine_op(self):
        self.ValBank.valC = self.Memory.pull_value(self.ValBank.valP, 8)
        self.ValBank.valP += 9

    def __ten_op(self):
        self.ValBank.rA = self.Memory.pull_byte(self.ValBank.valP + 1) >> 4
        self.ValBank.rB = self.Memory.pull_byte(self.ValBank.valP + 1) & 0xF
        self.ValBank.valC = self.Memory.pull_value(self.ValBank.valP + 2, 8)
        self.ValBank.valP += 10

    def fetch(self):
        self.__op_pull()
        try:
            self.op_lib[self.ValBank.OP]()
        except KeyError:
            self.ErrorFlag.set_state(2)
            self.State.set_state(2)
