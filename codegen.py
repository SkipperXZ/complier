from y import result
import sys

#loop count
count = 0
count_IF = 1
ELSE_stmt = []
#------ joel
# visit multiple statement  
instr_list = []  
data_list = ['.data'] 
var_list = []
Error = []
asm_data = '''.data

            '''
            
def print_instr(instr):
    instr_list.append(instr)        
            
def check_var_not_duplicate(var_name):
    for i in range(len(var_list)):
        if(var_list[i] == var_name):
            #print("%s == %s"%(var_list[i],var_name))
            return False
    return True
def push(register):
    print_instr('push  %s'%register)
def pop(register):
    print_instr('pop  %s'%register)

# base statement
def base_statement(stmt):
    if stmt:
        if stmt[0] == 'multi':
            recursion_statement(stmt[1],stmt[2])
        if stmt[0] == 'declare-value':  
            declar_var(stmt[1])
        if stmt[0] == 'assign-value':  
            if type(stmt[1]) is str and check_var_not_duplicate(stmt[1]):
                    Error.append("Unidentified Variable")
                    sys.exit(Error)
            if type(stmt[2]) is tuple:
                cal_func(stmt[2])
            else:
                if type(stmt[1]) is str and check_var_not_duplicate(stmt[1]):
                    Error.append("Unidentified Variable")
                    sys.exit(Error)
                print_instr("mov  eax,%s"%(stmt[1]))
            assign_value(stmt[1])
        if stmt[0] == 'for':
            loop_statement(stmt[1],stmt[2])
        if stmt[0] == 'if-else':
            compare_value_ifelse(stmt[1],stmt[2])
        if stmt[0] == 'else':
            else_statement(stmt[1])
        if stmt[0] == 'if':
            compare_value_if(stmt[1],stmt[2])

def compare_value_if(stmt1,stmt2):
    global count_IF
    print_instr(' mov        eax,  %s'%(stmt1[1]))
    print_instr(' cmp        %s,    %s'%(stmt1[1],stmt1[2]))
    if stmt1[0] == '>':
        print_instr(' jle        nextInstr%d'%(count_IF))
        ELSE_stmt.append(count_IF)
    elif stmt1[0] == '<':
        print_instr(' jge         nextInstr%d'%(count_IF))
        ELSE_stmt.append(count_IF)
    elif stmt1[0] == '==':
        print_instr(' jne         nextInstr%d'%(count_IF))
        ELSE_stmt.append(count_IF)
    elif stmt1[0] == '!=':
        print_instr(' je        nextInstr%d'%(count_IF))
        ELSE_stmt.append(count_IF)
    temp_count_IF = count_IF
    count_IF+=1
    base_statement(stmt2)
    print_instr('nextInstr%s:'%(ELSE_stmt[len(ELSE_stmt)-1]))
    ELSE_stmt.pop(len(ELSE_stmt)-1)

def compare_value_ifelse(stmt1,stmt2):
    global count_IF
    print_instr(' mov        eax,  %s'%(stmt1[1]))
    print_instr(' cmp        %s,    %s'%(stmt1[1],stmt1[2]))
    if stmt1[0] == '>':
        print_instr(' jle         else%d'%(count_IF))
        ELSE_stmt.append(count_IF)
    elif stmt1[0] == '<':
        print_instr(' jge         else%d'%(count_IF))
        ELSE_stmt.append(count_IF)
    elif stmt1[0] == '==':
        print_instr(' jne         else%d'%(count_IF))
        ELSE_stmt.append(count_IF)
    elif stmt1[0] == '!=':
        print_instr(' je        else%d'%(count_IF))
        ELSE_stmt.append(count_IF)
    temp_count_IFELSE = count_IF
    count_IF+=1
    base_statement(stmt2)
    print_instr(' jmp      nextInstr%d'%(temp_count_IFELSE))

def else_statement(stmt):
    print_instr('else%s:'%(ELSE_stmt[len(ELSE_stmt)-1]))
    base_statement(stmt)
    print_instr('nextInstr%s:'%(ELSE_stmt[len(ELSE_stmt)-1]))
    ELSE_stmt.pop(len(ELSE_stmt)-1)

def assign_value(var_name):
    if type(var_name) is str and check_var_not_duplicate(var_name):
        Error.append("Unidentified Variable")
        sys.exit(Error)
    print_instr("mov  %s,eax"%var_name)

