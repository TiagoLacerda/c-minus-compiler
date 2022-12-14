#ifndef STDIO_H
#define STDIO_H
#include <stdio.h>
#endif

#ifndef STDLIB_H
#define STDLIB_H
#include <stdlib.h>
#endif

extern FILE *yyin;
extern int yylex();
extern int yyparse();
extern int yylineno;
extern char *yytext;

void printTokenType(int code)
{
    if (code == 258)
        printf("PLUS");
    if (code == 259)
        printf("MINUS");
    if (code == 260)
        printf("ASTERISK");
    if (code == 261)
        printf("SLASH");
    if (code == 262)
        printf("LT");
    if (code == 263)
        printf("LE");
    if (code == 264)
        printf("GT");
    if (code == 265)
        printf("GE");
    if (code == 266)
        printf("EQ");
    if (code == 267)
        printf("NE");
    if (code == 268)
        printf("ASSIGN");
    if (code == 269)
        printf("SEMICOLON");
    if (code == 270)
        printf("COMMA");
    if (code == 271)
        printf("OPENPARENTHESIS");
    if (code == 272)
        printf("CLOSEPARENTHESIS");
    if (code == 273)
        printf("OPENSQUAREBRACKETS");
    if (code == 274)
        printf("CLOSESQUAREBRACKETS");
    if (code == 275)
        printf("OPENBRACKETS");
    if (code == 276)
        printf("CLOSEBRACKETS");
    if (code == 277)
        printf("ELSE");
    if (code == 278)
        printf("IF");
    if (code == 279)
        printf("INT");
    if (code == 280)
        printf("RETURN");
    if (code == 281)
        printf("VOID");
    if (code == 282)
        printf("WHILE");
    if (code == 283)
        printf("ID");
    if (code == 284)
        printf("NUM");
    if (code == 285)
        printf("ERROR");
}

int main(int argc, char **argv)
{
    yyin = fopen(argv[1], "r");
    // FILE *file = fopen(argv[1], "r");

    int token;
    token = yylex();
    while (token != 0)
    {
        printf("ln %d: %s - ", yylineno, yytext);
        printTokenType(token);
        printf("\n");
        token = yylex();
    }

    yyin = fopen(argv[1], "r");

    int status;
    status = yyparse();
    if (status == 0)
    {
        printf("OK!\n");
    }

    return 0;
}