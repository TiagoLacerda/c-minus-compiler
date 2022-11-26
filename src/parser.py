from typing import *
import sys
import os.path
from token import Token
from tokenList import TokenList
from tokenListNode import TokenListNode

# Bliblioteca padrao de string
import string

# Biblioteca para juncao de tipos iteraveis - nesse caso juncao de dict
from itertools import chain

arquivo_entrada = "output/example.json"

# Verifica se o arquivo de entrada existe no diretorio
if not os.path.exists(arquivo_entrada):
    print("Arquivo de entrada não existe")

# Abre o arquivo de entrada (resposta do analisador lexico)
f = open(arquivo_entrada, "r")
entrada = Token.from_json( f.read() )
f.close()

lista_tokens = TokenList()
lista_tokens.insert_all_tokens(entrada)
lista_tokens.ponteiro = lista_tokens.cabeca

# Declarando Classe do Analisador Sintatico
class AnalisadorSintatico():

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

    def reset_posicao_ponteiro(self):
        self.posicao_token_atual = lista_tokens.ponteiro.posicao
        self.tem_erro_sintatico = False
        self.erro_sintatico = ""

    def match(self, expectedTokenTag: str):
        if((self.posicao_token_atual>=len(self.entrada)) or (lista_tokens.ponteiro.posicao >= len(self.entrada))):
            return False
        elif(self.entrada[self.posicao_token_atual].tags[0]==expectedTokenTag):
            return True
        else:
            return False

    def erro(self, expectedToken: str):
        self.erro_sintatico = "Erro sintatico - Esperado " + expectedToken + " - linha: " + self.entrada[self.posicao_token_atual].line + " , coluna: " + self.entrada[self.posicao_token_atual].column + "\n" + " Token problemático: " + lista_tokens.ponteiro.token.value + "\n"
        self.tem_erro_sintatico = True
        print(self.erro_sintatico)
        return

    def parse(self):

        if(self.program()):
            if(lista_tokens.ponteiro.proximo == None):
                print("Cadeia é aceita")
            else:
                print("Cadeia não é aceita")
            
        else:
            print("Cadeia não é aceita")

    # <program> -> <declaration-list>
    def program(self):

        if(self.declaration_list()):
            return True
        else:
            return False

    # <declaration-list> -> <declaration> <declaration-list'>
    def declaration_list(self):
        
        if (self.declaration()):
            if (self.declaration_list_linha()):
                return True
            else:
                return False
        else:
            return False

    # <declaration> -> <var-declaration> | <fun-declaration>
    def declaration(self):

        if (self.var_declaration()):
            return True
        elif (self.fun_declaration()):
            return True
        else:
            return False

    # <declaration-list'> -> <declaration-list'> | epsilon
    def declaration_list_linha(self):

        if (self.declaration_list()):
            return True
        else:
            return True

    # <var-declaration> -> <type-spec> id <var-declaration'>
    def var_declaration(self):

        if (self.type_spec()):
            if (self.match(expectedTokenTag="id")):
                self.next_token()
                if (self.var_declaration_linha()):
                    lista_tokens.next_position_node(self.posicao_token_atual)
                    return True
                else:
                    self.reset_posicao_ponteiro()
                    return False
            else:
                self.erro(expectedToken=" identificador ")
                self.reset_posicao_ponteiro()
                return False
        else:
            return False

    # <var-declaration'> -> [ num ] ; | ;
    def var_declaration_linha(self):

        if (self.match(expectedTokenTag="open_square_brackets")):
            self.next_token()
            if (self.match(expectedTokenTag="num")):
                self.next_token()
                if (self.match(expectedTokenTag="close_square_brackets")):
                    self.next_token()
                    if (self.match(expectedTokenTag="semicolon")):
                        self.next_token()
                        return True
                    else:
                        self.erro(expectedToken=" ';' ")
                        return False
                else:
                    self.erro(expectedToken=" ']' ")
                    return False
            else:
                self.erro(expectedToken=" numero ")
                return False
        elif (self.match(expectedTokenTag="semicolon")):
            self.next_token()
            return True
        else:
            self.erro(expectedToken=" tokens ';' ou '[' ")
            return False
    

    # <type-spec> -> int | void
    def type_spec(self):

        if (self.match(expectedTokenTag="int")):
            self.next_token()
            return True
        if (self.match(expectedTokenTag="void")):
            self.next_token()
            return True
        else:
            self.erro(expectedToken=" tipos 'int' ou 'void' ")
            return False


    # <fun-declaration> -> <type-spec> id ( <params> ) <compound-stmt> 
    def fun_declaration(self):

        if (self.type_spec()):
            if (self.match(expectedTokenTag="id")):
                self.next_token()
                if (self.match(expectedTokenTag="open_parenthesis")):
                    self.next_token()
                    if (self.params()):
                        if (self.match(expectedTokenTag="close_parenthesis")):
                            self.next_token()
                            if (self.compound_stmt()):
                                lista_tokens.next_position_node(self.posicao_token_atual)
                                return True
                            else:
                                self.reset_posicao_ponteiro()
                                return False
                        else:
                            self.erro(expectedToken=" ')' ")
                            self.reset_posicao_ponteiro()
                            return False
                    else:
                        self.reset_posicao_ponteiro()
                        return False
                else:
                    self.erro(expectedToken=" '(' ")
                    self.reset_posicao_ponteiro()
                    return False
            else:
                self.erro(expectedToken=" identificador ")
                self.reset_posicao_ponteiro()
                return False
        else:
            return False

    # <params> -> <param-list> | void
    def params(self):

        if (self.params_list()):
            return True
        elif (self.match(expectedTokenTag="void")):
            self.next_token()
            return True
        else:
            self.erro(expectedToken=" 'void' ")
            return False

    # <param-list> -> <param> <param-list'>
    def param_list(self):

        if (self.param()):
            if (self.param_list_linha):
                return True
            else:
                return False
        else:
            return False

    # <param> -> <type-spec> id [] | <type-spec> id
    def param(self):

        if (self.type_spec()):
            if (self.match(expectedTokenTag="id")):
                self.next_token()
                if (self.match(expectedTokenTag="open_square_brackets")):
                    self.next_token()
                    if (self.match(expectedTokenTag="close_square_brackets")):
                        self.next_token()
                    else:
                        self.erro(expectedToken=" ']' ")
                        return False
                else:
                    return True
            else:
                self.erro(expectedToken=" identificador ")
                return False
        else:
            return False

    # <param-list'> -> , <param> <param-list'> | epsilon
    def param_list_linha(self):

        if (self.match(expectedTokenTag="comma")):
            self.next_token()
            if (self.param()):
                if (self.param_list_linha):
                    return True
                else:
                    return False
            else:
                return False
        else:
            return True