from typing import *

class synode:
    
    '''
    Node of a syntatic tree
    '''

    def __init__(
        self,
        state : str,
        level : int
    ):
        
        self.state : str = state
        self.level : int = level
        self.parent : object = None
        self.children : List[ object ]

        self.derivation : int = -1
        self.exploration : int = 0
        self.failed : bool = True

    def add_children( self , state : str ):

        child = synode( state , self.level + 1 )
        child.parent = self
        self.children.append( child )
        
    def __str__( self ) -> str:
        pass

    def __hash__( self ) -> int:
        pass

    