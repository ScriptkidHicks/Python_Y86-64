"""
This class represents the arithmetic logical unit
"""
from Flags import StateFlag, CCFlag
from ValBank import ValBank


class ALU:

    def __init__(self, val_bank: ValBank, state_flag: StateFlag, error_flag: StateFlag, sf: CCFlag, of: CCFlag, zf: CCFlag):
        self.ValBank = val_bank
        self.StateFlag = state_flag
        self.ErrorFlag = error_flag
        self.SF = sf
        self.OF = of
        self.ZF = zf

    def __flag_check(self, value):
        sf, zf, of = False
        if value < 0:
            sf = True
        if value == 0:
            zf = True
        if (value > 0xFFFFFFFFFFFFFFFF) or (value < -0xFFFFFFFFFFFFFFFF):
            of = True
        self.ZF, self.OF, self.SF = zf, of, sf

    def ADDQ(self):
        result = self.ValBank.valB + self.ValBank.valA
        self.__flag_check(result)
        return result

    def SUBQ(self):
        result = self.ValBank.valB - self.ValBank.valA
        self.__flag_check(result)
        return result

    def ANDQ(self):
        return self.ValBank.valB & self.ValBank.valA

    def ORQ(self):
        return self.ValBank.valB | self.ValBank.valA

    def IADDQ(self):
        result = self.ValBank.valB + self.ValBank.valC
        self.__flag_check(result)
        return result

    def ISUBQ(self):
        result = self.ValBank.valB - self.ValBank.valC
        self.__flag_check(result)
        return result
