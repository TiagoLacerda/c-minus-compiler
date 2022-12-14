%option yylineno

%{
#ifndef CMINUS_TAB_H
#define CMINUS_TAB_H
#include "cminus.tab.h"
#endif
%}

letter        [a-zA-Z]
digit         [0-9]
num           {digit}+
id            {letter}+

whitespace    [ \t]+

comment       \/\*.\*\/

%%

"+"           {return PLUS;}
"-"           {return MINUS;}
"*"           {return ASTERISK;}
"/"           {return SLASH;}
"<"           {return LT;}
"<="          {return LE;}
">"           {return GT;}
">="          {return GE;}
"=="          {return EQ;}
"!="          {return NE;}
"="           {return ASSIGN;}
";"           {return SEMICOLON;}
","           {return COMMA;}
"("           {return OPENPARENTHESIS;}
")"           {return CLOSEPARENTHESIS;}
"["           {return OPENSQUAREBRACKETS;}
"]"           {return CLOSESQUAREBRACKETS;}
"{"           {return OPENBRACKETS;}
"}"           {return CLOSEBRACKETS;}
else          {return ELSE;}
if            {return IF;}
int           {return INT;}
return        {return RETURN;}
void          {return VOID;}
while         {return WHILE;}
{id}          {return ID;}
{num}         {return NUM;}
{whitespace}  {/* skip whitespace */}
"/*"          { char c1;
                char c2;
                c1 = 0;
                do
                { c2 = input();
                  if (c2 == EOF) break;
                  if ((c1 == '*') && (c2 == '/')) break;
                  c1 = c2;
                } while (1);
              }
.             {return ERROR;}

%%

int yywrap(void)
{
    return 1;
}