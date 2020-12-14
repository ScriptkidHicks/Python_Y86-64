"""
This class abstracts the process of the 'write back' phase
of the Y86-64 cycle.
"""
from Registers import RegisterBank
from ValBank import ValBank


class RegWriter:

    def __init__(self, register_bank: RegisterBank, val_bank: ValBank):
        self.RegisterBank = register_bank
        self.ValBank = val_bank

        self.op_lib = {0xB0: self.__popq, 0x50: self.__mrmovq}
        for key in [0x00, 0x10, 0x40, 0x70, 0x71, 0x72, 0x73, 0x74, 0x75, 0x76, 0x77, 0x78]:
            self.op_lib[key] = self.__nops
        for key in [0x60, 0x61, 0x62, 0x63, 0x64, 0x65, 0x20, 0x30]:
            self.op_lib[key] = self.__vale_to_rb
        for key in [0x90, 0x80, 0xA0]:
            self.op_lib[key] = self.__vale_to_rsp
        for key in [0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27, 0x28]:
            self.op_lib[key] = self.__condmovq

    def __vale_to_rb(self):
        self.RegisterBank.set_reg_val(self.ValBank.rB, self.ValBank.valE)

    def __nops(self):
        pass

    def __vale_to_rsp(self):
        self.RegisterBank.set_reg_val(4, self.ValBank.valE)

    def __popq(self):
        self.RegisterBank.set_reg_val(4, self.ValBank.valE)
        self.RegisterBank.set_reg_val(self.ValBank.rA, self.ValBank.valM)

    def __condmovq(self):
        if self.ValBank.CND:
            self.RegisterBank.set_reg_val(self.ValBank.rB, self.ValBank.valE)

    def __mrmovq(self):
        self.RegisterBank.set_reg_val(self.ValBank.rA, self.ValBank.valM)

    def write_back(self):
        self.op_lib[self.ValBank.OP]()