def cal_func(stmt):
    if type(stmt[1]) is tuple and type(stmt[2]) is tuple:
        cal_func(stmt[1])
        push('eax')
        cal_func(stmt[2])
        if stmt[0] == '+':
            print_instr('pop   ebx')
            print_instr('add   eax,ebx')
        elif stmt[0] == '-':
            print_instr('pop   ebx')
            print_instr('sub   eax,ebx')
        elif stmt[0] == '*':
            print_instr('pop   ebx')
            print_instr('mul   ebx')
        elif stmt[0] == '/':
            print_instr('pop   ecx')
            print_instr('div   ecx')  
            print_instr('mov  eax,edx')
    elif type(stmt[1]) is tuple:
        cal_func(stmt[1])
        if stmt[0] == '+':
            print_instr('add  eax,%s'%stmt[2])
        elif stmt[0] == '-':
            print_instr('sub  eax,%s'%stmt[2])
        elif stmt[0] == '*':
            print_instr('mov  ebx,%s'%stmt[2])
            print_instr('mul  ebx')
        elif stmt[0] == '/':
            print_instr('mov  ecx,%s'%stmt[2])
            print_instr('div  ecx')    
    elif type(stmt[2]) is tuple:
        cal_func(stmt[2])
        if stmt[0] == '+':
            print_instr('add  eax,%s'%stmt[1])
        elif stmt[0] == '-':
            print_instr('sub  eax,%s'%stmt[1])
        elif stmt[0] == '*':
            print_instr('mov  ebx,%s'%stmt[1])
            print_instr('mul  ebx')
        elif stmt[0] == '/':
            print_instr('mov  ecx,%s'%stmt[1])
            print_instr('div  ecx')    
    elif stmt[0] == '+':
        add_func(stmt[1],stmt[2])
    elif stmt[0] == '-':
        sub_func(stmt[1],stmt[2]) 
    elif stmt[0] == '*':
        mul_func(stmt[1],stmt[2])
    elif stmt[0] == '/':
        div_func(stmt[1],stmt[2])       

def add_func(first,second):
    if (type(first) is str and check_var_not_duplicate(first)) or (type(second) is str and check_var_not_duplicate(second)):
        Error.append("Unidentified Variable")
        sys.exit(Error)
    print_instr('mov  eax,%s'%first)
    print_instr('add  eax,%s'%second)

 
def sub_func(first,second):
    if (type(first) is str and check_var_not_duplicate(first)) or (type(second) is str and check_var_not_duplicate(second)):
        Error.append("Unidentified Variable")
        sys.exit(Error)    
    print_instr('mov  eax,%s'%first)
    print_instr('sub  eax,%s'%second)

def mul_func(first,second):
    if (type(first) is str and check_var_not_duplicate(first)) or (type(second) is str and check_var_not_duplicate(second)):
        Error.append("Unidentified Variable")
        sys.exit(Error)  
    print_instr('mov  eax,%s'%first)
    print_instr('mov  ebx,%s'%second)
    print_instr('mul  ebx')    
    

def div_func(first,second):
    if (type(first) is str and check_var_not_duplicate(first)) or (type(second) is str and check_var_not_duplicate(second)):
        Error.append("Unidentified Variable")
        sys.exit(Error)
    print_instr('mov  eax,%s'%first)
    print_instr('mov  ecx,%s'%second)
    print_instr('div  ecx')    

def recursion_statement(stmt1,stmt2):
    base_statement(stmt1)
    base_statement(stmt2)


def declar_var(stmt):
    if not type(stmt) is tuple:
        var_name = stmt
        val = 0
    elif stmt[0] == 'assign-value':
        var_name = stmt[1]
        val = stmt[2]
    if check_var_not_duplicate(var_name):
        var_list.append(var_name)
        data_list.append("       %s     dd      %d"%(var_name,val))
        #asm_data+= '''         '''+var_name+''':     dw      '''+str(val)+'''/n''' 
    else:
        sys.exit("Failed Variable is Duplicate")

def loop_statement(num, stmt):
    global count
    temp_count = count
    count += 1
    print_instr('mov	cx, '+ str(num))
    print_instr('for'+str(temp_count)+':')
    print_instr('push cx')
    base_statement(stmt)
    print_instr('pop cx')
    print_instr('loop for'+str(temp_count))


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
#print(Error)
for ele in data_list:
    print(ele)
for ele in instr_list:
    print(ele)
