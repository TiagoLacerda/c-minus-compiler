from typing import *

state_set  = Set[ str ]
state_seq  = List[ str ]
transition = Dict[ str , List[ state_seq ] ]

class CFG:

    ''' Context Free Grammar'''

    def __init__(
        self,
        root : str,
        states : state_set,
        terminals : state_set,
        derivations : transition
    ):
        """
        Creates a Context Free Grammar.

        Keyword arguments:
        root: first state in all derivation
        states: a finite set of non terminal states.
        terminals: states that terminate a derivation sequence
        derivations: derivation rules of the grammar
        """

        #-----------------------------------------------
        # root must be a state
        if root not in states:
            raise ValueError (f"root value \'{root}\' is not in the given state set")

        #-----------------------------------------------
        # terminals must must be a disjoint set from states
        if not terminals.isdisjoint( states ):
            joint_states : state_set = terminals.intersection( states )
            seq : str = " ".join( joint_states )
            raise ValueError (f"states {seq} are both terminal and non terminal")
        
        #-----------------------------------------------
        # All non terminals must have at least one derivation rule
        no_derivation : state_set = states - set( derivations.keys() )
        if len( no_derivation ) != 0:
            seq : str = " ".join( no_derivation )
            raise ValueError (f"states {seq} have no known derivations")

        #-----------------------------------------------
        # Terminal states must have no derivations
        term_dev : state_set = terminals.intersection( set( derivations.keys() ) )
        if len( term_dev ) != 0:
            seq : str = " ".join( term_dev )
            raise ValueError (f"terminals {seq} must have no derivations")

        self.root = root
        self.states = states
        self.terminals = terminals
        self.derivations = derivations