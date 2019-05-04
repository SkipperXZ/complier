import sys
# write file

#loop count
count_loop = 0
temp = 0
count_str_label = 0
count_IF = 1
index = 0
ELSE_stmt = []

# visit multiple statement  
instr_list = []  
data_list = ['hexformat: dq "%llx",10,0','decformat: dq "%lld",10,0','newLineMsg dq 0xA, 0xD'] 
var_list = []
hex_list = []
array_var_list = []
array_list = []
Error = []

def convert_var(t):
    if type(t) is int:
        return t
    else:
        return '['+str(t)+']'

def is_array(str1):
    if not type(str1) is int :
        if '[' in str1:
            return True
        else:
            return False
    else:
        return False

def spilt_array_name(array_var):
        name = array_var.split('[')[0]
        index = ((array_var.split('[')[1]).split(']'))[0]
        if index.isdigit():
            return (name,int(index))
        else:
            return (name,index)

def is_var_index_array(array_var):
        arr = spilt_array_name(array_var)
        name = arr[0]
        index = arr[1]
        if not index.isdigit():
            return True
        else:
            return False 

def print_instr(instr):
    instr_list.append(instr)    


def print_header(f):
    f.write('section .data\n\t')
    for ele in data_list:
        f.write(ele)
        f.write('\n\t')
    f.write('''global main
    extern printf
section .text
main:
''')

def print_all_instr(f):
    for ele in instr_list:
        f.write(ele) 
        f.write('\n\t')

            
def error_undefine_var():
    sys.exit('Undenfied Variable')
def error_duplicate_define_var():
    sys.exit('Duplicate Variable')

def is_define_var(var):

    if '[' in var:
        print(var)
        for i in range(len(array_list)):
            if array_list[i] == spilt_array_name(var)[0]:
                return True
    for i in range(len(var_list)):
        if(var_list[i] == var):
            return True
    error_undefine_var()
    return False

def is_define_not_duplicate(var):
    for i in range(len(array_list)):
        if '[' in var:
            if array_list[i] == spilt_array_name(var)[0]:
                error_duplicate_define_var()
                return False
        else:
            if array_list[i] == var :
                return False
    for i in range(len(var_list)):
        if(var_list[i] == var):
            error_duplicate_define_var()
            return False

    return True

def push(register):
    print_instr('push  %s'%register)
def pop(register):
    print_instr('pop  %s'%register)

def base_statement(stmt):
    global temp
    if stmt:
        if stmt[0] == 'multi':
            recursion_statement(stmt[1],stmt[2])
        if stmt[0] == 'declare-value':  
            declar_var(stmt[1])
        if stmt[0] == 'assign-value':
            assign_func(stmt)
        if stmt[0] == 'declare-array':
            declar_array(stmt[1],stmt[2])
        if stmt[0] == 'for':
            loop_statement(stmt[1],stmt[2])
            temp -= 1
        if stmt == 'break':
            print_instr('jmp break'+str(temp))
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
            
def recursion_statement(stmt1,stmt2):
    base_statement(stmt1)
    base_statement(stmt2)

def assign_func(stmt):
    #print_instr("push    rax")  
    if type(stmt[1]) is str:
       if is_define_var(stmt[1]):
            pass
    if type(stmt[2]) is str:
        if is_define_var(stmt[2]):
            pass


    if  type(stmt[2]) is int:
         print_instr("mov    rax,%s"%convert_var(stmt[2])) 
        #print_instr("mov    %s,%s"%(convert_var(stmt[1]),convert_var(stmt[2])))
    elif type(stmt[2]) is str:
        
        if is_array(stmt[2]):
            mov_array_to_rax(stmt[2])
        else:
            print_instr("mov    rax,%s"%convert_var(stmt[2])) 
        
    elif type(stmt[2]) is tuple:
        cal_func(stmt[2])
    if is_array(stmt[1]):
        
        mov_rax_to_array(stmt[1])

    else:
        print_instr("mov  %s,rax"%convert_var(stmt[1]))
        
    #print_instr("pop    rax")

   

