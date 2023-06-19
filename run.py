#!/usr/bin/python3
from NatasTF import get_parser
import sys

if len(sys.argv) <= 1:
    print(f'Uso: ./run.py [Arquivo de entrada]')
    exit(1)

_input = "".join(open(sys.argv[1]).read())

get_parser().parse(_input)