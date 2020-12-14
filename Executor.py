"""
This class is an abstraction of the execution
phase performed by the Y86-64 processor.
"""
from Flags import CCFlag
from ALU import ALU
from ValBank import ValBank


class Executor:

    def __init__(self, val_bank: ValBank, alu: ALU, of: CCFlag, zf: CCFlag, sf: CCFlag):
        self.ValBank = val_bank
        self.ALU = alu
        self.OF = of
        self.ZF = zf
        self.SF = sf

        self.op_lib = {0x00: self.__nop, 0x10: self.__nop, 0x20: self.__rrmovq, 0x30: self.__irmovq,
                       0x40: self.__mr_rm, 0x50: self.__mr_rm, 0x60: self.__addq, 0x61: self.__subq,
                       0x62: self.__andq, 0x63: self.__orq, 0x64: self.__iaddq, 0x65: self.__isubq,
                       0x70: self.__jmp, 0x71: self.__jle, 0x72: self.__jl, 0x73: self.__je,
                       0x74: self.__jne, 0x75: self.__jge, 0x76: self.__jg, 0x77: self.__js,
                       0x78: self.__jns, 0x21: self.__cmovle, 0x22: self.__cmovl, 0x23: self.__cmove,
                       0x24: self.__cmovne, 0x25: self.__cmovge, 0x26: self.__cmovg, 0x27: self.__cmovs,
                       0x28: self.__cmovns, 0x80: self.__call, 0x90: self.__ret, 0xA0: self.__pushq,
                       0xB0: self.__popq
                       }

    def __nop(self):
        pass

    def __addq(self):
        self.ValBank.valE = self.ALU.ADDQ()

    def __subq(self):
        self.ValBank.valE = self.ALU.SUBQ()

    def __andq(self):
        self.ValBank.valE = self.ALU.ANDQ()

    def __orq(self):
        self.ValBank.valE = self.ALU.ORQ()

    def __iaddq(self):
        self.ValBank.valE = self.ALU.IADDQ()

    def __isubq(self):
        self.ValBank.valE = self.ALU.ISUBQ()

    def __rrmovq(self):
        self.ValBank.valE = self.ValBank.valA

    def __irmovq(self):
        self.ValBank.valE = self.ValBank.valC

    def __mr_rm(self):
        self.ValBank.valE = self.ValBank.valB + self.ValBank.valC

    def __pushq(self):
        self.ValBank.valE = self.ValBank.valB - 8

    def __popq(self):
        self.ValBank.valE = self.ValBank.valB + 8

    def __jmp(self):
        self.ValBank.CND = True

    def __je(self):
        self.ValBank.CND = self.ZF

    def __jne(self):
        self.ValBank.CND = not self.ZF

    def __js(self):
        self.ValBank.CND = self.SF

    def __jns(self):
        self.ValBank.CND = not self.SF

    def __jg(self):
        self.ValBank.CND = (self.SF == self.OF) and (not self.ZF)

    def __jge(self):
        self.ValBank.CND = self.SF == self.OF

    def __jl(self):
        self.ValBank.CND = self.SF != self.OF

    def __jle(self):
        self.ValBank.CND = (self.SF != self.OF) or self.ZF

    def __cmove(self):
        self.ValBank.valE = self.ValBank.valA
        self.ValBank.CND = self.ZF

    def __cmovne(self):
        self.ValBank.valE = self.ValBank.valA
        self.ValBank.CND = not self.ZF

    def __cmovs(self):
        self.ValBank.valE = self.ValBank.valA
        self.ValBank.CND = self.SF

    def __cmovns(self):
        self.ValBank.valE = self.ValBank.valA
        self.ValBank.CND = not self.SF

    def __cmovg(self):
        self.ValBank.valE = self.ValBank.valA
        self.ValBank.CND = (self.SF == self.OF) and (not self.ZF)

    def __cmovge(self):
        self.ValBank.valE = self.ValBank.valA
        self.ValBank.CND = self.SF == self.OF

    def __cmovl(self):
        self.ValBank.valE = self.ValBank.valA
        self.ValBank.CND = self.SF != self.OF

    def __cmovle(self):
        self.ValBank.valE = self.ValBank.valA
        self.ValBank.CND = (self.SF != self.OF) or self.ZF

    def __call(self):
        self.ValBank.valE = self.ValBank.valB - 8

    def __ret(self):
        self.ValBank.valE = self.ValBank.valB + 8

    def execute(self):
        self.op_lib[self.ValBank.OP]()
