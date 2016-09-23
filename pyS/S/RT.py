from enum import Enum

class InstructionType(Enum):
    """Enum for the instruction types
    """
    Assign=0
    Increment=1
    Decrement=2
    Goto=3

class Instruction:
    """Runtime S Instruction

    Attributes:
        label (int):                  Label number at the instruction
                                      or None if instruction is not labeled
        nvar (int):                   Variable number
        instr_t (RT.InstructionType): Type of instruction
        glabel (int):                 Jump label number of goto instruction
    """
    def __init__(self, label, nvar, instr_t, glabel):
        """
        Constructor
        """
        self.label = label
        self.nvar = nvar
        self.instr_t = instr_t
        self.glabel = glabel

    def __str__(self):
        ret = ''
        if self.label is not None:
            ret += 'E_{0}: '.format(self.label)

        if self.instr_t == InstructionType.Assign:
            ret += 'V_{0} <- V_{0}'.format(self.nvar)
        elif self.instr_t == InstructionType.Increment:
            ret += 'V_{0} <- V_{0} + 1'.format(self.nvar)
        elif self.instr_t == InstructionType.Decrement:
            ret += 'V_{0} <- V_{0} - 1'.format(self.nvar)
        else:
            ret += 'IF V_{0} =/= 0 GOTO E_{1}'.format(self.nvar,self.glabel)

        return ret
