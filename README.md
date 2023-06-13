# ELC408-Compiladores-2023
Trabalho Final da Disciplina de Compiladores ELC408 UFSM Professor Giovani Librelotto

O objetivo do trabalho foi a construção de uma linguagem de programação definida pelo professor o qual deveria ser feito um interpretador baseado nas técnicas vistas em aula.


# Execução
Está presente dentro da pasta Examples alguns exemplos de código, após instalar as dependências no arquivo `requirements.txt`, rode-os com `python run.py Examples/nome_arquivo.nfx`.

Eles podem ser alterados a gosto, desde que atendendam a gramática abaixo.

# Gramática

A gramática desta linguagem está abaixo, ela é uma GLC. Está descrita como <Símbolo não terminal> e os símbolos terminais estão representados por si próprios.

Símbolo inicial da gramática: \<declaracao>
```
<declaracao> := <dec_variavel> <comandos>
             |  <comandos>

<comandos> := <comando>
           |  <comandos> <comando>


<comando> := <atribuicao> ;
          |  <print> ;
          |  <exp> ;
          |  <leia> ;
          |  <enquanto>
          |  <if>

<enquanto> := <enquanto> ( <exp> ) { <comandos> }


<dec_variavel> := <tipo> <lista_nomes> <fim>
               |  <dec_variavel> <dec_variavel>

<fim> : ;

<tipo> := real
       |  inteiro
       |  char

<lista_nomes> := <identificador>
              |  <lista_nomes> , <lista_nomes>

<if> := se ( <exp> ) entao { <comandos> } senao { <comandos> }
     |  se ( <exp> ) entao { <comandos> }

<exp> := ( <exp> )
      |  <exp> + <exp>  %prec SUM
      |  <exp> - <exp>  %prec SUB
      |  <exp> * <exp>  %prec MUL
      |  <exp> / <exp>  %prec DIV
      | - <exp> %prec USUB
      | + <exp> %prec USUM
      | ! <exp>
      | <var>
      | <identificador>

<boolean> := verdadeiro
          |  falso

<boolean> := <comparable> == <comparable>
          |  <comparable> != <comparable>
          |  <comparable> >  <comparable>
          |  <comparable> >= <comparable>
          |  <comparable> <  <comparable>
          |  <comparable> <= <comparable>
          |  <comparable> && <comparable>
          |  <comparable> || <comparable>

<comparable> := número
             |  <boolean>
             |  <identificador>
             |  <exp>

<var> := NUM
      | CHAR
      | <boolean>

<atribuicao> : <identificador> = <exp>

<identificador> : ID_lexico

<print> := escrever ( <exp> )

<ler> := ler( <identificador> )
```

Sobre a precedência de operadores, a biblioteca fornece utilitários o qual retiram a necessidade de impor na gramática explicitamente este quesito, são os %prec que estão presentes no final de alguma produção.

# Explicação dos arquivos

## lexer.py
```md
Define quais são os tokens e uma função que trata erro quando um token não é reconhecido.
Esta parte é bem simples pois apenas definindo os tokens a biblioteca já faz todo o restante.
```
## parser.py
```
Neste arquivo está definido a estrutura, formalmente uma Gramática Livre de
Contexto (GLC) que está apresentada acima. Esta parte e o arquivo
acao_semantica.py estão ligados fortemente, pois ele constroi a árvore sintática
com objetos das classes contidas em acao_semantica. Após criada a árvore é feita
uma mágica compilística descrita abaixo etodas as classes são resolvidas em
símbolos corretamente tratados junto da execução do código.
```
## acao_semantica.py
```md
Dentro deste arquivo eu defino diversas classes que são chamadas dentro do
parser.py para que a arvore sintática esteja populada com classes.
Toda classe tem o método eval() que sintetizará um valor para atribuir à
classe pai.

Todo o código aqui é baseado em tradução dirigida por sintaxe. Após 
toda a arvore ser construída, e todo símbolo não terminal convertido em 
uma classe, o símbolo inicial que é <declaracao> inicia o processo de 
evaluation no <comandos> que é a classe Comandos neste arquivo.

Comandos é uma lista de <comando> onde cada comando é uma classe onde 
permite eval(), dessa forma, em ordem, todo código que deriva em 
<comando> será evaluated, desde o símbolo mais ao fundo da árvore até em
cima até que seja utilizado em uma operação ou simplesmente descartado.

Descrevendo o acima:
Código "escrever(1);"

<declaracao> deriva em <comandos>
<comandos> deriva em <escrever> ;
<escrever> deriva em escrever ( <exp> )
<exp> deriva em <var>
<var> deriva em num, que recebe do léxico e cria a classe Var()

<var> retorna e por não ter mais símbolos não terminais que necessitam 
de derivação, todas as outras chamadas de função retornam, criando classes
de si mesma no processo.
Entretanto, a primeira chamada de função, <declaracao>, não cria classe de
si mesma, mas roda o eval() do filho, que é Comandos, o qual chama eval()
de escrever, o qual chama eval() de Exp (que herdou Var), que chama eval()
de Var, o qual retorna seu valor léxico, Exp sobe este valor para a função de 
cima que é escrever, possibilitando ela chamar a função padrão do python
'print' com o argumento recebido, que é 1, realizando o print e retornando nada
para Comando, que retorna nada para Comandos, que finaliza a lista de Comando,
o qual retorna nada e finalmente, a primeira função <declaracao> que construiu
a árvore, terminou a avaliação e execução do código e finalizando ela o
programa finaliza junto.

Um processo que não foi falado foi a criação de variáveis na tabela presente
neste arquivo, o qual foi feito de uma forma diferente, pois como não se pode
declarar variáveis depois de um comando, assim que finalizado a derivação da
árvore em uma declaração de variável, já se popula a tabela com seu ID e 
respectivo tipo. Mantive desta forma por motivos didáticos, pois tem-se mais
de uma forma de realizar a mesma coisa.
```