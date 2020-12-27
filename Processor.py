from ALU import ALU
from Memory import Memory
from Registers import RegisterBank
from Flags import StateFlag, CCFlag
from Fetcher import Fetcher
from Decoder import Decoder
from Executor import Executor
from Memorizer import Memorizer
from RegWriter import RegWriter
from PCUpdater import PCUpdater
from ValBank import ValBank


"""
The following are sate and error libraries for use in displaying
and recording information about the state the processor is in
during each step of running a program. Currently they can be
accessed by print statements, but once a front end is designed
for this processor, these libraries will be used to display
the current state of the error code, and state code.
"""
state_lib = {0: "AOK", 1: "HLT", 2: "ERR"}
error_lib = {0: "", 1: "Index Error", 2: "Opcode Error"}


class Processor:
    """
    This represents the processor itself. Most work and operations
    will be outsourced to other objects referenced by the processor.
    The processor holds the values of valP, valE, valA, valB, valC,
    and rA, rB.
    """

    def __init__(self, mem_size: int = 10000):
        """
                The following is an abstraction for a bank of values
                such as valA, which will be used during each cycle.
                It's set up as an object to avoid circular import.
        """
        self.ValBank = ValBank()
        """
        The following are functional units like memory,
        registers, or flags
        """
        self.Memory = Memory(mem_size)
        self.RegisterBank = RegisterBank()
        self.ZF = CCFlag("ZF")  # zero flag
        self.OF = CCFlag("OF")  # overflow flag
        self.SF = CCFlag("SF")  # sign flag
        self.ErrorFlag = StateFlag("Error Flag", error_lib)
        self.StateFlag = StateFlag("State Flag", state_lib)
        self.ALU = ALU(self.ValBank, self.StateFlag, self.ErrorFlag, self.SF, self.OF, self.ZF)
        """
        The following are functional abstractions of operations
        that the processor performs
        """
        self.Fetcher = Fetcher(self.ValBank, self.RegisterBank, self.Memory, self.StateFlag, self.ErrorFlag)
        self.Decoder = Decoder(self.ValBank, self.RegisterBank, self.Memory)
        self.Executor = Executor(self.ValBank, self.ALU, self.OF, self.ZF, self.SF)
        self.Memorizer = Memorizer(self.ValBank, self.Memory)
        self.RegWriter = RegWriter(self.RegisterBank, self.ValBank)
        self.PCUpdater = PCUpdater(self.RegisterBank, self.ValBank)

    def run(self):
        """
        This is the only necessary public method for the processor.
        Currently the way to operate this is by manually loading values
        into the memory using the place_instruction method, then calling
        the 'run' method for the processor. Afterwards calling print
        on the memory object will reveal the finish state of the processor.
        """
        while self.StateFlag.State == 0:
            self.Fetcher.fetch()
            self.Decoder.decode()
            self.Executor.execute()
            self.Memorizer.memory_write()
            self.RegWriter.write_back()
            self.PCUpdater.update_pc()
