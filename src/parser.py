from typing import *
from enumProducoes import Producao
from syNode import SyNode
from token import Token
import string

# Declarando Classe do Analisador Sintatico
class Parser():

    # Metodo construtor da classe
    def __init__(
            self,
            tem_erro_sintatico : bool = False,
            erro_sintatico: string = "",
            entrada : List = [],
            posicao_token_atual : int = 0,
            saida : string = ""

        ):

        self.entrada = entrada
        self.posicao_token_atual = posicao_token_atual
        self.tem_erro_sintatico = tem_erro_sintatico
        self.erro_sintatico = erro_sintatico
        self.saida = saida
        
    # Faz o cabecote de leitura apontar para o proximo token da lista
    def next_token(self):
        self.posicao_token_atual += 1
        
    # Dá match com terminal e cria folha do terminal na arvore
    def match_terminal(self, parent: SyNode, expectedTokenTag: str):
        if self.posicao_token_atual >= len(self.entrada):
            return False
        if (self.entrada[self.posicao_token_atual].tags[0]==expectedTokenTag):
            folha_terminal = SyNode(parent=parent, symbol=None, token=self.entrada[self.posicao_token_atual])
            parent.add_children(folha_terminal)
            self.next_token()
            return True
        else:
            self.erro()
        return False

    def erro(self):
        self.erro_sintatico = "Erro sintatico - linha: " + self.entrada[self.posicao_token_atual].line + " , coluna: " + self.entrada[self.posicao_token_atual].column + "\n" + " Token problemático: " + self.entrada[self.posicao_token_atual].value + "\n"
        self.tem_erro_sintatico = True
        print(self.erro_sintatico)


    def parse(self) -> SyNode:
        return self.program()

    # <program> -> <declaration-list>
    def program(self):
        raiz = SyNode(symbol=Producao.PROGRAM) 
        self.declaration_list(raiz)

        if(self.posicao_token_atual < len(self.entrada)):
            self.erro()

        return raiz


    # <declaration-list> -> <declaration> <declaration-list'>
    def declaration_list(self, parent: SyNode):
        novo_no = SyNode(symbol=Producao.DECLARATION_LIST) 

        if (self.declaration(novo_no)):
            self.declaration_list_linha(novo_no)
            parent.add_children(novo_no)
            return True
        
        return False

    # <declaration> -> <var-declaration> | <fun-declaration>
    def declaration(self, parent: SyNode):
        novo_no = SyNode(symbol=Producao.DECLARATION) 
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
        novo_no = SyNode(symbol=Producao.DECLARATION_LIST_LINHA) 
        posicao_token_no_atual = self.posicao_token_atual

        if (self.declaration_list(novo_no)):
            parent.add_children(novo_no)
            return True

        self.posicao_token_atual = posicao_token_no_atual
        return False

    # <var-declaration> -> <type-spec> id [ num ] ; | <type-spec> id ;
    def var_declaration(self, parent: SyNode):
        novo_no = SyNode(symbol=Producao.VAR_DECLARATION) 

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
        novo_no = SyNode(symbol=Producao.TYPE_SPECIFIER) 

        if (self.match_terminal(parent=novo_no , expectedTokenTag="int")):
            parent.add_children(novo_no)
            return True

        if (self.match_terminal(parent=novo_no , expectedTokenTag="void")):
            parent.add_children(novo_no)
            return True

        return False


    # <fun-declaration> -> <type-spec> id ( <params> ) <compound-stmt> 
    def fun_declaration(self, parent: SyNode):
        novo_no = SyNode(symbol=Producao.FUN_DECLARATION) 

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
        novo_no = SyNode(symbol=Producao.PARAMS) 
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
        novo_no = SyNode(symbol=Producao.PARAM_LIST) 

        if (self.param(novo_no)):
            self.param_list_linha(novo_no)
            parent.add_children(novo_no)
            return True
            
        return False

    # <param> -> <type-spec> id [] | <type-spec> id
    def param(self, parent: SyNode):
        novo_no = SyNode(symbol=Producao.PARAM) 

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
        novo_no = SyNode(symbol=Producao.PARAM_LIST_LINHA) 
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
        novo_no = SyNode(symbol=Producao.COMPOUND_STMT) 

        if (self.match_terminal(parent=novo_no, expectedTokenTag="open_brackets")):
            if (self.local_decl(novo_no)):
                if (self.statement_list(novo_no)):
                    if (self.match_terminal(parent=novo_no,expectedTokenTag="close_brackets")):
                        parent.add_children(novo_no)
                        return True
                            
        return False
    
    # <local-decl> -> <local-decl'>
    def local_decl(self, parent: SyNode):
        novo_no = SyNode(symbol=Producao.LOCAL_DECLARATIONS) 

        if (self.local_decl_linha(novo_no)):
            parent.add_children(novo_no)
            return True
            
        return False
    
    # <local-decl'> -> <var-decl> <local-decl'> | epsilon
    def local_decl_linha(self, parent: SyNode):
        novo_no = SyNode(symbol=Producao.LOCAL_DECLARATIONS_LINHA) 
        posicao_token_no_atual = self.posicao_token_atual

        if (self.var_declaration(novo_no)):
            self.local_decl_linha(novo_no)
            parent.add_children(novo_no)
            return True
        
        self.posicao_token_atual = posicao_token_no_atual
        return False

    # <stmt-list> -> <stmt-list'>
    def statement_list(self, parent: SyNode):
        novo_no = SyNode(symbol=Producao.STATEMENT_LIST) 

        if (self.statement_list_linha(novo_no)):
            parent.add_children(novo_no)
            return True
            
        return False

    # <stmt-list'> -> <statement> <stmt-list'> | epsilon
    def statement_list_linha(self, parent: SyNode):
        novo_no = SyNode(symbol=Producao.STATEMENT_LIST_LINHA) 
        posicao_token_no_atual = self.posicao_token_atual

        if (self.statement(novo_no)):
            self.statement_list_linha(novo_no)
            parent.add_children(novo_no)
            return True
        
        self.posicao_token_atual = posicao_token_no_atual
        return False

    # <statement> -> <exp-stmt> | <compound-stmt> | <select-stmt> | <iter-stmt> | <return-stmt> 
    def statement(self, parent: SyNode):
        novo_no = SyNode(symbol=Producao.STATEMENT) 
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
        novo_no = SyNode(symbol=Producao.EXPRESSION_STMT) 
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
        novo_no = SyNode(symbol=Producao.SELECTION_STMT) 
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
        novo_no = SyNode(symbol=Producao.ITERATION_STMT) 

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
        novo_no = SyNode(symbol=Producao.RETURN_STMT) 

        if (self.match_terminal(parent=novo_no, expectedTokenTag="return")):
            if (self.match_terminal(parent=novo_no, expectedTokenTag="semicolon")):
                    parent.add_children(novo_no)
                    return True
            if (self.expression(novo_no)):
                if (self.match_terminal(parent=novo_no, expectedTokenTag="semicolon")):
                    parent.add_children(novo_no)
                    return True

        return False

    # <expression> -> <simple-exp> | <var> = <expression>
    def expression(self, parent: SyNode):
        novo_no = SyNode(symbol=Producao.EXPRESSION) 
        posicao_token_no_atual = self.posicao_token_atual

        if (self.simple_expression(novo_no)):
            parent.add_children(novo_no)
            return True

        self.posicao_token_atual = posicao_token_no_atual
        novo_no.children.clear()

        if (self.var(novo_no)):
            if (self.match_terminal(parent=novo_no, expectedTokenTag="eq")):
                if (self.expression(novo_no)):
                    parent.add_children(novo_no)
                    return True

        return False

    # <var> -> id [ <expression> ] | id ;
    def var(self, parent: SyNode):
        novo_no = SyNode(symbol=Producao.VAR) 

        if (self.match_terminal(parent=novo_no, expectedTokenTag="id")):
            posicao_token_no_atual = self.posicao_token_atual
            if (self.match_terminal(parent=novo_no, expectedTokenTag="open_square_brackets")):
                if (self.expression(novo_no)):
                    if (self.match_terminal(parent=novo_no, expectedTokenTag="close_square_brackets")):
                        parent.add_children(novo_no)
                        return True

                return False        
            self.posicao_token_atual = posicao_token_no_atual
            parent.add_children(novo_no)
            return True

        return False

    # <simple-expression> -> <additive-expression> <relop> <additive-expression> | <additive-expression>
    def simple_expression(self, parent: SyNode):
        novo_no = SyNode(symbol=Producao.SIMPLE_EXPRESSION) 

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
        novo_no = SyNode(symbol=Producao.RELOP) 

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
        novo_no = SyNode(symbol=Producao.ADDITIVE_EXPRESSION) 

        if (self.term(novo_no)):
            self.additive_expression_linha(novo_no)
            parent.add_children(novo_no)
            return True

        return False

    # <additive-expression> -> <addop> <additive-expression> | epsilon
    def additive_expression_linha(self, parent: SyNode):
        novo_no = SyNode(symbol=Producao.ADDITIVE_EXPRESSION_LINHA) 
        posicao_token_no_atual = self.posicao_token_atual

        if (self.addop(novo_no)):
            if (self.additive_expression(novo_no)):
                parent.add_children(novo_no)
                return True

        self.posicao_token_atual = posicao_token_no_atual
        return False

    # <addop> ->  + | - 
    def addop(self, parent: SyNode):
        novo_no = SyNode(symbol=Producao.ADDOP) 

        if (self.match_terminal(parent=novo_no, expectedTokenTag="plus")):
            parent.add_children(novo_no)
            return True

        if (self.match_terminal(parent=novo_no, expectedTokenTag="minus")):
            parent.add_children(novo_no)
            return True
        
        return False

    # <term> -> <factor> <term'>
    def term(self, parent: SyNode):
        novo_no = SyNode(symbol=Producao.TERM) 

        if (self.factor(novo_no)):
            self.term_linha(novo_no)
            parent.add_children(novo_no)
            return True

        return False

    # <term'> -> <mulop> <term> | epsilon
    def term_linha(self, parent: SyNode):
        novo_no = SyNode(symbol=Producao.TERM_LINHA) 
        posicao_token_no_atual = self.posicao_token_atual

        if (self.mulop(novo_no)):
            if (self.term(novo_no)):
                parent.add_children(novo_no)
                return True

        self.posicao_token_atual = posicao_token_no_atual
        return False

    # <mulop> ->  * | / 
    def mulop(self, parent: SyNode):
        novo_no = SyNode(symbol=Producao.MULOP) 

        if (self.match_terminal(parent=novo_no, expectedTokenTag="asterisk")):
            parent.add_children(novo_no)
            return True

        if (self.match_terminal(parent=novo_no, expectedTokenTag="slash")):
            parent.add_children(novo_no)
            return True
        
        return False

    # <factor> -> ( <expression> ) | <var> | <call> | num
    def factor(self, parent: SyNode):
        novo_no = SyNode(symbol=Producao.FACTOR) 
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
        novo_no = SyNode(symbol=Producao.CALL) 

        if (self.match_terminal(parent=novo_no, expectedTokenTag="id")):
            if (self.match_terminal(parent=novo_no,expectedTokenTag="open_parenthesis")):
                if (self.args(novo_no)):
                    if (self.match_terminal(parent=novo_no,expectedTokenTag="close_parenthesis")):
                        parent.add_children(novo_no)
                        return True
                            
        return False

    # <args> -> <arg-list> | epsilon
    def args(self, parent: SyNode):
        novo_no = SyNode(symbol=Producao.ARGS) 

        self.arg_list(novo_no)
        parent.add_children(novo_no)
        return True

    # <arg-list> -> <expression> <arg-list'>
    def arg_list(self, parent: SyNode):
        novo_no = SyNode(symbol=Producao.ARG_LIST) 

        if (self.expression(novo_no)):
            self.arg_list_linha(novo_no)
            parent.add_children(novo_no)
            return True

        return False

    # <arg-list'> -> , <arg-list> | epsilon
    def arg_list_linha(self, parent: SyNode):
        novo_no = SyNode(symbol=Producao.ARG_LIST_LINHA) 
        posicao_token_no_atual = self.posicao_token_atual

        if (self.match_terminal(parent=novo_no, expectedTokenTag="comma")):
            if (self.arg_list(novo_no)):
                parent.add_children(novo_no)
                return True
        
        self.posicao_token_atual = posicao_token_no_atual
        return False
                   

if __name__ == "__main__":
    parser = Parser()