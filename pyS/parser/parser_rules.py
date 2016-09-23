from .tokens import *
from ..S import RT

class ParserBaseException(Exception):
    def __str__(self):
        return "Parsing error"

class ParserException(ParserBaseException):
    def __init__(self, se, couse, msg):
        self._se = se
        self._couse = couse
        self._msg = msg

    def __str__(self):
        return "Parsing error at line {}: {}: {}".format(self._se.lineno(1),
                                                         self._couse,
                                                         self._msg)
class NotSameVarException(ParserException):
    def __init__(self, se, tok, var1, var2):
        ParserException.__init__(self,
                                 se,
                                 tok,
                                 'V_{0}, V_{1} : Different variables'.format(var1, var2))
def p_error(se):
    if se is None:
        raise ParserBaseException
    elif type(se.value) is tuple:
        raise ParserException(se, "rule " + se.type, "\n\tsubexpression value: " + se.value[0])
    else:
        raise ParserException(se, "rule " + se.type, "\n\tsubexpression value: " + se.value)

def p_instrlist(se):
    """
    instrlist :
              | linstr instrlist
    """
    if len(se) == 3: # linstr instrlist
        se[0] = [se[1]] + se[2]
    else:
        se[0] = []

def p_linstr(se):
    """
    linstr : instr
           | LABEL COLON instr
    """
    if len(se) == 2: # instr
        se[0] = se[1]
    else: # LABEL COLON instr
        temp = se[3]
        temp.label = se[1]
        se[0] = temp


def p_instr_incr(se):
    """
    instr : VAR ASSIGN VAR
    """
    if not se[1] == se[3]:
        raise NotSameVarException(se, se[2], se[1], se[3])
    se[0] = RT.Instruction(label=None,
                         nvar=se[1],
                         instr_t=RT.InstructionType.Assign,
                         glabel = None)

def p_instr_inc(se):
    """
    instr : VAR ASSIGN VAR ADD ONE
    """
    if not se[1] == se[3]:
        raise NotSameVarException(se, se[4], se[1], se[3])
    se[0] = RT.Instruction(label=None,
                         nvar=se[1],
                         instr_t=RT.InstructionType.Increment,
                         glabel = None)

def p_instr_dec(se):
    """
    instr : VAR ASSIGN VAR SUB ONE
    """
    if not se[1] == se[3]:
        raise NotSameVarException(se, se[4], se[1], se[3])
    se[0] = RT.Instruction(label=None,
                         nvar=se[1],
                         instr_t=RT.InstructionType.Decrement,
                         glabel = None)

def p_instr_goto(se):
    """
    instr : IF VAR NOT ZERO GOTO LABEL
    """
    se[0] = RT.Instruction(label=None,
                          nvar=se[2],
                          instr_t=RT.InstructionType.Goto,
                          glabel=se[6])