def cal_func(stmt):
    if type(stmt[1]) is str:
       if is_define_var(stmt[1]):
            pass
    if type(stmt[2]) is str:
        if is_define_var(stmt[2]):
            pass
    if type(stmt[1]) is tuple and type(stmt[2]) is tuple:
        cal_func(stmt[1])
        print_instr('push   rax')
        cal_func(stmt[2])
        if stmt[0] == '+':
            print_instr('pop   rbx')
            print_instr('add   rax,rbx')
        elif stmt[0] == '-':
            print_instr('pop   rbx')
            print_instr('sub   rax,rbx')
        elif stmt[0] == '*':
            print_instr('pop   rbx')
            print_instr('mul   rbx')
        elif stmt[0] == '/':
            print_instr('mov  rdx, 0')
            print_instr('mov   rcx,rax')
            print_instr('pop   rax')
            print_instr('CQO')
            print_instr('idiv   rcx')  
        elif stmt[0] == '%':
            print_instr('mov  rdx, 0')
            print_instr('mov   rcx,rax')
            print_instr('pop   rax')
            print_instr('CQO')
            print_instr('idiv   rcx')  
            print_instr('mov  rax,rdx')
    elif type(stmt[1]) is tuple:
        cal_func(stmt[1])
        if stmt[0] == '+':
            if is_array(stmt[2]):
                cal_index_esi(stmt[2])
                print_instr('add  rax,[%s+rsi]'%spilt_array_name(stmt[2])[0])
            else:
                print_instr('add  rax,%s'%convert_var(stmt[2]))
        elif stmt[0] == '-':
            if is_array(stmt[2]):
                cal_index_esi(stmt[2])
                print_instr('sub  rax,[%s+rsi]'%spilt_array_name(stmt[2])[0])
            else:
                print_instr('sub  rax,%s'%convert_var(stmt[2]))
        elif stmt[0] == '*':
            if is_array(stmt[2]):
                cal_index_esi(stmt[2])
                print_instr('mov  rbx,[%s+rsi]'%spilt_array_name(stmt[2])[0])
                print_instr('mul  rbx')
            else:
                print_instr('mov  rbx,%s'%convert_var(stmt[2]))
                print_instr('mul  rbx')
        elif stmt[0] == '/':
            if is_array(stmt[2]):
                cal_index_esi(stmt[2])
                print_instr('mov  rdx, 0')
                print_instr('CQO')
                print_instr('mov  rcx,[%s+rsi]'%spilt_array_name(stmt[2])[0])
                print_instr('idiv  rcx')  
            else:
                print_instr('mov  rdx, 0')
                print_instr('CQO')
                print_instr('mov  rcx,%s'%convert_var(stmt[2]))
                print_instr('idiv  rcx')  
        elif stmt[0] == '%':
            if is_array(stmt[2]):
                cal_index_esi(stmt[2])
                print_instr('mov  rdx, 0')
                print_instr('CQO')
                print_instr('mov  rcx,[%s+rsi]'%spilt_array_name(stmt[2])[0])
                print_instr('idiv  rcx')   
                print_instr('mov  rax,rdx') 
            else:
                print_instr('mov  rdx, 0')
                print_instr('CQO')
                print_instr('mov  rcx,%s'%convert_var(stmt[2]))
                print_instr('idiv  rcx')   
                print_instr('mov  rax,rdx') 
    elif type(stmt[2]) is tuple:
        cal_func(stmt[2])
        if stmt[0] == '+':
            if is_array(stmt[1]):
                cal_index_esi(stmt[1])
                print_instr('add  rax,[%s+rsi]'%spilt_array_name(stmt[1])[0])
            else:
                print_instr('add  rax,%s'%convert_var(stmt[1]))
        elif stmt[0] == '-':
            if is_array(stmt[1]):
                cal_index_esi(stmt[1])
                print_instr('sub  rax,[%s+rsi]'%spilt_array_name(stmt[1])[0])
            else:
                print_instr('sub  rax,%s'%convert_var(stmt[1]))
        elif stmt[0] == '*':
            if is_array(stmt[1]):
                cal_index_esi(stmt[1])
                print_instr('mov  rbx,[%s+rsi]'%spilt_array_name(stmt[1])[0])
                print_instr('mul  rbx')
            else:
                print_instr('mov  rbx,%s'%convert_var(stmt[1]))
                print_instr('mul  rbx')
        elif stmt[0] == '/':
            if is_array(stmt[1]):
                cal_index_esi(stmt[1])
                print_instr('CQO')
                print_instr('mov  rdx, 0')
                print_instr('mov  rcx,[%s+rsi]'%spilt_array_name(stmt[1])[0])
                print_instr('idiv  rcx')  
            else:
                print_instr('CQO')
                print_instr('mov  rdx, 0')
                print_instr('mov  rcx,%s'%convert_var(stmt[1]))
                print_instr('idiv  rcx')  
        elif stmt[0] == '%':
            if is_array(stmt[1]):
                cal_index_esi(stmt[1])
                print_instr('CQO')
                print_instr('mov  rdx, 0')
                print_instr('mov  rcx,[%s+rsi]'%spilt_array_name(stmt[1])[0])
                print_instr('div  rcx')   
                print_instr('mov  rax,rdx') 
            else:
                print_instr('CQO')
                print_instr('mov  rdx, 0')
                print_instr('mov  rcx,%s'%convert_var(stmt[1]))
                print_instr('div  rcx')   
                print_instr('mov  rax,rdx')  
            
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
    if is_array(first) and is_array(second):
        mov_array_to_rax(first)
        cal_index_esi(second)
        print_instr('add  rax,[%s+rsi]'%spilt_array_name(second)[0])
    elif is_array(first):
        mov_array_to_rax(first)
        print_instr('add  rax,%s'%convert_var(second))
    elif is_array(second):
        print_instr('mov  rax,%s'%convert_var(first))
        cal_index_esi(second)
        print_instr('add  rax,[%s+rsi]'%spilt_array_name(second)[0])
    else:
        print_instr('mov  rax,%s'%convert_var(first))
        print_instr('add  rax,%s'%convert_var(second))

 
