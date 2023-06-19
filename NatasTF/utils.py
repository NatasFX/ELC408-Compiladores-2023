# from NatasTF.parser import code
import sys


def print_error_line(lexpos):
    code = "".join(open(sys.argv[1]).read())
    line_code = code.split('\n')
    for idx, line in enumerate(line_code):
        if lexpos < len(line):
            print('Linha', idx+1, '|', line)
            break
        else:
            lexpos -= len(line) + 1     # +1 por causa do newline
        
    print('-'*(len('Linha '+str(idx+1)+' |')+lexpos+1),end='')
    print('^')