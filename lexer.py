import ply.lex as lex

reserved = {
    # TIPOS
    'char': 'CHAR',
    'real': 'REAL',
    'inteiro': 'INTEIRO',
    'nulo': 'NULO',
    
    # CONDICIONAIS
    'se': 'SE',
    'senao': 'SENAO',
    'entao': 'ENTAO',

    # FUNÇÕES PRÓPRIAS
    'escrever': 'ESCREVER',
    'ler': 'LER',

    # OUTROS
    'enquanto': 'ENQUANTO',
    'principal': 'PRINCIPAL'
}

tokens = list(reserved.values()) + [

    'COMMENT',

    'SUM',
    'SUB',
    'MUL',
    'DIV',

    'NEWLINE',
    'LPAREN',
    'RPAREN',

    'EQUALS',
    'NEQUALS',
    'ATTRIB',
    'MAIOR',
    'MAIOREQ',
    'MENOR',
    'MENOREQ',

    'FIMCMD',
    
    'VERDADEIRO',
    'FALSO',
    'NUM',
    'ID'
]

t_ignore_COMMENT = r'/\*(.|\n)*\*/'

t_SUM = r'\+'
t_SUB = r'\-'
t_MUL = r'\*'
t_DIV = r'/'


t_LPAREN = r'\('
t_RPAREN = r'\)'

t_EQUALS = r'=='
t_NEQUALS = r'!='
t_ATTRIB = r'='
t_MAIOR = r'>'
t_MAIOREQ = r'>='
t_MENOR = r'<'
t_MENOREQ = r'<='

t_FIMCMD = r';'

t_ignore_BRANCO = r'\s+'

def t_VERDADEIRO(t):
    'VERDADEIRO'
    t.value = True
    return t


def t_FALSO(t):
    'FALSO'
    t.value = False
    return t

def t_NUM(t):
    r'\d*\.?\d+'
    t.value = float(t.value)
    return t

def t_ID(t):
    r'[\$_a-zA-Z]\w*'

    t.type = reserved.get(t.value, t.type)

    return t

def t_NEWLINE(t):
    r'\n'
    t.lexer.lineno += 1
    t.lexer.linepos = 0
    pass


def t_error(t):
    nl = '\n'
    print(nl)
    print(t.value.split(nl)[0]) # linha que tem erro
    print(f"^")
    print(f"Erro léxico, token inválido: '{t.value[0]}' linha {t.lineno}")
    exit(1)


lexer = lex.lex()


if __name__ == '__main__':
    data = '''\
    escrever(3.0 + 4 * 10);
    /*a **** ///

    /***

    /*/*/* 1*/*/ a = b;
    '''

    lexer.input(data)
    
    while True:
        tok = lexer.token()
        if not tok: break
        print(tok)
