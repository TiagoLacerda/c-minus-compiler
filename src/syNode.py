from typing import *

from token import Token
from enumProducoes import Producao

class SyNode:
    
    '''
    Node of a syntatic tree
    '''

    def __init__(
        self,
        symbol : Producao,
        token : Token = None,
        parent = None,
        level = 0
    ):
        
        '''
        Creates a node of a syntatic tree.

        Arguments:
        state: one symbol of its grammar, either a state or a terminal
        level: the depth of the node on the tree
        '''

        self.symbol = symbol
        self.token = token
        self.level = level
        self.parent = parent
        self.children = list()

    def add_children( self , child ):
        self.children.append( child )
    
    #------------------------------------------------------------
    # Boi this is going to be a nervous wreck to code
    def __str__( self ) -> str:
        
        nodes = [ self ]
        explored = [ -1 ]

        s = ""
        while nodes:

            node = nodes[ -1 ]
            if explored[ -1 ] == -1:
                indent = ( node.level - self.level )*"| "
                if (node.symbol == None):
                    s = s + f"{indent}{node.token.tags[0]}\n"
                else:
                    s = s + f"{indent}{node.symbol.name}\n"
                explored[ -1 ] = 0

            if explored[ -1 ] >= len( node.children ):
                nodes.pop()
                explored.pop()

            else:
                child = node.children[ explored[ -1 ] ]
                nodes.append( child )
                explored[ -1 ] += 1
                explored.append( -1 )
        return s

    def __hash__( self ) -> int:
        pass

    
