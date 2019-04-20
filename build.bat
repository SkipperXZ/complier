@echo off
flex l.l
bison -d y.y
gcc lex.yy.c y.tab.c
@pause