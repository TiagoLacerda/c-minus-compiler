import string
from typing import *

from enumProducoes import Producao
from syNode import SyNode
from token import Token


class SyParserTokenException(Exception):
    def __init__(self, token):
        self.erro = "Erro sintatico - linha: {} , coluna: {} \n Token problemático: {} \n".format(token.line, token.column, token.value)
        super().__init__(self.erro)

# Declarando Classe do Analisador Sintatico
class SyParser():

    # Metodo construtor da classe
    def __init__(
            self,
            entrada : List[ Token ] = [],
            posicao_token_atual : int = 0,
            saida : string = ""

        ):

        self.entrada = entrada
        self.posicao_token_atual = posicao_token_atual
        self.saida = saida
        
    # Faz o cabecote de leitura apontar para o proximo token da lista
    def next_token(self):
        self.posicao_token_atual += 1
        
    # Dá match com terminal e cria folha do terminal na arvore
    def match_terminal(self, parent: SyNode, expectedTokenTag: string):
        if self.posicao_token_atual >= len(self.entrada):
            return False
        if (self.entrada[self.posicao_token_atual].tags[0]==expectedTokenTag):
            folha_terminal = SyNode(parent=parent, symbol=None, token=self.entrada[self.posicao_token_atual], level=parent.level+1)
            parent.add_children(folha_terminal)
            self.next_token()
            return True
        return False

    def parse(self) -> SyNode:
        return self.program()

    # <program> -> <declaration-list>
    def program(self):
        raiz = SyNode(symbol=Producao.PROGRAM) 
        self.declaration_list(raiz)

        if(self.posicao_token_atual < len(self.entrada)):
            raise SyParserTokenException(self.entrada[self.posicao_token_atual])

        print(raiz)
        print("\nPassou no analisador sintatico!")
        return raiz


    # <declaration-list> -> <declaration> <declaration-list'>
    def declaration_list(self, parent: SyNode):
        novo_no = SyNode(symbol=Producao.DECLARATION_LIST, parent=parent, level=parent.level+1) 

        if (self.declaration(novo_no)):
            self.declaration_list_linha(novo_no)
            parent.add_children(child=novo_no)
            return True
        
        return False

    # <declaration> -> <var-declaration> | <fun-declaration>
    def declaration(self, parent: SyNode):
        novo_no = SyNode(symbol=Producao.DECLARATION, parent=parent, level=parent.level+1) 
        posicao_token_no_atual = self.posicao_token_atual

        if (self.var_declaration(novo_no)):
            parent.add_children(novo_no)
            return True

        self.posicao_token_atual = posicao_token_no_atual
        novo_no.children.clear()

        if (self.fun_declaration(novo_no)):
            parent.add_children(novo_no)
            return True

        return False

    # <declaration-list'> -> <declaration-list> | epsilon
    def declaration_list_linha(self, parent: SyNode):
        novo_no = SyNode(symbol=Producao.DECLARATION_LIST_LINHA, parent=parent, level=parent.level+1) 
        posicao_token_no_atual = self.posicao_token_atual

        if (self.declaration_list(novo_no)):
            parent.add_children(novo_no)
            return True

        self.posicao_token_atual = posicao_token_no_atual
        return False

    # <var-declaration> -> <type-spec> id [ num ] ; | <type-spec> id ;
    def var_declaration(self, parent: SyNode):
        novo_no = SyNode(symbol=Producao.VAR_DECLARATION, parent=parent, level=parent.level+1) 

        if (self.type_spec(novo_no)):
            if (self.match_terminal(parent=novo_no, expectedTokenTag="id")):
                posicao_token_no_atual = self.posicao_token_atual
                if (self.match_terminal(parent=novo_no, expectedTokenTag="semicolon")):
                    parent.add_children(novo_no)
                    return True

            self.posicao_token_atual = posicao_token_no_atual
            if (self.match_terminal(parent=novo_no, expectedTokenTag="open_square_brackets")):
                if (self.match_terminal(parent=novo_no, expectedTokenTag="num")):
                    if (self.match_terminal(parent=novo_no, expectedTokenTag="close_square_brackets")):
                        if (self.match_terminal(parent=novo_no, expectedTokenTag="semicolon")):
                            parent.add_children(novo_no)
                            return True

        return False

    # <type-spec> -> int | void
    def type_spec(self, parent: SyNode):
        novo_no = SyNode(symbol=Producao.TYPE_SPECIFIER, parent=parent, level=parent.level+1) 

        if (self.match_terminal(parent=novo_no , expectedTokenTag="int")):
            parent.add_children(novo_no)
            return True

        if (self.match_terminal(parent=novo_no , expectedTokenTag="void")):
            parent.add_children(novo_no)
            return True

        return False


    # <fun-declaration> -> <type-spec> id ( <params> ) <compound-stmt> 
    def fun_declaration(self, parent: SyNode):
        novo_no = SyNode(symbol=Producao.FUN_DECLARATION, parent=parent, level=parent.level+1) 

        if (self.type_spec(novo_no)):
            if (self.match_terminal(parent=novo_no, expectedTokenTag="id")):
                if (self.match_terminal(parent=novo_no,expectedTokenTag="open_parenthesis")):
                    if (self.params(novo_no)):
                        if (self.match_terminal(parent=novo_no,expectedTokenTag="close_parenthesis")):
                            if (self.compound_statement(novo_no)):
                                parent.add_children(novo_no)
                                return True
                            
        return False

    # <params> -> <param-list> | void
    def params(self, parent: SyNode):
        novo_no = SyNode(symbol=Producao.PARAMS, parent=parent, level=parent.level+1) 
        posicao_token_no_atual = self.posicao_token_atual

        if (self.param_list(novo_no)):
            parent.add_children(novo_no)
            return True
        
        self.posicao_token_atual = posicao_token_no_atual
        novo_no.children.clear()

        if (self.match_terminal(parent=novo_no , expectedTokenTag="void")):
            parent.add_children(novo_no)
            return True

        return False

    # <param-list> -> <param> <param-list'>
    def param_list(self, parent: SyNode):
        novo_no = SyNode(symbol=Producao.PARAM_LIST, parent=parent, level=parent.level+1) 

        if (self.param(novo_no)):
            self.param_list_linha(novo_no)
            parent.add_children(novo_no)
            return True
            
        return False

    # <param> -> <type-spec> id [] | <type-spec> id
    def param(self, parent: SyNode):
        novo_no = SyNode(symbol=Producao.PARAM, parent=parent, level=parent.level+1) 

        if (self.type_spec(novo_no)):
            if (self.match_terminal(parent=novo_no, expectedTokenTag="id")):
                posicao_token_no_atual = self.posicao_token_atual
                if (self.match_terminal(parent=novo_no, expectedTokenTag="open_square_brackets")):
                    if (self.match_terminal(parent=novo_no, expectedTokenTag="close_square_brackets")):
                        parent.add_children(novo_no)
                        return True

                self.posicao_token_atual = posicao_token_no_atual
                parent.add_children(novo_no)
                return True

        return False

    # <param-list'> -> , <param> <param-list'> | epsilon
    def param_list_linha(self, parent: SyNode):
        novo_no = SyNode(symbol=Producao.PARAM_LIST_LINHA, parent=parent, level=parent.level+1) 
        posicao_token_no_atual = self.posicao_token_atual

        if (self.match_terminal(parent=novo_no, expectedTokenTag="comma")):
            if (self.param(novo_no)):
                self.param_list_linha(novo_no)
                parent.add_children(novo_no)
                return True
        
        self.posicao_token_atual = posicao_token_no_atual
        return False

    # <compound-stmt> -> { <local-decl> <stmt-list> }
    def compound_statement(self, parent: SyNode):
        novo_no = SyNode(symbol=Producao.COMPOUND_STMT, parent=parent, level=parent.level+1) 

        if (self.match_terminal(parent=novo_no, expectedTokenTag="open_brackets")):
            if (self.local_decl(novo_no)):
                if (self.statement_list(novo_no)):
                    if (self.match_terminal(parent=novo_no,expectedTokenTag="close_brackets")):
                        parent.add_children(novo_no)
                        return True
                            
        return False
    
    # <local-decl> -> <var-decl> <local-decl'> | epsilon
    def local_decl(self, parent: SyNode):
        novo_no = SyNode(symbol=Producao.LOCAL_DECLARATIONS, parent=parent, level=parent.level+1) 
        posicao_token_no_atual = self.posicao_token_atual

        if (self.var_declaration(novo_no)):
            self.local_decl_linha(novo_no)
            parent.add_children(novo_no)

        else:
            self.posicao_token_atual = posicao_token_no_atual

        return True

    # <local-decl'> -> <local-decl>
    def local_decl_linha(self, parent: SyNode):
        novo_no = SyNode(symbol=Producao.LOCAL_DECLARATIONS_LINHA, parent=parent, level=parent.level+1) 

        if (self.local_decl(novo_no)):
            parent.add_children(novo_no)
            return True
            
        return False

    # <stmt-list> -> <stmt-list'>
    def statement_list(self, parent: SyNode):
        novo_no = SyNode(symbol=Producao.STATEMENT_LIST, parent=parent, level=parent.level+1) 

        if (self.statement_list_linha(novo_no)):
            parent.add_children(novo_no)
            return True
            
        return False

    # <stmt-list'> -> <statement> <stmt-list> | epsilon
    def statement_list_linha(self, parent: SyNode):
        novo_no = SyNode(symbol=Producao.STATEMENT_LIST_LINHA, parent=parent, level=parent.level+1) 
        posicao_token_no_atual = self.posicao_token_atual

        if (self.statement(novo_no)):
            self.statement_list(novo_no)
            parent.add_children(novo_no)
            
        else:
            self.posicao_token_atual = posicao_token_no_atual

        return True

    # <statement> -> <exp-stmt> | <compound-stmt> | <select-stmt> | <iter-stmt> | <return-stmt> 
    def statement(self, parent: SyNode):
        novo_no = SyNode(symbol=Producao.STATEMENT, parent=parent, level=parent.level+1) 
        posicao_token_no_atual = self.posicao_token_atual

        if (self.expression_statement(novo_no)):
            parent.add_children(novo_no)
            return True

        self.posicao_token_atual = posicao_token_no_atual
        novo_no.children.clear()

        if (self.compound_statement(novo_no)):
            parent.add_children(novo_no)
            return True
            
        self.posicao_token_atual = posicao_token_no_atual
        novo_no.children.clear()

        if (self.select_statement(novo_no)):
            parent.add_children(novo_no)
            return True
        
        self.posicao_token_atual = posicao_token_no_atual
        novo_no.children.clear()

        if (self.iteration_statement(novo_no)):
            parent.add_children(novo_no)
            return True

        self.posicao_token_atual = posicao_token_no_atual
        novo_no.children.clear()

        if (self.return_statement(novo_no)):
            parent.add_children(novo_no)
            return True
        
        return False

    # <expression-stmt> -> <expression> ; | ;
    def expression_statement(self, parent: SyNode):
        novo_no = SyNode(symbol=Producao.EXPRESSION_STMT, parent=parent, level=parent.level+1) 
        posicao_token_no_atual = self.posicao_token_atual

        if (self.expression(novo_no)):
            if (self.match_terminal(parent=novo_no, expectedTokenTag="semicolon")):
                parent.add_children(novo_no)
                return True
            
        self.posicao_token_atual = posicao_token_no_atual
        novo_no.children.clear()

        if (self.match_terminal(parent=novo_no, expectedTokenTag="semicolon")):
            parent.add_children(novo_no)
            return True
            
        return False

    # <select_statement> -> if ( <expression> ) <statement> | if ( <expression> ) <statement> else <statement>
    def select_statement(self, parent: SyNode):
        novo_no = SyNode(symbol=Producao.SELECTION_STMT, parent=parent, level=parent.level+1) 
        posicao_token_no_atual = self.posicao_token_atual

        if (self.match_terminal(parent=novo_no, expectedTokenTag="if")):
            if (self.match_terminal(parent=novo_no, expectedTokenTag="open_parenthesis")):
                if (self.expression(novo_no)):
                    if (self.match_terminal(parent=novo_no, expectedTokenTag="close_parenthesis")):
                        if (self.statement(novo_no)):
                            posicao_token_no_atual = self.posicao_token_atual
                            if (self.match_terminal(parent=novo_no, expectedTokenTag="else")):
                                if (self.statement(novo_no)):
                                    parent.add_children(novo_no)
                                    return True

                            self.posicao_token_atual = posicao_token_no_atual
                            parent.add_children(novo_no)
                            return True

        return False

    # <iteration_statement> -> while ( <expression> ) <statement>
    def iteration_statement(self, parent: SyNode):
        novo_no = SyNode(symbol=Producao.ITERATION_STMT, parent=parent, level=parent.level+1) 

        if (self.match_terminal(parent=novo_no, expectedTokenTag="while")):
            if (self.match_terminal(parent=novo_no, expectedTokenTag="open_parenthesis")):
                if (self.expression(novo_no)):
                    if (self.match_terminal(parent=novo_no, expectedTokenTag="close_parenthesis")):
                        if (self.statement(novo_no)):
                            parent.add_children(novo_no)
                            return True

        return False

    # <return_statement> -> return <expression> ; | return ;
    def return_statement(self, parent: SyNode):
        novo_no = SyNode(symbol=Producao.RETURN_STMT, parent=parent, level=parent.level+1) 

        if (self.match_terminal(parent=novo_no, expectedTokenTag="return")):
            if (self.expression_statement(novo_no)):
                parent.add_children(novo_no)
                return True

        return False

    # <expression> -> <simple-exp> | <var> = <expression>
    def expression(self, parent: SyNode):
        novo_no = SyNode(symbol=Producao.EXPRESSION, parent=parent, level=parent.level+1) 
        posicao_token_no_atual = self.posicao_token_atual

        if (self.var(novo_no)):
            if (self.match_terminal(parent=novo_no, expectedTokenTag="assing")):
                if (self.expression(novo_no)):
                    parent.add_children(novo_no)
                    return True

        self.posicao_token_atual = posicao_token_no_atual
        novo_no.children.clear()

        if (self.simple_expression(novo_no)):
            parent.add_children(novo_no)
            return True

        return False

    # <var> -> id [ <expression> ] | id ;
    def var(self, parent: SyNode):
        novo_no = SyNode(symbol=Producao.VAR, parent=parent, level=parent.level+1) 

        if (self.match_terminal(parent=novo_no, expectedTokenTag="id")):
            posicao_token_no_atual = self.posicao_token_atual
            if (self.match_terminal(parent=novo_no, expectedTokenTag="open_square_brackets")):
                if (self.expression(novo_no)):
                    if (self.match_terminal(parent=novo_no, expectedTokenTag="close_square_brackets")):
                        parent.add_children(novo_no)
                        return True
  
            self.posicao_token_atual = posicao_token_no_atual
            parent.add_children(novo_no)
            return True

        return False

    # <simple-expression> -> <additive-expression> <relop> <additive-expression> | <additive-expression>
    def simple_expression(self, parent: SyNode):
        novo_no = SyNode(symbol=Producao.SIMPLE_EXPRESSION, parent=parent, level=parent.level+1) 

        if (self.additive_expression(novo_no)):
            posicao_token_no_atual = self.posicao_token_atual
            if (self.relop(novo_no)):
                if (self.additive_expression(novo_no)):
                    parent.add_children(novo_no)
                    return True
                              
            self.posicao_token_atual = posicao_token_no_atual
            parent.add_children(novo_no)
            return True

        return False

    # <relop> ->  <= | < | > | >= | == | != 
    def relop(self, parent: SyNode):
        novo_no = SyNode(symbol=Producao.RELOP, parent=parent, level=parent.level+1) 

        if (self.match_terminal(parent=novo_no, expectedTokenTag="le")):
            parent.add_children(novo_no)
            return True

        if (self.match_terminal(parent=novo_no, expectedTokenTag="lt")):
            parent.add_children(novo_no)
            return True

        if (self.match_terminal(parent=novo_no, expectedTokenTag="gt")):
            parent.add_children(novo_no)
            return True

        if (self.match_terminal(parent=novo_no, expectedTokenTag="ge")):
            parent.add_children(novo_no)
            return True

        if (self.match_terminal(parent=novo_no, expectedTokenTag="eq")):
            parent.add_children(novo_no)
            return True

        if (self.match_terminal(parent=novo_no, expectedTokenTag="ne")):
            parent.add_children(novo_no)
            return True
        
        return False

    # <additive-expression> -> <term> <additive-expression'>
    def additive_expression(self, parent: SyNode):
        novo_no = SyNode(symbol=Producao.ADDITIVE_EXPRESSION, parent=parent, level=parent.level+1) 

        if (self.term(novo_no)):
            self.additive_expression_linha(novo_no)
            parent.add_children(novo_no)
            return True

        return False

    # <additive-expression> -> <addop> <additive-expression> | epsilon
    def additive_expression_linha(self, parent: SyNode):
        novo_no = SyNode(symbol=Producao.ADDITIVE_EXPRESSION_LINHA, parent=parent, level=parent.level+1) 
        posicao_token_no_atual = self.posicao_token_atual

        if (self.addop(novo_no)):
            if (self.additive_expression(novo_no)):
                parent.add_children(novo_no)
                return True

        self.posicao_token_atual = posicao_token_no_atual
        return False

    # <addop> ->  + | - 
    def addop(self, parent: SyNode):
        novo_no = SyNode(symbol=Producao.ADDOP, parent=parent, level=parent.level+1) 

        if (self.match_terminal(parent=novo_no, expectedTokenTag="plus")):
            parent.add_children(novo_no)
            return True

        if (self.match_terminal(parent=novo_no, expectedTokenTag="minus")):
            parent.add_children(novo_no)
            return True
        
        return False

    # <term> -> <factor> <term'>
    def term(self, parent: SyNode):
        novo_no = SyNode(symbol=Producao.TERM, parent=parent, level=parent.level+1) 

        if (self.factor(novo_no)):
            self.term_linha(novo_no)
            parent.add_children(novo_no)
            return True

        return False

    # <term'> -> <mulop> <term> | epsilon
    def term_linha(self, parent: SyNode):
        novo_no = SyNode(symbol=Producao.TERM_LINHA, parent=parent, level=parent.level+1) 
        posicao_token_no_atual = self.posicao_token_atual

        if (self.mulop(novo_no)):
            if (self.term(novo_no)):
                parent.add_children(novo_no)
                return True

        self.posicao_token_atual = posicao_token_no_atual
        return False

    # <mulop> ->  * | / 
    def mulop(self, parent: SyNode):
        novo_no = SyNode(symbol=Producao.MULOP, parent=parent, level=parent.level+1) 

        if (self.match_terminal(parent=novo_no, expectedTokenTag="asterisk")):
            parent.add_children(novo_no)
            return True

        if (self.match_terminal(parent=novo_no, expectedTokenTag="slash")):
            parent.add_children(novo_no)
            return True
        
        return False

    # <factor> -> ( <expression> ) | <var> | <call> | num
    def factor(self, parent: SyNode):
        novo_no = SyNode(symbol=Producao.FACTOR, parent=parent, level=parent.level+1) 
        posicao_token_no_atual = self.posicao_token_atual

        if (self.match_terminal(parent=novo_no, expectedTokenTag="open_parenthesis")):
            if (self.expression(novo_no)):
                if (self.match_terminal(parent=novo_no, expectedTokenTag="close_parenthesis")):
                    parent.add_children(novo_no)
                    return True
            return False

        self.posicao_token_atual = posicao_token_no_atual

        if (self.var(novo_no)):
            parent.add_children(novo_no)
            return True

        self.posicao_token_atual = posicao_token_no_atual
        novo_no.children.clear()

        if (self.call(novo_no)):
            parent.add_children(novo_no)
            return True

        self.posicao_token_atual = posicao_token_no_atual
        novo_no.children.clear()

        if (self.match_terminal(parent=novo_no, expectedTokenTag="num")):
            parent.add_children(novo_no)
            return True

        return False

    # <call> -> id ( <args> )
    def call(self, parent: SyNode):
        novo_no = SyNode(symbol=Producao.CALL, parent=parent, level=parent.level+1) 

        if (self.match_terminal(parent=novo_no, expectedTokenTag="id")):
            if (self.match_terminal(parent=novo_no,expectedTokenTag="open_parenthesis")):
                if (self.args(novo_no)):
                    if (self.match_terminal(parent=novo_no,expectedTokenTag="close_parenthesis")):
                        parent.add_children(novo_no)
                        return True
                            
        return False

    # <args> -> <arg-list> | epsilon
    def args(self, parent: SyNode):
        novo_no = SyNode(symbol=Producao.ARGS, parent=parent, level=parent.level+1) 

        self.arg_list(novo_no)
        parent.add_children(novo_no)
        return True

    # <arg-list> -> <expression> <arg-list'>
    def arg_list(self, parent: SyNode):
        novo_no = SyNode(symbol=Producao.ARG_LIST, parent=parent, level=parent.level+1) 

        if (self.expression(novo_no)):
            self.arg_list_linha(novo_no)
            parent.add_children(novo_no)
            return True

        return False

    # <arg-list'> -> , <arg-list> | epsilon
    def arg_list_linha(self, parent: SyNode):
        novo_no = SyNode(symbol=Producao.ARG_LIST_LINHA, parent=parent, level=parent.level+1) 
        posicao_token_no_atual = self.posicao_token_atual

        if (self.match_terminal(parent=novo_no, expectedTokenTag="comma")):
            if (self.arg_list(novo_no)):
                parent.add_children(novo_no)
                return True
        
        self.posicao_token_atual = posicao_token_no_atual
        return False
                   
