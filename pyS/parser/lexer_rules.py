from .tokens import *

class LexerException(Exception):
    def __init__(self, lineno, colno, msg):
        self._lineno = lineno
        self._colno = colno
        self._msg = msg

    def __str__(self):
        return "Lexer error at line {}, column {}: {}".format(self._lineno,
                                                              self._colno,
                                                              self._msg)

def t_error(tok):
    msg = "Unknown token " + str(tok.value)
    raise LexerException(tok.lineno, tok.lexpos, msg)

def t_IGNORE(tok):
    r"\n+"
    tok.lexer.lineno += len(tok.value)

def t_LABEL(tok):
    r"E_[1-9][0-9]*"
    tok.value = int(tok.value[2:])
    return tok

def t_VAR(tok):
    r"V_[0-9]+"
    tok.value = int(tok.value[2:])
    return tok

t_ignore_WHITESPACES = r"[ \t]"
t_ASSIGN = r"<-"
t_ADD = r"\+"
t_SUB = r"\-"
t_NOT = r"=/="
t_COLON = r":"
t_ZERO = r"0"
t_ONE = r"1"
t_IF = r"IF"
t_GOTO = r"GOTO"
