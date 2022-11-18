from typing import *

class synode:
    
    '''
    Node of a syntatic tree
    '''
    EXPLORING = 0 # Checking if cureent derivation is the correct one
    SUCCESS   = 1 # Current derivation is indeed correct
    FAIL      = 2 # Current derivation failed, try next one
    DEAD      = 3 # No more derivations to try, fails parent node

    def __init__(
        self,
        symbol : str,
        level : int
    ):
        
        '''
        Creates a node of a syntatic tree.

        Arguments:
        state: one symbol of its grammar, either a state or a terminal
        level: the depth of the node on the tree
        '''

        self.symbol : str = symbol
        self.level : int = level
        self.parent : object = None
        self.children : List[ object ] = list()

        self.derivation  : int = 0 # Current derivation being evaluated
        self.to_explore  : int = 0 # Next Symbol of current derivation to be explored
        self.status      : int = synode.EXPLORING

        #---------------------------------------------------------
        # index of the last token matched by the tree with root in
        # self
        self.last_match  : int = -1

    def add_children( self , state : str ):

        child = synode( state , self.level + 1 )
        child.parent = self
        child.last_match = self.last_match
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
                s = s + f"{indent}{node.symbol}\n"
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

    
