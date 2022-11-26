
from typing import *
import os.path
from token import Token

# Bliblioteca padrao de string
import string

class TokenListNode():

    # Metodo construtor da classe
    def __init__(
            self,
            token : Token = None,
            proximoNo = None,
            anteriorNo = None,
            posicao : int = 0

        ):

        self.token = token
        self.proximo = proximoNo
        self.anterior = anteriorNo
        self.posicao = posicao
    