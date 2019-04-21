%token IDENTIFIER STRING_LITERAL CONSTANT HEX
%token LE_OP GE_OP EQ_OP NE_OP
%token INT64 ARRAY
%token IF ELSE WHILE DO FOR BREAK 

%start starter
%%

primary_expression
	: IDENTIFIER
    | CONSTANT
	| STRING_LITERAL
	| HEX
	;

unary_operator
	: '+'
	| '-'
	;

cast_expression
	: unary_operator primary_expression 
	| '(' cast_expression ')'
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

init_declarator
	: declarator 
	| declarator CONSTANT
	| declarator '=' additive_expression
	;

declarator 
	: IDENTIFIER
	;

declaration
	: declaration_specifiers ';'
	| declaration_specifiers init_declarator ';'
	;

declaration_specifiers
	: INT64
	;

statement
	: expression_statement
	| selection_statement
	| iteration_statement
	| jump_statement
	| compound_statement
	;

compound_statement
	: '{' '}'
	| '{' statement_list '}'
	| '{' declaration_list '}'
	| '{' declaration_list statement_list '}'
	;

declaration_list
	: declaration
	| declaration_list declaration
	;

statement_list
	: statement
	| statement_list statement
	;

expression_statement
	: ';'
	| equality_expression ';'
	;

selection_statement
	: IF '(' equality_expression ')' statement
	| IF '(' equality_expression ')' statement ELSE statement
	;

iteration_statement
	: FOR '(' CONSTANT ')' statement
	;

jump_statement
	: BREAK ';'
	;

starter
	: external_declaration
	| starter external_declaration
	;

external_declaration
	: declaration
	| statement	
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
