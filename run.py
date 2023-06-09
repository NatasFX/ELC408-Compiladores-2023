from NatasTF import get_parser
from sys import stdin

get_parser().parse("\n".join(stdin.readlines()))