import operator
from types import LambdaType
from NatasTF.utils import print_error_line

# Guardamos o contexto das variáveis aqui
# Como essa linguagem não suporta funções
# tratamos elas como escopo global
variaveis = {

}

# Tabela para tradução dos tipos para os tipos da linguagem
_tipos = {
    str: 'char',
    float: 'real',
    int: 'inteiro'
}

# função que obtem a posicao absoluta do lexem no código
err_info = lambda p, n: p.lexpos(n)


# Classe base que usamos como "interface"
class Base:
    error_info = None

    def eval(self):
        try:
            return self._eval()
        except Exception as e:
            error_handler(str(e), self.error_info)

    def _eval(self):
        raise NotImplementedError()


class Identificador(Base):

    def __init__(self, p, name):
        self.error_info = err_info(p, name)
        self.name = p[name]


    def assign(self, val):

        if self.name not in variaveis:
            raise Exception(f'Erro semântico: Variável \'{self.name}\' referenciada mas não declarada.')
        
        if isinstance(val, str): # se forem tipos iguais
            if variaveis[self.name]['type'] == 'char':
                variaveis[self.name]['value'] = val
                return
            else:
                raise Exception(f'Erro semântico: Variável \'{self.name}\' do tipo \'{variaveis[self.name]["type"]}\' incompatível com tipo \'{_tipos[type(val)]}\'')
        
        if variaveis[self.name]['type'] == 'real':
            variaveis[self.name]['value'] = float(val) # atribui float na variavel real
        elif variaveis[self.name]['type'] == 'inteiro':
            variaveis[self.name]['value'] = int(val) # se não for real, é inteiro, então converte
        else:
            raise Exception(f'Erro semântico: Variável \'{self.name}\' do tipo \'{variaveis[self.name]["type"]}\' incompatível com tipo \'{_tipos[type(val)]}\'')


    def _eval(self):
        
        if self.name in variaveis:
            if 'value' not in variaveis[self.name]:
                raise Exception(f'Erro semântico: Variável \'{self.name}\' referenciada mas não inicializada.')
            return variaveis[self.name]['value']
        else:
            raise Exception(f'Erro semântico: Variável \'{self.name}\' não definida.')

    
class Atribuicao(Base):
    def __init__(self, p, ID, value):
        self.error_info = err_info(p, ID) # pegando o ID inves de value
        self.ID = p[ID]
        self.value = p[value]

    def _eval(self):
        self.ID.assign(self.value.eval())


class Var(Base):
    def __init__(self, p, value):
        self.error_info = err_info(p,value)
        self.value = p[value]
        
    def _eval(self): # limpar char
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

    def __init__(self, p, left, op, right):
        self.error_info = err_info(p, op)
        self.left = p[left]
        self.op = p[op]
        self.right = p[right]

    def _eval(self):
        try:
            op = self.ops[self.op]

            if isinstance(op, LambdaType):
                return int(op(self.left, self.right))

            return int(op(self.left.eval(), self.right.eval()))
        except Exception as e:
            raise Exception(f'Erro semântico ao fazer operação binária: {e}. ({self.left} {self.op} {self.right})')



class Comandos(Base):
    def __init__(self, list=None):
        if not list:
            list = []
        self.list = list

    def _eval(self):
        r = []
        for cmd in self.list:
            res = cmd.eval()

            if res: r.append(res)

        return r
    

class Se(Base):
    def __init__(self, p, exp, pv, pf=None):
        self.error_info = err_info(p, exp)
        self.exp = p[exp]
        self.pv = p[pv]
        self.pf = None if not pf else p[pf]

    def _eval(self):
        if self.exp.eval():
            return self.pv.eval()
        elif self.pf:
            return self.pf.eval()
        

class Print(Base):
    def __init__(self, p, arg: Base):
        self.error_info = err_info(p, arg)
        self.arg = p[arg]
    
    def _eval(self):
        s = self.arg.eval()
        print(s if type(s) != str else s.replace('\\n', '\n').replace('\\t', '\t'))


class Ler(Base):
    def __init__(self, p, arg: Base):
        self.error_info = err_info(p, arg)
        self.arg = p[arg]
    
    def _eval(self):
        self.arg.assign(input(f"Variável '{self.arg.name}' recebe: "))


class Enquanto(Base):
    def __init__(self, p, exp, comandos):
        self.error_info = err_info(p, exp)
        self.exp = p[exp]
        self.comandos =p[comandos]

    def _eval(self):
        while self.exp.eval():
            self.comandos.eval()


class OpBinaria(Base):
    def __init__(self, p, left, op, right):
        self.error_info = err_info(p, op)
        self.left = p[left]
        self.op = p[op]
        self.right = p[right]

    def _eval(self):
        left, right = self.left.eval(), self.right.eval()

        try:
            if self.op == '+':
                return left + right
            elif self.op == '-':
                return left - right
            elif self.op == '/':
                return left / right
            elif self.op == '*':
                return left * right

        except ZeroDivisionError:
            raise Exception(f"Erro semântico: Divisão por zero.")
        except:
            raise Exception(f"Erro semântico: operação \'{self.op}\' com tipos ({_tipos[type(left)]}, {_tipos[type(right)]}) não suportado.")


class OpUnaria(Base):
    _ops = {
        '!': lambda x: not x,
        '-': lambda x: -x,
        '+': lambda x: x
    }
    
    def __init__(self, p, arg, op):
        self.error_info = err_info(p, op)
        self.arg = p[arg]
        self.op = p[op]
    
    def _eval(self):
        val = self.arg.eval()
        try:
            return self._ops[self.op](val)
        except:
            raise Exception(f"Erro semântico: operação \'{self.op}\' com tipo {_tipos[type(val)]} não suportado.")



# trata erro encontrado em alguma produção
def error_handler(error, lexpos):
    print('\nErro encontrado! Veja abaixo a linha e a mensagem de erro.\n')
    if not lexpos:
        print('Linha desconhecida.')
    else:
        print_error_line(lexpos)

    print(error)
    exit(1)