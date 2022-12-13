#ifndef STDLIB_H
#define STDLIB_H
#include <stdlib.h>
#endif

#ifndef STDIO_H
#define STDIO_H
#include <stdio.h>
#endif

#ifndef GLOBALS_H
#define GLOBALS_H
#include "../globals.h"
#endif

extern int yylex();
extern int yylineno;
extern char *yytext;

void print(int code)
{
    if (code == PLUS) printf("PLUS");
    if (code == MINUS) printf("MINUS");
    if (code == ASTERISK) printf("ASTERISK");
    if (code == SLASH) printf("SLASH");
    if (code == LT) printf("LT");
    if (code == LE) printf("LE");
    if (code == GT) printf("GT");
    if (code == GE) printf("GE");
    if (code == EQ) printf("EQ");
    if (code == NE) printf("NE");
    if (code == ASSIGN) printf("ASSIGN");
    if (code == SEMICOLON) printf("SEMICOLON");
    if (code == COMMA) printf("COMMA");
    if (code == OPENPARENTHESIS) printf("OPENPARENTHESIS");
    if (code == CLOSEPARENTHESIS) printf("CLOSEPARENTHESIS");
    if (code == OPENSQUAREBRACKETS) printf("OPENSQUAREBRACKETS");
    if (code == CLOSESQUAREBRACKETS) printf("CLOSESQUAREBRACKETS");
    if (code == OPENBRACKETS) printf("OPENBRACKETS");
    if (code == CLOSEBRACKETS) printf("CLOSEBRACKETS");
    if (code == ELSE) printf("ELSE");
    if (code == IF) printf("IF");
    if (code == INT) printf("INT");
    if (code == RETURN) printf("RETURN");
    if (code == VOID) printf("VOID");
    if (code == WHILE) printf("WHILE");
    if (code == ID) printf("ID");
    if (code == NUM) printf("NUM");
    if (code == ERROR) printf("ERROR");
}

int main(void)
{
    int token;
    token = yylex();
    while (1)
    {
        printf("ln %d: %s - ", yylineno, yytext);
        print(token);
        printf("\n");
        token = yylex();
    }
    return 0;
}
