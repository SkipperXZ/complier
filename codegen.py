from y import result
import sys

#loop count
count = 0
count_IF = 1
index = 0
ELSE_stmt = []

# visit multiple statement  
instr_list = ['main:']  
data_list = ['.data\n',"msg db \"$\""] 
var_list = []
array_var_list = []
Error = []

    
            
def print_instr(instr):
    if '[' not in instr:
        pass
    else:
        tempinstr = instr
        for i in var_list:
            if i in instr and '[' in i:
                splited_1 = i.split('[')
                splited_2 = splited_1[1].split(']')
                tempinstr = tempinstr.replace(i, splited_1[0]+'['+ str(int(splited_2[0])*4) +']'+splited_2[1])
        instr = tempinstr
    instr_list.append(instr)    

def print_cll_module_instr():

    print('''jmp finish
        printvar:
            mov bx,0
            jmp digit

        digit:
            mov edx,0
            mov ecx,10
            div ecx
            inc bx
            push edx

            cmp eax,0
            jg digit
            mov cx,bx
            jmp print
        print: 
            pop edx
            add edx,48
            mov  ah, 02h    
            int 21h
            loop print	
            ret
        printstr: 
            mov  ah, 02h    
            int 21h
            ret
        finish:
            ret
        end main''')

def print_header():
    print('''
      .model tiny
      .386
      ''')
    for ele in data_list:
        print(ele)
    print('''
        .code
        org 100h
    ''')
    
def print_all_instr():

    for ele in instr_list:
        print(ele)        

      

def print_instr_without_check_array(instr):  
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
                sys.exit("Unidentified Variable")
            elif (type(stmt[1]) is str  and type(stmt[2]) is int) or (type(stmt[1]) is str  and type(stmt[2]) is str):
                if check_var_not_duplicate(stmt[1]) or check_var_not_duplicate(stmt[2]):
                    sys.exit("Unidentified Variable")
                print_instr("mov    %s,%s"%(stmt[1],stmt[2]))
                return
            elif type(stmt[2]) is tuple:
                cal_func(stmt[2])
            else:
                print_instr("mov  eax,%s"%(stmt[1]))
            assign_value(stmt[1])
        if stmt[0] == 'declare-array':
            declar_array(stmt[1],stmt[2])
#        if stmt[0] == 'assign-array':
#            assign_array(stmt[1],stmt[2])     
        if stmt[0] == 'for':
            loop_statement(stmt[1],stmt[2])
        if stmt[0] == 'if-else':
            compare_value_ifelse(stmt[1],stmt[2])
        if stmt[0] == 'else':
            else_statement(stmt[1])
        if stmt[0] == 'if':
            compare_value_if(stmt[1],stmt[2])
        if stmt[0] == 'display-var':
            display_var(stmt[1])
        if stmt[0] == 'display-string':
            display_str(stmt[1])
        if stmt[0] == 'display-array':
            display_array(stmt[1],stmt[2])
            
def display_array(arr_name,arr_index):
    
    if(type(arr_index) is int):
        print_instr("push eax")
        print_instr("push ebx")
        print_instr("push ecx")
        print_instr("push edx")
        print_instr_without_check_array("mov   eax,%s[%s]"%(arr_name,arr_index*4))
        print_instr("call printvar")
        print_instr("pop edx")
        print_instr("pop ecx")
        print_instr("pop ebx")
        print_instr("pop eax")
    else:
        print_instr("push eax")
        print_instr("push ebx")
        print_instr("push ecx")
        print_instr("push edx")
        mul_func("i",4)
        print_instr("mov   esi,eax")
        print_instr_without_check_array("mov   eax,%s[si]"%arr_name)
        print_instr("call printvar")
        print_instr("pop edx")
        print_instr("pop ecx")
        print_instr("pop ebx")
        print_instr("pop eax")

def display_str(str): 
    print_instr("mov msg,%s"%str)
    print_instr("mov edx,offset msg")
    print_instr("call printstr")
        
def display_var(var_name):
    
    if not check_var_not_duplicate(var_name):
        print_instr("push eax")
        print_instr("push ebx")
        print_instr("push ecx")
        print_instr("push edx")
        print_instr("mov   eax,%s"%var_name)
        print_instr("call printvar")
        print_instr("pop edx")
        print_instr("pop ecx")
        print_instr("pop ebx")
        print_instr("pop eax")
        
    else:
        sys.exit('Unidentified Variable')
def recur_assign_array(stmt):
    if type(stmt[0]) is tuple:
        recur_assign_array(stmt[0])
    elif type(stmt[0]) is int:
        array_var_list.append(stmt[0])
    if type(stmt[1]) is tuple:
        recur_assign_array(stmt[1])
    elif type(stmt[1]) is int:  
        array_var_list.append(stmt[1])
        
