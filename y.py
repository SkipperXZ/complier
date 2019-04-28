# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 16:16:48 2019

@author: User
"""

# Yacc example
 
import ply.yacc as yacc
 
 # Get the token map from the lexer.  This is required.
from l import tokens
   
precedence = (
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIVIDE'),
        ('right', 'UMINUS')
        )

def p_starter_loop(p):
    '''
    starter : starter external_declaration
    '''
    p[0] = ('multi',p[1],p[2])
def p_starter(p):
    '''
    starter : external_declaration
    '''
    p[0] = p[1]
def p_external_declaration(p):
    '''
    external_declaration : declaration
                         | statement	     
    '''
    p[0] = p[1]
def p_signed_number(p):
    '''
    signed_number : MINUS NUMBER %prec UMINUS
    '''
    p[0] = -p[2]
    
def p_expression_array(p):
    '''
    expression : NAME LBK NUMBER RBK
    '''
    p[0] = p[1]+p[2]+str(p[3])+p[4]
def p_expression_number(p):
    '''
      expression : signed_number
                 | NUMBER
                 | NAME
    '''
    p[0] = p[1]
    
def p_expression(p):
    '''
    expression : expression PLUS expression
               | expression MINUS expression
               | expression TIMES expression
               | expression DIVIDE expression
               | expression MOD expression
               | expression LT_OP expression
               | expression GT_OP expression
               | expression EQ_OP expression
               | expression NE_OP expression
               | LPAREN expression RPAREN
    '''
    if p[2] == '+':
        p[0] = ('+',p[1],p[3])
    elif p[2] == '-':
        p[0] = ('-',p[1],p[3])
    elif p[2] == '*':
        p[0] = ('*',p[1],p[3])
    elif p[2] == '/':
        p[0] = ('/',p[1],p[3])
    elif p[2] == '%':
        p[0] = ('%',p[1],p[3])
    elif p[2] == '<':
        p[0] = ('<',p[1],p[3])
    elif p[2] == '>':
        p[0] = ('>',p[1],p[3])
    elif p[2] == '==':
        p[0] = ('==',p[1],p[3])
    elif p[2] == '!=':
        p[0] = ('!=',p[1],p[3])
    else:
        p[0] = p[2]
    
def p_init_declarator_notassign(p): 
    '''
    init_declarator : declarator
    '''
    p[0] = p[1]
    
def p_init_declarator_array(p):
    '''
    init_declarator : declarator LBK NUMBER RBK EQUALS expression
    '''
    p[0] = ('assign-value', p[1]+p[2]+str(p[3])+p[4], p[6])
def p_init_declarator(p):
    '''
    init_declarator : declarator EQUALS expression
    '''
    p[0] = ('assign-value', p[1], p[3])
def p_array_init_declarator(p):
    '''
    init_declarator_array : declarator EQUALS LBK array_declarator RBK
    '''
    p[0] = (p[1], p[4])
def p_array_number(p):
    '''
    array_declarator : NUMBER
    '''
    p[0] = p[1]
    
def p_array_declarator(p):
    '''
    array_declarator : array_declarator COMMA NUMBER
    '''
    p[0] = (p[1],p[3])
    
def p_array_declaration(p):
    '''
    declaration : declaration_specifiers LBK NUMBER RBK init_declarator_array SEMICO
    '''
    p[0] = ('declare-array',p[3],p[5])
    
def p_array_as_name(p):
    '''
    declarator : NAME LBK NUMBER RBK
    '''
    p[0] = p[1]+p[2]+str(p[3])+p[4]
def p_declarator(p):
    '''
    declarator : NAME
    '''
    p[0] = p[1]
    
def p_declaration(p):
    '''
    declaration  : declaration_specifiers init_declarator SEMICO
    '''
    p[0] = ('declare-value',p[2])

def p_assign_exist_id(p):
    '''
    declaration : init_declarator SEMICO
    '''
    p[0] = p[1]
    
def p_declaration_specifiers(p):
    '''
    declaration_specifiers : INT64
                           | ARRAY
    '''
    p[0] = p[1]
    
def p_statement(p):
    '''
    statement : expression_statement
              | selection_statement
              | iteration_statement
              | jump_statement
              | compound_statement
              | display_statement
    '''
    p[0] = p[1]
    
def p_display_statement_str(p):
    '''
    display_statement : DISPLAY LPAREN STRING RPAREN SEMICO
    '''
    
    p[0] = ('display-string',p[3])
def p_display_statement_var(p):
    '''
    display_statement : DISPLAY LPAREN NAME RPAREN SEMICO
    '''
    
    p[0] = ('display-var',p[3])
def p_compound_empty_statement(p):
    '''
    compound_statement : LCB RCB
    '''
    
def p_compound_statement(p):
    '''
    compound_statement : LCB multi_statement RCB
                       | LCB selection_statement RCB
    '''
    p[0] = p[2]
    
def p_declaration_list_single(p): 
    '''
    multi_statement : declaration
    '''
    p[0] = p[1]
def p_declaration_list(p):
    '''
    multi_statement : multi_statement declaration
    '''
    p[0] = ('multi',p[1],p[2])
def p_statement_list_single(p):
    '''
    multi_statement : statement
    '''
    p[0] = p[1]
def p_statement_list(p):
    '''
    multi_statement : multi_statement statement
    '''
    p[0] = ('multi', p[1],p[2])
def p_expresseion_close_statement(p):
    '''
    expression_statement : SEMICO
    '''
def p_expression_statement(p):
    '''
    expression_statement : expression SEMICO
    '''
    p[0] = p[1]

def p_selection_statement_else(p):
    '''
    selection_statement : IF LPAREN expression RPAREN statement ELSE statement
    '''
    p[0] = ('multi',('if-else',p[3],p[5]),('else',p[7]))
def p_selection_statement(p):
    '''
    selection_statement : IF LPAREN expression RPAREN statement
    '''
    p[0] = ('if',p[3],p[5])
def p_iteration_statement(p):
    '''
    iteration_statement : FOR LPAREN NUMBER RPAREN statement
    '''
    p[0] = ('for',p[3],p[5])
def p_jump_statement(p):
    '''
    jump_statement : BREAK SEMICO
    '''
    p[0] = 'break'
    
 # Error rule for syntax errors
def p_error(p):
     print("Syntax error in input!")


 # Build the parser
parser = yacc.yacc()


result = parser.parse('''
                      display("test");
                      ''')
#print(result)
#print(asm_data)

#base_statement(result)
