"""
This object is meant to imitate a basic form of memory that the chip
would have access to. It's possible that this project will implement
more complex forms of memory, including tiered caching as things
go on.
"""


class Memory:

    def __init__(self, size = 10000):
        self.size = size
        self.MemBlock = [0] * size

    def __repr__(self):
        print_out = ""
        for x in range(self.size):
            if x % 8 == 0:
                print_out += "\n"
            print_out += f"{self.MemBlock[x]:x} "
        return print_out

    def pull_byte(self, index):
        if (index < 0) or (index >= self.size):
            raise IndexError(f"Index {index} was out of range of memory sized {self.size}")
        return self.MemBlock[index]

    def place_instruction(self, index: int, instruction: int, length:int):
        if (index < 0) or (index >= self.size):
            raise IndexError(f"Index {index} was out of range of memory sized {self.size}")
        for x in range(length - 1, -1, -1):
            commit = 0xFF & instruction
            instruction = instruction >> 8
            self.MemBlock[x + index] = commit

    def place_value(self, index: int, value: int, length: int):
        if (index < 0) or (index >= self.size):
            raise IndexError(f"Index {index} was out of range of memory sized {self.size}")
        for x in range(length):
            commit = 0xFF & value
            value = value >> 8
            self.MemBlock[x + index] = commit

    def pull_value(self, index: int, length: int):
        if (index < 0) or (index >= self.size):
            raise IndexError(f"Index {index} was out of range of memory sized {self.size}")
        value = 0
        for x in range(length - 1, -1, -1):
            value <<= 8
            value |= self.MemBlock[x + index]
        return value