def sub_func(first,second):
    if is_array(first) and is_array(second):
        mov_array_to_rax(first)
        cal_index_esi(second)
        print_instr('sub  rax,[%s+rsi]'%spilt_array_name(second)[0])
    elif is_array(first):
        mov_array_to_rax(first)
        print_instr('sub  rax,%s'%convert_var(second))
    elif is_array(second):
        print_instr('mov  rax,%s'%convert_var(first))
        cal_index_esi(second)
        print_instr('sub  rax,[%s+rsi]'%spilt_array_name(second)[0])
    else:
        print_instr('mov  rax,%s'%convert_var(first))
        print_instr('sub  rax,%s'%convert_var(second))

def mul_func(first,second):
    if is_array(first) and is_array(second):
        mov_array_to_rax(first)
        cal_index_esi(second)
        print_instr('mov  rbx,[%s+rsi]'%spilt_array_name(second)[0])
        print_instr('mul  rbx')
    elif is_array(first):
        mov_array_to_rax(first)
        print_instr('mov  rbx,%s'%convert_var(second))
        print_instr('mul  rbx') 
    elif is_array(second):
        print_instr('mov  rax,%s'%convert_var(first))
        cal_index_esi(second)
        print_instr('mov  rbx,[%s+rsi]'%spilt_array_name(second)[0])
        print_instr('mul  rbx') 
    else:
        print_instr('mov  rax,%s'%convert_var(first))
        print_instr('mov  rbx,%s'%convert_var(second))
        print_instr('mul  rbx')    
        

def div_func(first,second):
    print_instr('mov  rdx, 0')
    if is_array(first) and is_array(second):
        mov_array_to_rax(first)
        print_instr('CQO')
        cal_index_esi(second)
        print_instr('mov  rcx,[%s+rsi]'%spilt_array_name(second)[0])
        print_instr('idiv  rcx')  
    elif is_array(first):
        mov_array_to_rax(first)
        print_instr('CQO')
        print_instr('mov  rcx,%s'%convert_var(second))
        
        print_instr('idiv  rcx')  
    elif is_array(second):
        print_instr('mov  rax,%s'%convert_var(first))
        print_instr('CQO')
        cal_index_esi(second)
        print_instr('mov  rcx,[%s+rsi]'%spilt_array_name(second)[0])
        print_instr('idiv  rcx')  
    else:
        print_instr('mov  rax,%s'%convert_var(first))
        print_instr('CQO')
        print_instr('mov  rcx,%s'%convert_var(second))
        print_instr('idiv  rcx')    
 
def mod_func(first,second):
    print_instr('mov  rdx, 0')
    if is_array(first) and is_array(second):
        mov_array_to_rax(first)
        print_instr('CQO')
        cal_index_esi(second)
        print_instr('mov  rcx,[%s+rsi]'%spilt_array_name(second)[0])
        print_instr('div  rcx')  
    elif is_array(first):
        mov_array_to_rax(first)
        print_instr('CQO')
        print_instr('mov  rcx,%s'%convert_var(second))
        print_instr('idiv  rcx')  
    elif is_array(second):
        print_instr('mov  rax,%s'%convert_var(first))
        print_instr('CQO')
        cal_index_esi(second)
        print_instr('mov  rcx,[%s+rsi]'%spilt_array_name(second)[0])
        print_instr('idiv  rcx')  
    else:
        print_instr('mov  rax,%s'%convert_var(first))
        print_instr('CQO')
        print_instr('mov  rcx,%s'%convert_var(second))
        print_instr('idiv  rcx')   
    print_instr('mov  rax,rdx')  

