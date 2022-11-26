
from typing import *
import os.path
from token import Token
from tokenListNode import TokenListNode

# Bliblioteca padrao de string
import string

class TokenList():

    # Metodo construtor da classe
    def __init__(
            self,
            cabeca = None,
            ponteiro = None

        ):

        self.cabeca = cabeca
        self.ponteiro = ponteiro

    def insert(lista, token : Token):
        # 1) Cria um novo nodo com o dado a ser armazenado.
        novo_no = TokenListNode(token)

        # 3) Faz com que a cabeça da lista referencie o novo nodo.
        lista.cabeca = novo_no
        lista.ponteiro = novo_no

    def append(lista, token : Token, indice : int):

        # Cria um novo nodo com o dado desejado.
        novo_no = TokenListNode(token)

        novo_no.posicao = indice
        
        novo_no.anterior = lista.ponteiro

        novo_no.anterior.proximo = novo_no

        lista.ponteiro = novo_no

    def next_node(lista):

        lista.ponteiro = lista.ponteiro.proximo


    def insert_all_tokens(lista, listaTokens : List ):

        i = 0
        for item in listaTokens:
            if item == listaTokens[0]:
                lista.insert(item)
            else:
                lista.append(item, indice=i)
            i += 1

    def next_position_node(lista, posicao: int):

        while( lista.ponteiro.posicao != posicao):
            lista.next_node()
