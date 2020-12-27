class Memory:
    """
    Memory Object. Used to represent the linear form
    of memory that the Y86-64 processor has access to.
    There is currently no memory caching or tiered memory.
    """

    def __init__(self, size = 10000):
        """
        Instantiates a memory object, with 'size' bytes of space.
        Because of the addressing system that Y86-64 uses it's
        possible to have 0xFFFFFFFFFFFFFFFF addresses in theory,
        but numbers of that order don't exist as ints in python,
        so a memory of that size is not practical or possible.
        You should not need a memory larger than 1000 realistically.
        :param size: number of bytes the memory should contain.
        """
        self.size = size
        self.MemBlock = [0] * size

    def __repr__(self):
        """
        This method is structured so that when the print method is
        called on the memory object, it will return a neat string
        organized into 8 byte chunks. Instructions will necessarily
        by split between lines, but this will cleanly represent int
        storage.
        :return: str
        """
        print_out = ""
        for x in range(self.size):
            if x % 8 == 0:
                print_out += "\n"
            print_out += f"{self.MemBlock[x]:x} "
        return print_out

    def place_instruction(self, index: int, instruction: int, length:int):
        """
        Useful for placing an instruction because the instruction is
        not reversed during placement as a value would be in little
        endian systems
        :param index: location of the start of the instruction. Int
        :param instruction: the int value of the instruction itself.
        :param length: The size of the instruction in bytes
        """
        if (index < 0) or (index >= self.size):
            raise IndexError(f"Index {index} was out of range of memory sized {self.size}")
        for x in range(length - 1, -1, -1):
            commit = 0xFF & instruction
            instruction = instruction >> 8
            self.MemBlock[x + index] = commit

    def place_value(self, index: int, value: int, length: int = 8):
        """
        Places a value in memory, reversing the value's byte order
        so that it is little endian.
        :param index: starting index of the value
        :param value: value itself
        :param length: the number of bytes in the value.
        """
        if (index < 0) or (index >= self.size):
            raise IndexError(f"Index {index} was out of range of memory sized {self.size}")
        for x in range(length):
            commit = 0xFF & value
            value = value >> 8
            self.MemBlock[x + index] = commit

    def pull_value(self, index: int, length: int):
        """
        Pulls a value from memory, reversing the byte order in
        the process, since the storage method is reverse endian.
        :param index: Start index of the value
        :param length: number of bytes of the value
        :return: int: the value
        """
        if (index < 0) or (index >= self.size):
            raise IndexError(f"Index {index} was out of range of memory sized {self.size}")
        value = 0
        for x in range(length - 1, -1, -1):
            value <<= 8
            value |= self.MemBlock[x + index]
        return value
