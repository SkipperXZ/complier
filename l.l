%option noyywrap
D			[0-9]
L			[a-zA-Z_]
H			[a-fA-F0-9]
E			([Ee][+-]?{D}+)
P                       		([Pp][+-]?{D}+)
FS			(f|F|l|L)
IS                      		((u|U)|(u|U)?(l|L|ll|LL)|(l|L|ll|LL)(u|U))

%{
#include <stdio.h>
#include "y.tab.h"

void count(void);
%}

%%
"/*"			{ comment(); }
"//"[^\n]*              		{ /* consume //-comment */ }

"break"			{  printf("[%d] %s   ",BREAK,yytext);return(BREAK); }
"else"			{  printf("[%d] %s   ",ELSE,yytext);return(ELSE); }
"for"			{  printf("[%d] %s   ",FOR,yytext);return(FOR); }
"if"			{  printf("[%d] %s   ",IF,yytext);return(IF); }
"int64"			{ printf("[%d] %s   ",INT64,yytext); return(INT64); }

{L}({L}|{D})*		{ printf("[%d] %s   ",check_type(),yytext); return(check_type()); }

0[xX]{H}+{IS}?		{ printf("[%d] %s   ",CONST,yytext); return(CONST); }
0[0-7]*{IS}?		{ printf("[%d] %s   ",CONST,yytext); return(CONST); }
[1-9]{D}*{IS}?		{ printf("[%d] %s   ",CONST,yytext); return(CONST); }
L?'(\\.|[^\\'\n])+'	{ printf("[%d] %s   ",CONST,yytext); return(CONST); }

{D}+{E}{FS}?		{ printf("[%d] %s   ",CONST,yytext); return(CONST); }
{D}*"."{D}+{E}?{FS}?	{ printf("[%d] %s   ",CONST,yytext); return(CONST); }
{D}+"."{D}*{E}?{FS}?	{ printf("[%d] %s   ",CONST,yytext); return(CONST); }
0[xX]{H}+{P}{FS}?	{ printf("[%d] %s   ",CONST,yytext); return(CONST); }
0[xX]{H}*"."{H}+{P}{FS}?     { printf("[%d] %s   ",CONST,yytext); return(CONST); }
0[xX]{H}+"."{H}*{P}{FS}?     { printf("[%d] %s   ",CONST,yytext); return(CONST); }

"=="			{ printf("[%d] %s   ",EQ_OP,yytext); return(EQ_OP); }
"!="			{ printf("[%d] %s   ",NE_OP,yytext); return(NE_OP); }
";"			{ printf("[%d] %s   ",';',yytext); return(';'); }
("{"|"<%")			{ printf("[%d] %s   ",'{',yytext); return('{'); }
("}"|"%>")			{ printf("[%d] %s   ",'}',yytext); return('}'); }
","			{ printf("[%d] %s   ",',',yytext); return(','); }
"="			{ printf("[%d] %s   ",'=',yytext); return('='); }
"("			{ printf("[%d] %s   ",'(',yytext); return('('); }
")"			{ printf("[%d] %s   ",')',yytext); return(')'); }
("["|"<:")			{ printf("[%d] %s   ",BREAK,yytext); return('['); }
("]"|":>")			{ printf("[%d] %s   ",BREAK,yytext); return(']'); }
"-"			{ printf("[%d] %s   ",'-',yytext); return('-'); }
"+"			{ printf("[%d] %s   ",'+',yytext);return('+'); }
"*"			{ printf("[%d] %s   ",'*',yytext); return('*'); }
"/"			{ printf("[%d] %s   ",'/',yytext); return('/'); }
"%"			{ printf("[%d] %s   ",'%',yytext); return('%'); }
"<"			{ printf("[%d] %s   ",'<',yytext); return('<'); }
">"			{ printf("[%d] %s   ",'>',yytext); return('>'); }

[ \t\v\n\f]		{ count(); }
.			{ /* Add code to complain about unmatched characters */ }

%%

/*int yywrap(void)
{
	return 1;
}*/


void comment(void)
{
	char c, prev = 0;
  
	while ((c = input()) != 0)      /* (EOF maps to 0) */
	{
		if (c == '/' && prev == '*')
			return;
		prev = c;
	}
	//error("unterminated comment");
}


int column = 0;

void count(void)
{
	int i;

	for (i = 0; yytext[i] != '\0'; i++)
		if (yytext[i] == '\n')
			column = 0;
		else if (yytext[i] == '\t')
			column += 8 - (column % 8);
		else
			column++;

	ECHO;
}


int check_type(void)
{
/*
* pseudo code --- this is what it should check
*
*	if (yytext == type_name)
*		return TYPE_NAME;
*
*	return IDENTIFIER;
*/

/*
*	it actually will only return IDENTIFIER
*/

	return IDENTIFIER;
}
int main(int argc,char **argv)
{
   yyin = fopen(argv[1], "r");
   if(yyparse()){
	   printf("\ncomplie failed\n");
   }else
		printf("\n complie successful \n");
}