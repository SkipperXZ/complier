from y import result

#loop count
count = 0
count_IF = 1
ELSE_stmt = []
#------ joel
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
def push(register):
    print('push  %s'%register)
def pop(register):
    print('pop  %s'%register)

# base statement
def base_statement(stmt):
    if stmt:
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
        if stmt[0] == 'for':
            loop_statement(stmt[1],stmt[2])
        if stmt[0] == 'if':
            compare_value(stmt[1],stmt[2])
        if stmt[0] == 'else':
            ELSE_statement(stmt[1])
            
def compare_value(stmt1,stmt2):
    global count_IF
    print(' cmp        %s,    %s'%(stmt1[1],stmt1[2]))
    if stmt1[0] == '>':
        print(' jg        else%d'%(count_IF))
        ELSE_stmt.append(count_IF)
    elif stmt1[0] == '<':
        print(' jl         else%d'%(count_IF))
        ELSE_stmt.append(count_IF)
    elif stmt1[0] == '==':
        print(' je         else%d'%(count_IF))
        ELSE_stmt.append(count_IF)
    elif stmt1[0] == '!=':
        print(' jne        else%d'%(count_IF))
        ELSE_stmt.append(count_IF)
    count_IF+=1
    base_statement(stmt2)

def ELSE_statement(stmt):
    print(' jmp      both%d'%(ELSE_stmt[len(ELSE_stmt)-1]))
    print('else%s:'%(ELSE_stmt[len(ELSE_stmt)-1]))
    base_statement(stmt)
    print('both%s:'%(ELSE_stmt[len(ELSE_stmt)-1]))
    ELSE_stmt.pop(len(ELSE_stmt)-1)

def assign_value(var_name):
    print("mov  %s,eax"%var_name)

def cal_func(stmt):
    if type(stmt[1]) is tuple and type(stmt[2]) is tuple:
        cal_func(stmt[1])
        push('eax')
        cal_func(stmt[2])
        if stmt[0] == '+':
            print('pop   ebx')
            print('add   eax,ebx')
        elif stmt[0] == '-':
            print('pop   ebx')
            print('sub   eax,ebx')
        elif stmt[0] == '*':
            print('pop   ebx')
            print('mul   ebx')
        elif stmt[0] == '/':
            print('pop   ecx')
            print('div   ecx')  
            print('mov  eax,edx')
    elif type(stmt[1]) is tuple:
        cal_func(stmt[1])
        if stmt[0] == '+':
            print('add  eax,%s'%stmt[2])
        elif stmt[0] == '-':
            print('sub  eax,%s'%stmt[2])
        elif stmt[0] == '*':
            print('mov  ebx,%s'%stmt[2])
            print('mul  ebx')
        elif stmt[0] == '/':
            print('mov  ecx,%s'%stmt[2])
            print('div  ecx')    
    elif type(stmt[2]) is tuple:
        cal_func(stmt[2])
        if stmt[0] == '+':
            print('add  eax,%s'%stmt[1])
        elif stmt[0] == '-':
            print('sub  eax,%s'%stmt[1])
        elif stmt[0] == '*':
            print('mov  ebx,%s'%stmt[1])
            print('mul  ebx')
        elif stmt[0] == '/':
            print('mov  ecx,%s'%stmt[2])
            print('div  ecx')    
    elif stmt[0] == '+':
        add_func(stmt[1],stmt[2])
    elif stmt[0] == '-':
        sub_func(stmt[1],stmt[2]) 
    elif stmt[0] == '*':
        mul_func(stmt[1],stmt[2])
    elif stmt[0] == '/':
        div_func(stmt[1],stmt[2])       

def add_func(first,second):
    print('mov  eax,%s'%first)
    print('add  eax,%s'%second)

 
def sub_func(first,second):    
    print('mov  eax,%s'%first)
    print('sub  eax,%s'%second)

def mul_func(first,second):    
    print('mov  eax,%s'%first)
    print('mov  ebx,%s'%second)
    print('mul  ebx')    
    

def div_func(first,second): 
    print('mov  eax,%s'%first)
    print('mov  ecx,%s'%second)
    print('div  ecx')    

def recursion_statement(stmt1,stmt2):
    base_statement(stmt1)
    base_statement(stmt2)


def declar_var(stmt):
    if stmt[0] == 'assign-value':
        var_name = stmt[1]
        val = stmt[2]
    if check_var_not_duplicate(var_name):
        var_list.append(var_name)
        print(".data       %s     dd      %d"%(var_name,val))
        #asm_data+= '''         '''+var_name+''':     dw      '''+str(val)+'''/n''' 
    else:
        print("Failed Variable is Duplicate")

def loop_statement(num, stmt):
    global count
    temp_count = count
    count += 1
    print('mov	cx, '+ str(num))
    print('for'+str(temp_count)+':')
    print('push cx')
    base_statement(stmt)
    print('pop cx')
    print('loop for'+str(temp_count))


'''
while True:
    try:
        s = input('calc > ')
    except EOFError:
        break
    if not s: continue
'''

#print(result)
#print(asm_data)

base_statement(result)
