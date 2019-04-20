%token IDENTIFIER STRING_LITERAL
%token LE_OP GE_OP EQ_OP NE_OP
%token INT64 CONST ARRAY
%token IF ELSE WHILE DO FOR BREAK 

%start startfromhere
%%

primary_expression
	: IDENTIFIER
	| CONST
	| STRING_LITERAL
	;
unary_operator
	: '-'
	| '+'
	;
cast_expression
	: unary_operator primary_expression
	| primary_expression
	;
multiplicative_expression
	: cast_expression
	| multiplicative_expression '*' cast_expression
	| multiplicative_expression '/' cast_expression
	| multiplicative_expression '%' cast_expression
	;
additive_expression
	: multiplicative_expression
	| additive_expression '+' multiplicative_expression
	| additive_expression '-' multiplicative_expression
	;
relational_expression
	: additive_expression
	| relational_expression '<' additive_expression
	| relational_expression '>' additive_expression
	;
equality_expression
	: relational_expression 
	| equality_expression EQ_OP relational_expression
	| equality_expression NE_OP relational_expression
	;
expression
	: relational_expression
	;
expression_statement
	: expression ';'
	| ';'
	;
direct_declarator
	: IDENTIFIER
	| expression_statement
	;
declaration
	: declaration_constant IDENTIFIER cast_expression ';'
	| declaration_specifiers IDENTIFIER ';'
	| declaration_specifiers IDENTIFIER '=' cast_expression ';'
	;

declaration_specifiers 
	: INT64	
	;
declaration_constant
	: CONST
	;
startfromhere
	: declaration
	| direct_declarator
	| startfromhere declaration
	| startfromhere direct_declarator
	;
%%
#include <stdio.h>

extern char yytext[];
extern int column;

yyerror(s)
char *s;
{
	fflush(stdout);
	printf("\n%*s\n%*s\n", column, "^", column, s);
}