def mov_array_to_rax(array):
    cal_index_esi(array)
    print_instr("mov rax,[%s+rsi]"%spilt_array_name(array)[0])    

def mov_rax_to_array(array):    
    cal_index_esi(array) 
    print_instr("mov [%s+rsi],rax"%spilt_array_name(array)[0])  

def cal_index_esi(array):
    print_instr('push rax')
    var = spilt_array_name(array)
    name = var[0]
    index =var[1]
    mul_func(index,8)
    print_instr("mov rsi,rax")  
    print_instr('pop rax')

def display_array(arr_name,arr_index):
        print_instr("sub rsp, 40 ")
        print_instr("push rax")
        mul_func(arr_index,8)
        print_instr("mov rsi,rax")  
        print_instr("pop rax")
        print_instr("mov rax,[%s+rsi]"%arr_name) 
        print_instr("mov rcx, decformat")    
        print_instr("movq xmm1, rax")
        print_instr("movq rdx, xmm1")
        print_instr("call printf")
        print_instr("mov rcx, newLineMsg")
        print_instr("call printf")
        print_instr("add rsp, 40 ")
   
def display_str(string): 
    global count_str_label
    data_list.append('tempstr'+str(count_str_label)+': dq '+string+' ,10 ,0')
    print_instr("sub rsp, 40 ")
    print_instr("mov rcx, tempstr"+str(count_str_label))     
    print_instr("call printf")
    print_instr("mov rcx, newLineMsg")
    print_instr("call printf")
    print_instr("add rsp, 40 ")
    count_str_label += 1
    
def display_var(var_name):
    
    if is_define_var(var_name):
        # check if var is hex
        
        for ele in hex_list:
            if var_name in ele:
                print_instr("sub rsp, 40 ")
                print_instr("mov rcx, hexformat") 
                print_instr("movq xmm1, qword [%s]"%var_name)
                print_instr("movq rdx, xmm1")
                print_instr("call printf")
                print_instr("mov rcx, newLineMsg")
                print_instr("call printf")
                print_instr("add rsp, 40 ")
                return
            
        print_instr("sub rsp, 40 ")
        print_instr("mov rcx, decformat") 
        print_instr("movq xmm1, qword [%s]"%var_name)
        print_instr("movq rdx, xmm1")
        print_instr("call printf")
        print_instr("mov rcx, newLineMsg")
        print_instr("call printf")
        print_instr("add rsp, 40 ")

        
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
    if type(stmt) is str:
        if is_define_not_duplicate(stmt):
            data_list.append(stmt+' TIMES '+str(size)+' dq 0')
    else:
        if is_define_not_duplicate(stmt[0]):
            global index
            recur_assign_array(stmt[1])
            temp_str = '%s dq '%stmt[0]
            array_list.append(stmt[0])
            print(array_list)
            temp_ele = ''
            for ele in array_var_list:
                temp_ele += str(ele) 
                if array_var_list[len(array_var_list)-1] != ele:
                    temp_ele += ' , '
            data_list.append(temp_str + temp_ele)
            array_var_list.clear()
            index = 0
        
            
