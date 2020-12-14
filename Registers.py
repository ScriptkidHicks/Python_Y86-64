
class Register:

    def __init__(self, name: str):
        self.value = 0
        self.name = name


class RegisterBank:

    def __init__(self):
        self.reg_bank = [Register("%rax"), Register("%rcx"), Register("%rdx"), Register("%rbx"),
                         Register("%rsp"), Register("%rbp"), Register("%rsi"), Register("%rdi"),
                         Register("%r8"), Register("%r9"), Register("%r10"), Register("%r11"),
                         Register("%r12"), Register("%r13"), Register("%r14"), Register("%pc")]

    def set_reg_val(self, register, value):
        if (register > 15) or (register < 0):
            raise LookupError
        if type(value) is not int:
            raise TypeError
        self.reg_bank[register] = value

    def get_reg_val(self, register):
        if (register > 15) or (register < 0):
            raise LookupError
        return self.reg_bank[register].value

    def __getitem__(self, item):
        return self.reg_bank[item]
