from .datatypes import SInt, STuple, SList
from . import RT

class SInstruction(SInt):
    """S Instruction
    """
    def __init__(self, z):
        SInt.__init__(self, z)

    def decode(self):
        """Decodes S Instruction into a S Runtime Instruction
        """
        (a, y) = STuple(self.z).decode()
        (b, c) = STuple(y).decode()
        return RT.Instruction(label   = a if not a == 0 else None,
                              nvar    = c + 1,
                              instr_t = RT.InstructionType(b)
                                        if b <= 2 else \
                                        RT.InstructionType.Goto,
                              glabel  = b-2 if b > 2 else None)

    @staticmethod
    def encode(rt_inst):
        """Encodes RT.Instruction into a SInstruction

        Attributes:
            rt_inst (RT.Instruction) : Runtime Instruction to encode
        """
        a = rt_inst.label if rt_inst.label is not None else 0
        c = rt_inst.nvar - 1
        if rt_inst.instr_t == RT.InstructionType.Goto:
            b = rt_inst.glabel + 2
        else:
            b = rt_inst.instr_t.value

        return SInstruction(STuple.encode((a, STuple.encode((b, c)).z)))

class SProgram(SList):
    """S Code
    """
    def __init__(self, z):
        SList.__init__(self, z)

    def decode(self):
        """Decodes SProgram into a list of RT.Instruction

        Yields:
            Runtime Instruction per line
        """
        return (SInstruction(i).decode() for i in super(SProgram, self).decode())

    @staticmethod
    def encode(rits):
        """Encodes list of RT.Instruction into a SProgram

        Attributes:
            rits (iterable of RT.Instruction): Runtime Instructions
        """
        return SProgram(SList.encode([SInstruction.encode(rit).z for rit in rits]))

    def __str__(self):
        return "\n".join(map(str, self.decode()))
