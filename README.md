# c-minus-compiler
Trabalho da disciplina de Compiladores do curso de Ciência da Computação da Universidade Federal Fluminense.


# Compilador desenvolvido em Python
### Ferramentas necessárias (Windows)
Python - https://www.python.org/

### Como executar
python ./src/compiler.py \<source\> \<tokens\> \<syntree\> -d -v -o

-d: Se o programa deve escrever sua saída no console.

-v: Se a informação escrita no console deve ser detalhada or resumida.

-o: Se o programa deve escrever os tokens no arquivo \<tokens\>, em formato JSON, e a árvore de análise sintática no arquivo \<syntree\>, em formato de texto. 

e.g. python ./src/compiler.py ./src/example1.cminus ./output/example1.tokens.json ./output/example1.syntree.txt -d -v -o

# Compilador desenvolvido em C utilizando Lex & Yacc
### Ferramentas necessárias (Windows)
Flex - https://gnuwin32.sourceforge.net/packages/flex.htm
Bison - https://www.gnu.org/software/bison/

### Como compilar
flex ./lex/cminus.l
bison -d ./yacc/cminus.y
gcc ./cminus.tab.c ./lex.yy.c ./src/lexyacc.c -o lexyacc

### Como executar
./lexyacc ./src/example1.cminus