def declar_array(size,stmt):
    global index
    #if stmt[0] == 'assign-array':
    recur_assign_array(stmt[1])
    temp_str = '%s dd '%stmt[0]
    temp_ele = ''
    if not check_var_not_duplicate('%s[%s]'%(stmt[0],index)):
        sys.exit('variable duplicate')
        return
    for ele in array_var_list:
        temp_ele += str(ele) 
        if array_var_list[len(array_var_list)-1] != ele:
            temp_ele += ' , '
        if check_var_not_duplicate('%s[%s]'%(stmt[0],index)):
            var_list.append('%s[%s]'%(stmt[0],index))
            index += 1
    data_list.append(temp_str + temp_ele)
    array_var_list.clear()
    index = 0
    #elif type(stmt[2]) is str:
        #data_list.append('%s times %s dd 0'%(stmt[2],size))
            
#declarator EQUALS LBK array_declarator RBK
'''
def assign_array(name,stmt):
    global index
    if type(stmt[0]) is tuple:
        assign_array(name,stmt[0])
    elif type(stmt[0]) is int:
        print_instr('mov	%s[%s], %s'%(name,index,stmt[0]))
        if check_var_not_duplicate('%s[%s]'%(name,index)):
            var_list.append('%s[%s]'%(name,index))
        index += 4
    if type(stmt[1]) is tuple:
        assign_array(name,stmt[1])
    elif type(stmt[1]) is int:
        print_instr('mov	%s[%s], %s'%(name,index,stmt[1]))
        if check_var_not_duplicate('%s[%s]'%(name,index)):
            var_list.append('%s[%s]'%(name,index))
        index += 4
'''
def compare_value_if(stmt1,stmt2):
    global count_IF
    print_instr(' mov        eax,  %s'%(stmt1[1]))
    print_instr(' mov        ebx,  %s'%(stmt1[2]))
    print_instr(' cmp        eax,    ebx')
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
    count_IF+=1
    base_statement(stmt2)
    print_instr('nextInstr%s:'%(ELSE_stmt[len(ELSE_stmt)-1]))
    ELSE_stmt.pop(len(ELSE_stmt)-1)

def compare_value_ifelse(stmt1,stmt2):
    global count_IF
    print_instr(' mov        eax,  %s'%(stmt1[1]))
    print_instr(' mov        ebx,  %s'%(stmt1[2]))
    print_instr(' cmp        eax,    ebx')
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
    if check_var_not_duplicate(var_name):
        sys.exit("Unidentified Variable")
    
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
            print_instr('mov  edx, 0')
            print_instr('pop   ecx')
            print_instr('div   ecx')  
        elif stmt[0] == '%':
            print_instr('mov  edx, 0')
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
            print_instr('mov  edx, 0')
            print_instr('mov  ecx,%s'%stmt[2])
            print_instr('div  ecx')  
        elif stmt[0] == '%':
            print_instr('mov  edx, 0')
            print_instr('mov  ecx,%s'%stmt[2])
            print_instr('div  ecx')   
            print_instr('mov  eax,edx') 
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
        elif stmt[0] == '%':
            print_instr('mov  ecx,%s'%stmt[1])
            print_instr('div  ecx')     
            print_instr('mov  eax,edx') 
    elif stmt[0] == '+':
        add_func(stmt[1],stmt[2])
    elif stmt[0] == '-':
        sub_func(stmt[1],stmt[2]) 
    elif stmt[0] == '*':
        mul_func(stmt[1],stmt[2])
    elif stmt[0] == '/':
        div_func(stmt[1],stmt[2])
    elif stmt[0] == '%':
        mod_func(stmt[1],stmt[2])          

def add_func(first,second):
    if (type(first) is str and check_var_not_duplicate(first)) or (type(second) is str and check_var_not_duplicate(second)):
        Error.append("Unidentified Variable")
        sys.exit(Error)
    print_instr('mov  eax,%s'%first)
    print_instr('add  eax,%s'%second)

 
def sub_func(first,second):
    if (type(first) is str and check_var_not_duplicate(first)) or (type(second) is str and check_var_not_duplicate(second)):
        sys.exit("Unidentified Variable")    
    print_instr('mov  eax,%s'%first)
    print_instr('sub  eax,%s'%second)

def mul_func(first,second):
    if (type(first) is str and check_var_not_duplicate(first)) or (type(second) is str and check_var_not_duplicate(second)):
        sys.exit("Unidentified Variable")  
    print_instr('mov  eax,%s'%first)
    print_instr('mov  ebx,%s'%second)
    print_instr('mul  ebx')    
    

def div_func(first,second):
    if (type(first) is str and check_var_not_duplicate(first)) or (type(second) is str and check_var_not_duplicate(second)):
        sys.exit("Unidentified Variable")
    print_instr('mov  edx, 0')
    print_instr('mov  eax,%s'%first)
    print_instr('mov  ecx,%s'%second)
    print_instr('div  ecx')    
 
def mod_func(first,second):
    if (type(first) is str and check_var_not_duplicate(first)) or (type(second) is str and check_var_not_duplicate(second)):
        sys.exit("Unidentified Variable")
    print_instr('mov  edx, 0')
    print_instr('mov  eax,%s'%first)
    print_instr('mov  ecx,%s'%second)
    print_instr('div  ecx')    
    print_instr('mov  eax,edx')  

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

print_header()
print_all_instr()
print_cll_module_instr()





