%{
    #include<stdio.h>
    #include<stdlib.h>
    #include<string.h>
    #include<ctype.h>

    void yyerror(const char *s);
    int yylex();
    int yywrap();
%}

%token PLUS MINUS ASTERISK SLASH LT LE GT GE EQ NE ASSIGN SEMICOLON COMMA OPENPARENTHESIS CLOSEPARENTHESIS OPENSQUAREBRACKETS CLOSESQUAREBRACKETS OPENBRACKETS CLOSEBRACKETS ELSE IF INT RETURN VOID WHILE ID NUM ERROR

%%

program: declarationlist
;

declarationlist: declaration declarationlistlinha
;

declarationlistlinha: declarationlist
| 
;

declaration: vardeclaration 
| fundeclaration
;

vardeclaration: typespecifier ID vardeclarationlinha
;
vardeclarationlinha: SEMICOLON 
| OPENSQUAREBRACKETS NUM CLOSESQUAREBRACKETS SEMICOLON
;

typespecifier: INT 
| VOID
;

fundeclaration: typespecifier ID OPENPARENTHESIS params CLOSEPARENTHESIS compoundstmt
;

params: paramlist 
| VOID
;

paramlist: param paramlistlinha
;

paramlistlinha: COMMA param paramlistlinha
| 
;

param: typespecifier ID paramlinha
;

paramlinha: OPENSQUAREBRACKETS CLOSESQUAREBRACKETS
| 
;

compoundstmt: OPENBRACKETS localdeclarations statementlist CLOSEBRACKETS
;

localdeclarations: vardeclaration localdeclarationslinha
| 
;

localdeclarationslinha: localdeclarations 
;

statementlist: statement statementlistlinha
| 
;

statementlistlinha: statementlist
;

statement: expressionstmt 
| compoundstmt 
| selectionstmt 
| iterationstmt 
| returnstmt
;

expressionstmt: expression SEMICOLON 
| SEMICOLON
;

selectionstmt: IF OPENPARENTHESIS expression CLOSEPARENTHESIS statement selectionstmtlinha
;

selectionstmtlinha: ELSE statement
| 
;

iterationstmt: WHILE OPENPARENTHESIS expression CLOSEPARENTHESIS statement
;

returnstmt: RETURN expressionstmt
;

expression: var ASSIGN expression 
| simpleexpression
;

var : ID varlinha
;

varlinha: OPENSQUAREBRACKETS expression CLOSESQUAREBRACKETS
| 
;

simpleexpression: additiveexpression simpleexpressionlinha
;

simpleexpressionlinha: relop additiveexpression 
| 
;

relop: LE 
| LT 
| GT 
| GE 
| EQ 
| NE
;

additiveexpression: term additiveexpressionlinha
;

additiveexpressionlinha: addop additiveexpression
| 
;

addop: PLUS 
| MINUS
;

term: factor termlinha
;

termlinha: mulop term
| 
;

mulop: ASTERISK 
| SLASH
;

factor: OPENPARENTHESIS expression CLOSEPARENTHESIS 
| var 
| call 
| NUM
;

call: ID OPENPARENTHESIS args CLOSEPARENTHESIS
;

args: arglist 
| 
;

arglist: expression arglistlinha
;

arglistlinha: COMMA arglist
| 
;

%%

void yyerror(const char* msg) {
    fprintf(stderr, "%s\n", msg);
}