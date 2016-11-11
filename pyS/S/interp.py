#!/usr/bin/env
from .language import SProgram
from .RT import InstructionType

class StopProgram(Exception):
    pass

class Variables:
    def __init__(self):
        self._vars = {}

    def set(self, nvar, value):
        if value <= 0:
            self._vars.pop(nvar, None)
        else:
            self._vars[nvar] = value

    def get(self, nvar):
        return self._vars.get(nvar, 0)

class SInterp:
    def __init__(self, code, args={}):
        self._instrlist = list(SProgram(code).decode())
        self._vars = Variables()
        self._lines_by_label = {}
        self._pos = 0
        # Process labels
        last_label = None
        for lineno, rt_inst in enumerate(self._instrlist):
            if rt_inst.label is not None and \
               rt_inst.label != last_label:
                last_label = rt_inst.label
                self._lines_by_label[last_label] = lineno
        # Process arguments
        for nvar, value in args.items():
            self._vars.set(value)

    def rewind(self, args):
        self._pos = 0
        self._vars = Variables()
        # Process arguments
        for nvar, value in args.items():
            self._vars.set(nvar, value)

    def lines(self):
        return len(self._instrlist)

    def pos(self):
        return self._pos

    def list(self, line, n=1):
        if line >= len(self._instrlist) or line < 0:
            raise StopProgram
        start = max(line - n//2, 0)
        end = min(start + n, len(self._instrlist))
        return ((i, self._instrlist[i]) for i in range(start, end))

    def step(self):
        if self._pos >= len(self._instrlist):
            raise StopProgram
        rt_inst = self._instrlist[self._pos]
        if rt_inst.instr_t == InstructionType.Goto and \
           self._vars.get(rt_inst.nvar) != 0:
            if rt_inst.glabel not in self._lines_by_label:
                self._pos = len(it_instr)
                raise StopProgram
            else:
                self._pos = self._lines_by_label[rt_inst.glabel]
                return
        elif rt_inst.instr_t == InstructionType.Increment:
            self._vars.set(rt_inst.nvar, self._vars.get(rt_inst.nvar) + 1)
        elif rt_inst.instr_t == InstructionType.Decrement:
            self._vars.set(rt_inst.nvar, self._vars.get(rt_inst.nvar) - 1)
        self._pos += 1

    def var_value(self, varnum):
        return self._vars.get(varnum)
