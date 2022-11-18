from typing import *
import json
from collections import deque
from copy import deepcopy

from syntree import synode

state_set  = Set[ str ]
state_seq  = List[ str ]
transition = Dict[ str , List[ state_seq ] ]

EPSILON = '\u03B5'

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

        #---------------------------------------------------
        # Checking for left_recursion. ie if there any derivation
        # like A :: A B | A a, where a is terminal and A and B are
        # states
        self.left_recursion = False
        for state in states:
            for rule in derivations[ state ]:
                if rule[ 0 ] == state:
                    self.left_recursion = True
                    break

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
            return CFG.from_json( f.read() )
    
    def __str__( self ) -> str:
        
        name = "unknown" if self.name is None else self.name
        name_header  : str = f"name = {name}" 

        state_list = list( self.states )
        state_list.sort()
        state_header : str = "states: [" + " , ".join( state_list ) + "]"

        termn_list = list( self.terminals )
        termn_list.sort()
        termn_header : str = "terminals: [" + " , ".join( termn_list ) + "]"

        transition_str : str = "rules:\n"
        states : Deque[ str ] = deque( [ self.root ] )
        visited : state_set = { self.root } 

        while states:  # while there are elements in the queue

            #-------------------------------------------------
            # fetching next state and transitions
            state = states.popleft()
            transitions = self.derivations[ state ]

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
                    c : bool = st == EPSILON # Ah yes, epsilon is the empty state. 
                    if not ( a or b or c ):
                        states.append( st )
                        visited.add( st )
        
        return f"{name_header}\n{state_header}\n{termn_header}\n{transition_str}"

    ######## PARSING #########

    def build_syntree( self , tok_seq : List[ str ] ):

        node : object = synode( self.root , 0 )
        root = node
        node_swp = True
        while True:
            
            # if node_swp:
                # print( root )
            node_swp = False

            if node.symbol == EPSILON:
                node.status = synode.SUCCESS

            is_root : bool = node.symbol == self.root
            is_leaf : bool = node.symbol in self.terminals
            is_expl : bool = node.status == synode.EXPLORING
            is_succ : bool = node.status == synode.SUCCESS
            is_fail : bool = node.status == synode.FAIL
            is_dead : bool = node.status == synode.DEAD
            

            #------------------------------------------------------
            # Here the derivation is fineshed. You either have a
            # correct tree or sequence is not syntatically correct
            if is_root and ( is_dead or is_succ ):
                return node
            
            #-----------------------------------------------------
            # If the node is dead, it means that there are no deri
            # vations remaining to try. So the parent failed its c
            # urrent derivation and try the next one. This logic is
            # repeated upstream untill a node with at least one deri
            # vation remainig is found.
            if is_dead:
                node_swp = True
                node = node.parent
                node.derivation += 1
                node.status = synode.FAIL
                continue
            
            #---------------------------------------------------
            # A node is succesfull if is a leaf node and its symbol
            # matches its correspondent token or when its non leaf
            # and all of its children are succesfull. In both cases
            # must return to the parent, update the last matched token
            # and explore the next child.
            if is_succ:
                parent = node.parent
                parent.last_match = node.last_match
                parent.to_explore += 1
                node = parent
                continue
            
            #----------------------------------------------------
            # internal node in exploration mode. 3 subcases.
            if is_expl and not( is_leaf ):
                
                #-----------------------------------------------
                # Here the node was not even initialized. So the
                # first derivation is loaded on its children.
                if len( node.children ) == 0:
                    symbol : str = node.symbol
                    tokens : state_seq = self.derivations[ symbol ][ 0 ]
                    for tok in tokens:
                        node.add_children( tok )
                    node_swp = True
                
                #-----------------------------------------------
                # The node already explored all of its children
                # on the current derivation. Meaning it is correct
                if node.to_explore >= len( node.children ):
                    node.status = synode.SUCCESS
                
                #------------------------------------------------
                # The last child of the current derivation was correct
                # now time to explore the next one.
                else:
                    child = node.children[ node.to_explore ]
                    child.last_match = node.last_match
                    node = child
                continue
            
            #-------------------------------------------------------
            # A leaf node in exploration mode only checks if its symbol
            # matches the corresponding token. Case positive, it is sucesse
            # ful, else is already dead.
            if is_expl:
                try:
                    tok : str = tok_seq[ node.last_match + 1 ]
                    if node.symbol == tok:
                        node.status = synode.SUCCESS
                        node.last_match += 1
                    else:
                        node.status = synode.DEAD
                except IndexError:
                    node.status = synode.DEAD
                continue
            
            #--------------------------------------------------------------
            # My homeboy has failed, noooooooooooo.
            # Jokes apart, it should try the next derivation, if there is one
            # , and revert back to exploration mode. However, if there is no
            # more derivations, the node is dead
            if is_fail and not( is_leaf ):
                symbol : str = node.symbol
                rules = self.derivations[ symbol ]
                if node.derivation < len( rules ): # there are new derivations to try
                    tokens = rules[ node.derivation ]
                    node.children.clear()
                    node.to_explore = 0
                    for tok in tokens:
                        node.add_children( tok )
                    node.status = synode.EXPLORING
                    node_swp = True
                else:
                    node.status = synode.DEAD
        pass

    def remove_leftr( self ):

        '''
        Re edits the grammar rules in order to remove left recursions.
        This is necessary in order to guarantee that the top down parsing
        of a token list wont enter in an infinite loop

        for example:
        
        >>> print( G )
        states = [ A , B ]
        terminals = [ a , b , c , d ]

        A :: B a | A a | c
        B :: B b | A b | d

        >>> G.remove_leftr()
        >>> print( G )
        
        states = [ A , B , A* , B* ]
        terminals = [ a , b , c , d ]

        A :: B a A* | c A*
        B :: c A* b B* | d B*
        A* :: a A* | None 
        B* :: b B* | a A* b B* | None
        '''

        if not self.left_recursion:
            return
        
        #-------------------------------------------------------
        # Sorting states based on number of possible derivations
        state_lst : state_seq = list( self.states )
        foo : Callable = lambda x : len( self.derivations[ x ] )
        state_lst.sort( key = foo )

        #--------------------------------------------------------
        # New ruleset
        rules_dict : Dict[ str , List[ state_seq ] ] = deepcopy( self.derivations )
        new_states : state_set = set()
        
        n : int = len( state_lst )
        for i in range( n ):

            Si : str = state_lst[ i ]
            rules : List[ state_seq ] = rules_dict[ Si ]

            j : int = 0
            while j <= i:

                if j == i:
                    #-------------------------------------------------------------
                    # Replace any rule in the grammar with the format:
                    # A :: A a | b
                    #
                    # By the new rules
                    # A :: b A*
                    # A* :: a A* | None
                    #
                    # Where b and a are sequences of symbols ( states and terminals )
                    # that do not begin with the state A

                    a_seqs : List[ state_lst ] = []
                    b_seqs : List[ state_lst ] = []
                    for rule in rules:
                        if rule[ 0 ] == Si:
                            a_seqs.append( rule[ 1: ] )
                        else:
                            b_seqs.append( rule )
                    
                    #------------------------------------------------------------
                    # no imediate recursion
                    if not a_seqs:
                        j += 1
                        continue
                    
                    #------------------------------------------------------------
                    # All imediate recursions. No Idea on what to do
                    if not b_seqs:
                        pass
                    
                    new_states.add( Si + "*" )
                    rules_dict[ Si ] = []
                    for b_rule in b_seqs:
                        rules_dict[ Si ].append( b_rule + [ Si + "*" ] )

                    rules_dict[ Si + "*" ] = []
                    for a_rule in a_seqs:
                        rules_dict[ Si + "*" ].append( a_rule + [ Si + "*" ] )
                    rules_dict[ Si + "*" ].append( [EPSILON] )

                else:
                    Sj = state_lst[ j ]

                    #-----------------------------------------------------------
                    # Replace any rule with the format.
                    # Si :: Sj b
                    #
                    # by, for every a where Sj :: a:
                    # Si :: a b
                    
                    bs : List[ state_seq ] = []
                    for rule in rules:
                        if rule[ 0 ] == Sj and len( rule ) > 1:
                            rules.remove( rule )
                            bs.append( rule[ 1: ] )
                    
                    if not bs:
                        j += 1
                        continue
                        
                    for b in bs:
                        for a in rules_dict[ Sj ]:
                            rules.append( a + b )
                j += 1

        self.left_recursion = False
        self.derivations = rules_dict
        self.states = self.states | new_states

    def parse( self , tok_seq : List[ str ] , verbose : bool = False ) -> bool:
        
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
        
        #-----------------------------------------------------
        # left recursions must be removed for efficient and
        # reliable top down parsing
        if self.left_recursion:
            self.remove_leftr()
        
        tree : object = self.build_syntree( tok_seq )
        result = tree.status == synode.SUCCESS
        if result and verbose:
            print( tree )

        return result
        

if __name__ == "__main__":

    G = CFG.from_file( "boolform.json" )

    sep = "-"*20
    print( f"before{sep}\n\n{G}\n")
    G.remove_leftr()
    print( f"after{sep}\n\n{G}\n")

    test = "~ ( id + id ) = id".split()
    print( f"test tokens: {test}")

    tree = G.build_syntree( test )
    print( f"\nresulting syntree:\n{tree}")
    print( tree.status == synode.SUCCESS)
    