def compare_value_if(stmt1,stmt2):
    global count_IF
    if  is_array(stmt1[2]) and is_array(stmt1[1]):
        mov_array_to_rax(stmt1[2])
        print_instr('mov rbx,rax')
        print_instr('push rbx')
        mov_array_to_rax(stmt1[1])
        print_instr('pop rbx')
    elif  is_array(stmt1[2]):
        mov_array_to_rax(stmt1[2])
        print_instr('mov rbx,rax')
        print_instr('mov rax,  %s'%(convert_var(stmt1[1])))
    elif is_array(stmt1[1]):
        mov_array_to_rax(stmt1[1])
        print_instr('mov rbx,  %s'%(convert_var(stmt1[2])))
    else:
        
        print_instr('mov rax,  %s'%(convert_var(stmt1[1])))
        print_instr('mov rbx,  %s'%(convert_var(stmt1[2])))


    print_instr('cmp rax, rbx')
    if stmt1[0] == '>':
        print_instr('jle        nextInstr%d'%(count_IF))
        ELSE_stmt.append(count_IF)
    elif stmt1[0] == '<':
        print_instr('jge         nextInstr%d'%(count_IF))
        ELSE_stmt.append(count_IF)
    elif stmt1[0] == '==':
        print_instr('jne         nextInstr%d'%(count_IF))
        ELSE_stmt.append(count_IF)
    elif stmt1[0] == '!=':
        print_instr('je        nextInstr%d'%(count_IF))
        ELSE_stmt.append(count_IF)
    elif stmt1[0] == '>=':
        print_instr('jl        nextInstr%d'%(count_IF))
        ELSE_stmt.append(count_IF)
    elif stmt1[0] == '<=':
        print_instr('jg        nextInstr%d'%(count_IF))
        ELSE_stmt.append(count_IF)
    count_IF+=1
    base_statement(stmt2)
    print_instr('nextInstr%s:'%(ELSE_stmt[len(ELSE_stmt)-1]))
    ELSE_stmt.pop(len(ELSE_stmt)-1)

def compare_value_ifelse(stmt1,stmt2):
    global count_IF
    if  is_array(stmt1[2]) and is_array(stmt1[1]):

        mov_array_to_rax(stmt1[2])
        print_instr('mov        rbx,rax')
        print_instr('push       rbx')
        mov_array_to_rax(stmt1[1])
        print_instr('pop       rbx')
    elif  is_array(stmt1[2]):
        mov_array_to_rax(stmt1[2])
        print_instr('mov        rbx,rax')
        
        print_instr('mov       rax,  %s'%(convert_var(stmt1[1])))
    elif is_array(stmt1[1]):
        mov_array_to_rax(stmt1[1])
        print_instr('mov        rbx,  %s'%(convert_var(stmt1[2])))
    else:
        print_instr('mov        rax,  %s'%(convert_var(stmt1[1])))
        print_instr('mov        rbx,  %s'%(convert_var(stmt1[2])))
    print_instr('cmp        rax,    rbx')

    if stmt1[0] == '>':
        print_instr('jle         else%d'%(count_IF))
        ELSE_stmt.append(count_IF)
    elif stmt1[0] == '<':
        print_instr('jge         else%d'%(count_IF))
        ELSE_stmt.append(count_IF)
    elif stmt1[0] == '==':
        print_instr('jne         else%d'%(count_IF))
        ELSE_stmt.append(count_IF)
    elif stmt1[0] == '!=':
        print_instr('je        else%d'%(count_IF))
        ELSE_stmt.append(count_IF)
    elif stmt1[0] == '>=':
        print_instr('jl        else%d'%(count_IF))
        ELSE_stmt.append(count_IF)
    elif stmt1[0] == '<=':
        print_instr('jg        else%d'%(count_IF))
        ELSE_stmt.append(count_IF)
    temp_count_IFELSE = count_IF
    count_IF+=1
    base_statement(stmt2)
    print_instr('jmp      nextInstr%d'%(temp_count_IFELSE))

def else_statement(stmt):
    print_instr('else%s:'%(ELSE_stmt[len(ELSE_stmt)-1]))
    base_statement(stmt)
    print_instr('nextInstr%s:'%(ELSE_stmt[len(ELSE_stmt)-1]))
    ELSE_stmt.pop(len(ELSE_stmt)-1)



def declar_var(stmt):
    if not type(stmt) is tuple:
        var_name = stmt
        val = 0
    elif stmt[0] == 'assign-value':
        var_name = stmt[1]
        val = stmt[2]
    if is_define_not_duplicate(var_name):
        var_list.append(var_name)        
        if not '0x' in str(val):
            data_list.append("       %s     dq      %d"%(var_name,val))
        else:
            hex_list.append(var_name)
            data_list.append("       %s     dq      %s"%(var_name,val))
        


def loop_statement(num, stmt):
    global count_loop
    global temp
    temp_count = count_loop
    temp = temp_count
    count_loop += 1
    
    print_instr('mov	rcx, '+ str(num))
    print_instr('for'+str(temp_count)+':')
    print_instr('push rcx')
    base_statement(stmt)
    print_instr('pop rcx')
    print_instr('dec rcx')
    print_instr('cmp rcx, 0')
    print_instr('jne for'+str(temp_count))
    print_instr('jmp notbreak'+str(temp_count))
    print_instr('break'+str(temp_count)+':')
    print_instr('pop rcx')
    print_instr('notbreak'+str(temp_count)+':')
    


