import operator
from types import LambdaType

# Guardamos o contexto das variáveis aqui
# Como essa linguagem não suporta funções
# tratamos elas como escopo global
variaveis = {

}

# Classe base que usamos como "interface"
class Base:
    def eval(self):
        raise NotImplementedError()

class Identificador(Base):

    _tipos = {str: 'char',
             float: 'real',
             int: 'inteiro'}

    def __init__(self, name):
        self.name = name

    def assign(self, val):

        if self.name not in variaveis:
            print(f'Variável \'{self.name}\' referenciada mas não declarada.')
            exit(1)
        
        # se for string
        if isinstance(val, str):
            if variaveis[self.name]['type'] == 'char': # tipos iguais, show
                variaveis[self.name]['value'] = val
                return
            
            try:
                val = float(val)
            except:
                print(f'Erro de atribuição: Variável \'{self.name}\' do tipo \'{variaveis[self.name]["type"]}\' incompatível com tipo \'{self._tipos[type(val)]}\'')
                exit(1)
        
        if variaveis[self.name]['type'] == 'real':
            variaveis[self.name]['value'] = float(val) # atribui float na variavel real
        else:
            variaveis[self.name]['value'] = int(val) # se não for real, é inteiro, então converte


    def eval(self):
        
        if self.name in variaveis:
            if 'value' not in variaveis[self.name]:
                print(f'Erro em tempo de execução: Variável \'{self.name}\' referenciada mas não inicializada.')
                exit(1)
            return variaveis[self.name]['value']
        else:
            print(f'Erro em tempo de execução: Variável \'{self.name}\' não definida.')
            exit(1)

class Atribuicao(Base):
    def __init__(self, ID: Identificador, value):
        self.ID = ID
        self.value = value

    def eval(self):
        self.ID.assign(self.value.eval())

class Var(Base):
    def __init__(self, value):
        self.value = value

    def eval(self): # limpar char
        return self.value.strip('\'') if type(self.value) == str else self.value

class BoolExp(Base):
    ops = {
        '>' : operator.gt,
        '>=': operator.ge,
        '<' : operator.lt,
        '<=': operator.le,
        '==': operator.eq,
        '!=': operator.ne,

        '&&': lambda a, b: a.eval() and b.eval(),
        '||': lambda a, b: a.eval() or b.eval()
    }

    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def eval(self):
        try:
            op = self.ops[self.op]

            if isinstance(op, LambdaType):
                return op(self.left, self.right)

            return op(self.left.eval(), self.right.eval())
        except Exception as e:
            print(f'Erro em tempo de execução ao fazer operação binária: {e}. ({self.left} {op} {self.right})')
            exit(1)


class Comandos:
    def __init__(self, list=None):
        if not list:
            list = []
        self.list = list

    def eval(self):
        ret = []
        for n in self.list:
            res = n.eval()

            if res: ret.append(res)

        return ret
    
class Se(Base):
    def __init__(self, exp: Base, pv: Comandos, pf=None):
        self.exp = exp
        self.pv = pv
        self.pf = pf

    def eval(self):
        if self.exp.eval():
            return self.pv.eval()
        elif self.pf:
            return self.pf.eval()
        

class Print(Base):
    def __init__(self, arg: Base):
        self.arg = arg
    
    def eval(self):
        s = self.arg.eval()
        print(s if type(s) != str else s.replace('\\n', '\n').replace('\\t', '\t'))

class Ler(Base):
    def __init__(self, arg: Base):
        self.arg = arg
    
    def eval(self):
        self.arg.assign(input(f"Variável '{self.arg.name}' recebe: "))

class Enquanto(Base):
    def __init__(self, exp: Base, comandos: Comandos):
        self.exp = exp
        self.comandos = comandos

    def eval(self):
        while self.exp.eval():
            self.comandos.eval()
        

class OpBinaria(Base):
    def __init__(self, left: Base, op: str, right: Base):
        self.left = left
        self.op = op
        self.right = right

    def eval(self):
        left, right = self.left.eval(), self.right.eval()

        tleft, tright = type(left), type(right)

        if tleft != tright and str in [tleft, tright]:
            print(f"Soma de tipos ({tleft.__name__}, {tright.__name__}) não suportado.")
            exit(1)

        if self.op == '+':
            return left + right
        elif self.op == '-':
            return left - right
        elif self.op == '/':
            return left / right
        elif self.op == '*':
            return left * right
