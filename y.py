# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 16:16:48 2019

@author: User
"""

# Yacc example
 
import ply.yacc as yacc
 
 # Get the token map from the lexer.  This is required.
from l import tokens
   
class node:
    def  __init__(self, op, left=None, right=None):
        self.op = op
        self.left = left
        self.right = right


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
    
def p_init_declarator_notassign(p): 
    '''
    init_declarator : declarator
    '''
    p[0] = p[1]
    
def p_init_declarator(p):
    '''
    init_declarator : declarator EQUALS expression
    '''
    p[0] = ('assign-value', p[1], p[3])
def p_array_init_declarator(p):
    '''
    init_declarator : declarator EQUALS LBK array_declarator RBK
    '''
    p[0] = ('assign-array',p[1], p[4])
def p_array_number(p):
    '''
    array_declarator : NUMBER
    '''
    p[0] = p[1]
    
def p_array_declarator(p):
    '''
    array_declarator : array_declarator COMMA NUMBER
    '''
    p[0] = (',',p[1],p[3])
    
def p_array_declaration(p):
    '''
    declaration : declaration_specifiers LBK NUMBER RBK init_declarator SEMICO
    '''
    p[0] = ('declare-array',p[3],p[5])
    
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
    '''
    p[0] = p[1]
    
def p_compound_empty_statement(p):
    '''
    compound_statement : LCB RCB
    '''
def p_compound_statement(p):
    '''
    compound_statement : LCB statement_list RCB
                       | LCB declaration_list RCB
                       | LCB declaration_list statement_list RCB
    '''
    p[0] = p[2]
    
def p_declaration_list_single(p): 
    '''
    declaration_list : declaration
    '''
    p[0] = p[1]
def p_declaration_list(p):
    '''
    declaration_list : declaration_list declaration
    '''
    p[0] = (p[1],p[2])
def p_statement_list_single(p):
    '''
    statement_list : statement
    '''
    p[0] = p[1]
def p_statement_list(p):
    '''
    statement_list : statement_list statement
    '''
    p[0] = (p[1],p[2])
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
    p[0] = ('if-else',p[3],p[5],p[7])
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
     

        
 
        
# visit multiple statement     
var_list = []
asm_data = '''.data

            '''
def check_var_not_duplicate(var_name):
    for i in range(len(var_list)):
        if(var_list[i] == var_name):
            #print("%s == %s"%(var_list[i],var_name))
            return False
    return True

# base statement
def base_statement(stmt):
    if stmt[0] == 'multi':
        recursion_statement(stmt[1],stmt[2])
    if stmt[0] == 'declare-value':  
        declar_var(stmt[1])
    if stmt[0] == 'assign-value':  
        if check_var_not_duplicate(stmt[1]):
            return
        if type(stmt[2]) is tuple:
            cal_func(stmt[2])
        else:
            
            print("mov  eax,%s"%(stmt[1]))
        assign_value(stmt[1])

def assign_value(var_name):
    print("mov  eax,[%s]"%(var_name))

def cal_func(stmt):
    if type(stmt[1]) is tuple:
        cal_func(stmt[1])
        if stmt[0] == '+':
            print('add  eax,%s'%stmt[2])
        elif stmt[0] == '-':
            print('sub  eax,%s'%stmt[2])
    elif stmt[0] == '+':
        add_func(stmt[1],stmt[2])
    elif stmt[0] == '-':
        sub_func(stmt[1],stmt[2])    

def add_func(first,second):
    print('mov  %s,eax'%first)
    print('add  eax,%s'%second)
 
def minus_func(first,second):    
    print('mov  %s,eax'%first)
    print('sub  eax,%s'%second)



def recursion_statement(stmt1,stmt2):
    base_statement(stmt1)
    base_statement(stmt2)


def declar_var(stmt):
    if stmt[0] == 'assign-value':
        var_name = stmt[1]
        val = stmt[2]
    if check_var_not_duplicate(var_name):
        var_list.append(var_name)
        print(".data       %s     dw      %d"%(var_name,val))
        #asm_data+= '''         '''+var_name+''':     dw      '''+str(val)+'''/n''' 
    else:
        print("Failed Variable is Duplicate")

  
     
 
 # Build the parser
parser = yacc.yacc()


'''
while True:
    try:
        s = input('calc > ')
    except EOFError:
        break
    if not s: continue
'''
result = parser.parse('''int64 a=1;
                      int64 b=5;
                      int64 c=3;
                      int64 d=7;
                      int64 e=9;
                      a= 5+7+6-7;
                      b= 5+3-1-5-7;''')
print(result)
print(asm_data)

base_statement(result)
