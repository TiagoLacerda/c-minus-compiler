from typing import *
import json
from collections import deque

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
        derivations : transition,

        name : str = None
    ):
        """
        Creates a Context Free Grammar.

        Mandatory arguments:
        root: first state in any derivation sequence
        states: a finite set of non terminal states.
        terminals: states that terminate a derivation sequence
        derivations: derivation rules of the grammar

        Optional arguments:
        name: name of the language that uses this grammar
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
        self.name = name

    ######## DATA REPRESENTATION #########
    def to_dict( self ) -> Dict[ str , Any ]:

        '''
        Returns an equivalent to this class instance as a <dict>.
        '''

        d =  {
            'root' : self.root,
            'states' : list( self.states ),
            'terminals' : list( self.terminals ),
            'derivations' : self.derivations
        }

        if not( self.name is None ):
            d[ 'name' ] = self.name

        return d 

    @staticmethod
    def from_dict( data : Dict[ str , Any ] ):

        """
        Returns a class instance from an equivalent <dict>.
        """

        return CFG(
            data[ 'root' ],
            set( data[ 'states' ] ),
            set( data[ 'terminals' ] ),
            data[ 'derivations' ],

            name = data.get("name",None)
        )

    def to_json(self):
        """
        Returns an equivalent to this class instance as a json <str>.
        """
        return json.dumps(self.to_dict())

    @staticmethod
    def from_json(data: str):
        """
        Returns a class instance from an equivalent json <str>.
        """
        return CFG.from_dict(json.loads(data))
    
    def to_file( self , folder : str = None ):
        
        """
        Saves object locally in json format
        """

        #------------------------------------------------------
        # Grammar must have a name, for the file.
        if self.name is None:
            raise ValueError( "If this grammar was a horse America would make song about it, because it has no name" )
        
        if folder is None:
            path = f"{self.name}cfg.json"
        else:
            path = f"./{folder}/{self.name}cfg.json"
        
        with open( path , "w" ) as f:
            f.write( self.to_json() )
    
    @staticmethod
    def from_file( filename ):
        with open( filename , "r" ) as f:
            return CFG.from_json( f.readline() )
    
    def __str__( self ) -> str:
        
        name = "unknown" if self.name is None else self.name
        name_header  : str = f"name = {name}" 
        state_header : str = "states = " + " ".join( self.states )
        termn_header : str = "terminals = " + " ".join( self.terminals )

        transition_str : str = ""
        states : Deque[ str ] = deque( [ self.root ] )
        visited : state_set = set() 

        while states:  # while there are elements in the queue

            #-------------------------------------------------
            # fetching next state and transitions
            state = states.popleft()
            transitions = self.derivations[ state ]
            visited.add( state )

            #------------------------------------------------
            # updating transition strings 
            slst = []
            for tr in transitions:
                if len( tr ) == 1:
                    slst.append( tr[ 0 ] )
                else:
                    slst.append(
                        " ".join( tr )
                    )
            transition_str += state + " :: " + " | ".join( slst ) + "\n"

            #--------------------------------------------------
            # updating the queue
            for tr in transitions:
                for st in tr:
                    a : bool = st in visited
                    b : bool = st in self.terminals
                    if not ( a or b ):
                        states.append( st )
        
        return f"{name_header}\n\n{state_header}\n{termn_header}\n\n{transition_str}"

    ######## PARSING #########

    def parse( self , tok_seq : List[ str ] ) -> bool:
        
        '''
        Checks if tok_seq represents a valid sentence, according
        to the rules of the grammar. Uses the recursive descent
        algorithm.
        '''
        
        result : bool

        #-----------------------------------------------------
        # If any of the tokens are foreign to the terminals,
        # then there is no need to make a parse tree: the se-
        # quence is invalid.
        if any( tok not in self.terminals for tok in tok_seq ):
            return False
        
        return result
        

if __name__ == "__main__":


    f = open( 'tinycfg.json' , 'r')
    G = CFG.from_json( f.read() )
    f.close()
    print( G ) 