import ply.yacc as yacc
from NatasTF.lexer import *
from NatasTF.acao_semantica import *

# informação de precedência para o yacc utilizar na gramática
precedence = (
    ('left', 'NOT'),
    ('left', 'SUM', 'SUB'),
    ('left', 'MUL', 'DIV'),
    ('right', 'USUB'),
    ('right', 'USUM')
)

# pilha utilizada para salvar as variáveis que estão sendo instanciadas no momento
declaracoes = []



#########################################
# DECLARAÇÕES DOS SÍMBOLOS DA GRAMÁTICA #
#########################################

# Cada função tem uma string que representa o que o símbolo a esquerda pode derivar
# Palavras em maiúsculo indicam símbolos não terminais declarados na fase léxica

def p_sem_declaracao(p):
    '''
    declaracao : comandos
    '''

    p[0] = p[1].eval()


def p_declaracao(p):
    '''
    declaracao : dec_variavel comandos
    '''

    p[0] = p[2].eval()

def p_lista_comandos(p):
    '''
    comandos : comando
             | comandos comando
    '''

    if len(p) == 2:
        p[0] = Comandos([p[1]])
    else:
        p[1].list.append(p[2])
        p[0] = p[1]


def p_comando(p):
    '''
    comando : atribuicao FIMCMD
            | print FIMCMD
            | exp FIMCMD
            | leia FIMCMD
            | enquanto
            | if
    '''

    p[0] = p[1]


def p_enquanto(p):
    '''
    enquanto : ENQUANTO LPAREN exp RPAREN LCHAVE comandos RCHAVE
    '''

    p[0] = Enquanto(p[3], p[6])


def p_dec_variavel(p):
    '''
    dec_variavel : tipo lista_nomes fim
                 | dec_variavel dec_variavel
    '''

    declaracoes.clear()
    p[0] = p[1]


# Usado para finalizar a criação das variáveis, pois elas precisam ser
# primeiro instanciadas e depois populadas,
# para evitar fazer gambiarras piores, fiz a menos pior
def p_fim(p):
    '''
    fim : FIMCMD
    '''

    tipo = declaracoes[0]

    for var in declaracoes[1:]:
        variaveis[var] = {'type': tipo}

    p[0] = p[1]


def p_tipo(p):
    '''
    tipo : REAL
         | INTEIRO
         | CHAR
    '''

    declaracoes.append(p[1])
    p[0] = p[1]


def p_lista_nomes(p):
    '''
    lista_nomes : identificador
                | lista_nomes VIRGULA lista_nomes
    '''

    p[0] = p[1]


def p_if(p):
    '''
    if : SE LPAREN exp RPAREN ENTAO LCHAVE comandos RCHAVE SENAO LCHAVE comandos RCHAVE
    '''

    p[0] = Se(p[3], p[7], p[11])
    

def p_if_noelse(p):
    '''
    if : SE LPAREN exp RPAREN ENTAO LCHAVE comandos RCHAVE
    '''

    p[0] = Se(p[3], p[7])


def p_paren(p):
    '''
    exp : LPAREN exp RPAREN
    '''

    p[0] = p[2] if isinstance(p[2], Base) else Var(p[2])


def p_boolean_var(p):
    '''
    boolean : VERDADEIRO
            | FALSO
    '''

    p[0] = p[1]


def p_boolean(p):
    '''
    boolean : comparable EQUALS comparable
            | comparable NEQUALS comparable
            | comparable MAIOR comparable
            | comparable MAIOREQ comparable
            | comparable MENOR comparable
            | comparable MENOREQ comparable
            | comparable BITAND comparable
            | comparable BITOR comparable
    '''

    p[0] = BoolExp(p[1], p[2], p[3])


def p_comparable(p):
    '''
    comparable : NUM
               | boolean
               | identificador
               | exp
    '''

    if isinstance(p[1], Base):
        p[0] = p[1]
    else:
        p[0] = Var(p[1])


def p_operacao_binaria(p):
    '''
    exp : exp SUM exp  %prec SUM
        | exp SUB exp  %prec SUB
        | exp MUL exp  %prec MUL
        | exp DIV exp  %prec DIV
    '''

    p[0] = OpBinaria(p[1], p[2], p[3])


def p_operacao_unaria(p):
    '''
    exp : SUB exp %prec USUB
        | SUM exp %prec USUM
        | NOT exp
    '''

    p[0] = UnaryOp(p[2], p[1])


def p_exp(p):
    '''
    exp : var
        | identificador
    '''

    p[0] = p[1]

def p_var(p):
    '''
    var : NUM
        | CHAR
        | boolean
    '''

    if isinstance(p[1], Base):
        p[0] = p[1]
    else:
        p[0] = Var(p[1])


def p_atribuicao(p):
    '''
    atribuicao : identificador ATTRIB exp
    '''

    p[0] = Atribuicao(p[1], p[3])


def p_identificador(p):
    '''
    identificador : ID
    '''

    declaracoes.append(p[1])
    p[0] = Identificador(p[1])


def p_print(p):
    '''
    print : ESCREVER LPAREN exp RPAREN
    '''

    p[0] = Print(p[3])


def p_ler(p):
    '''
    leia : LER LPAREN identificador RPAREN
    '''

    p[0] = Ler(p[3])


def p_error(p):
    if p is not None:
        print(f"Erro sintático linha {p.lineno}, token inválido '{p.value}' {p.lexpos}")
        exit(1)

    print("ERRO Fim inesperado do arquivo.")
    exit(1)


class Parser():
    def __init__(self):
        self.yacc = yacc.yacc()

    def parse(self, arg):
        self.yacc.parse(arg)
        
def get_parser():
    return Parser()