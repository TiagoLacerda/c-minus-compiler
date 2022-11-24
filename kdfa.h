
typedef struct{

    unsigned int q0;   // Initial state, the token processing starts here
    int curr;          // Current state, if equals to -1 is trash  

    /*
    The value of curr can be anywhere in the interval [-1 , Q + F )
    */
    unsigned int Q;        // Number of normal states
    unsigned int F;        // Number of final states
    unsigned int n_states; // Always Q + F

    unsigned int n_tok;

    int * rules;

} KDFA;

typedef *KDFA KDFA_ptr;

KDFA_ptr init_KDFA(
    unsigned int q0,
    unsigned int Q,
    unsigned int F,
);

/* ##### Automaton information ###### */

int is_trash( KDFA_ptr M );

int is_final( KDFA_ptr M );

int get_pos( KDFA_ptr M , int state , int tok );

/* ##### Automaton manipulation ###### */

void reset_auto( KDFA_ptr M );

int add_rule( KDFA_ptr M , int old_st , int tok , int new_st );

int read_tok( KDFA_ptr M , int tok );

/* ##### Operation between automomatons*/