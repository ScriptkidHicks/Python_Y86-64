"""
This class is an abstraction of the decoding process done by
a Y86-64 ValBank
"""
from ValBank import ValBank
from Registers import RegisterBank
from Memory import Memory


class Decoder:

    def __init__(self, val_bank: ValBank, register_bank: RegisterBank, memory: Memory):
        self.ValBank = val_bank
        self.RegisterBank = register_bank
        self.Memory = memory

        self.op_lib = {0xA0: self.__pushq}
        for key in [0x00, 0x10, 0x30, 0x70, 0x71, 0x72, 0x73, 0x74, 0x75, 0x76]:
            self.op_lib[key] = self.__nops
        for key in [0x60, 0x61, 0x62, 0x63, 0x64, 0x65, 0x20, 0x40, 0x50]:
            self.op_lib[key] = self.__both_norm_pull
        for key in [0xB0, 0x80, 0x90]:
            self.op_lib[key] = self.__pop_call_ret

    def __both_norm_pull(self):
        self.ValBank.valA = self.RegisterBank.get_reg_val(self.ValBank.rA)
        self.ValBank.valB = self.RegisterBank.get_reg_val(self.ValBank.rB)

    def __pushq(self):
        self.ValBank.valA = self.RegisterBank.get_reg_val(self.ValBank.rA)
        self.ValBank.valB = self.RegisterBank.get_reg_val(4)

    def __pop_call_ret(self):
        self.ValBank.valA = self.ValBank.valB = self.RegisterBank.get_reg_val(4)

    def __nops(self):
        pass

    def decode(self):
        self.op_lib[self.ValBank.OP]()
