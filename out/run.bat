@echo off
nasm -f win64 a.asm
gcc -m64 a.obj
a.exe
pause
