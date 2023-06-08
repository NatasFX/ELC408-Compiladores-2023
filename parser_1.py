import ply.yacc as yacc
from lexer import *

def get_parser():
    return yacc.yacc()


