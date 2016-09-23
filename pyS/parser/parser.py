from ply.lex import lex
from ply.yacc import yacc

from ..S.language import SProgram

from . import lexer_rules
from . import parser_rules

def parse(strcode):
    lexer = lex(module=lexer_rules)
    parser = yacc(module=parser_rules)

    return SProgram.encode(parser.parse(strcode, lexer))
