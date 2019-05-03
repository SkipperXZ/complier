import y
import codegen
import sys
import argparse
import subprocess
import os



if not os.path.isdir("out"):
    path = "out"
    access_rights = 0o755
    try:  
        os.mkdir(path, access_rights)
    except OSError:  
        print ("Creation of the directory %s failed" % path)
    else:  
        print ("Successfully created the directory %s" % path)

parser = argparse.ArgumentParser()

parser.add_argument("input")
args = parser.parse_args()


data =''''''

f = open('out/a.asm', 'w+')

code = open(args.input, 'r').read()
result = y.parse(code)

if result:
    codegen.base_statement(result)
    codegen.print_header(f)
    codegen.print_all_instr(f)

'''
p = subprocess.Popen(['nasm', '-f', 'win64','out/'+args.input+'.asm'])
p.wait()
print('out/'+args.input+'.obj')
p = subprocess.Popen(['gcc', '-m64','out/'+args.input+'.obj'])
p.wait()
print("Complied successfully.")
'''

f.write('ret')
f.close()

b = open('out/run.bat', 'w+')
b.write('''@echo off
nasm -f win64 a.asm
gcc -m64 a.obj
a.exe
pause
''')
b.close


