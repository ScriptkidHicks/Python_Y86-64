"""
This class abstracts the Y86-64 process
of updating the PC value
"""
from Registers import RegisterBank
from ValBank import ValBank


class PCUpdater:

    def __init__(self, registers: RegisterBank, val_bank: ValBank):
        self.RegisterBank = registers
        self.ValBank = val_bank

        self.op_lib = {0x90: self.__ret, 0x80: self.__call}
        for key in [0x00, 0x10, 0x20, 0x30, 0x40, 0x50, 0x60, 0x61, 0x62, 0x63, 0x64,
                    0x65, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27, 0x28, 0xA0, 0xB0]:
            self.op_lib[key] = self.__regular_update
        for key in [0x70, 0x71, 0x72, 0x73, 0x74, 0x75, 0x76, 0x77, 0x78]:
            self.op_lib[key] = self.__conditional_update

    def __regular_update(self):
        self.RegisterBank.set_reg_val(15, self.ValBank.valP)

    def __conditional_update(self):
        if self.ValBank.CND:
            self.RegisterBank.set_reg_val(15, self.ValBank.valC)
        else:
            self.RegisterBank.set_reg_val(15, self.ValBank.valP)

    def __call(self):
        self.RegisterBank.set_reg_val(15, self.ValBank.valC)

    def __ret(self):
        self.RegisterBank.set_reg_val(15, self.ValBank.valM)

    def update_pc(self):
        self.op_lib[self.ValBank.OP]()
