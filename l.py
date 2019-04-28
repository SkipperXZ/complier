import ply.lex as lex
 
 # List of token names.   This is always required
tokens = (
    'INT64','ARRAY',
    'NAME','NUMBER','STRING',
	'IF','ELSE','BREAK','FOR','DISPLAY',
    'EQUALS', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE','MOD',
	'COMMA','SEMICO',
	'LPAREN','RPAREN','LCB','RCB','LBK','RBK',
	'EQ_OP','NE_OP','GT_OP','LT_OP'
)
RESERVED = {
    "int64": "INT64",
    "if": "IF",
	"else": "ELSE",
	"break": "BREAK",
    "return": "RETURN",
	"for": "FOR",
    "array": "ARRAY",
    "display":"DISPLAY"
}
 # Regular expression rules for simple tokens
t_INT64    = r"int64"
t_IF = r"if"
t_ELSE = r"else"
t_BREAK = r"break"
t_FOR = r"for"
t_ARRAY = r"array"
t_DISPLAY = r"display"
t_STRING = r'\"[a-zA-Z0-9]*\"'
#t_CONST = r'\d+'
t_EQUALS = r'='
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_MOD = r'%'
t_DIVIDE = r'/'
t_COMMA = r'\,'
t_SEMICO = r';'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LCB = r'\{'
t_RCB = r'\}'
t_LBK = r'\['
t_RBK = r'\]'
t_EQ_OP = r'=='
t_NE_OP = r'!='
t_GT_OP = r'>'
t_LT_OP = r'<'
 
 # A regular expression rule with some action code

 
 # Define a rule so we can track line numbers
def t_newline(t):
     r'\n+'
     t.lexer.lineno += len(t.value)

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_NAME(t):
     r'[a-zA-Z_][a-zA-Z0-9_]*'
     t.type = RESERVED.get(t.value, "NAME")
     return t
 # A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'
 # Error handling rule
def t_error(t):
     print("Illegal character '%s'" % t.value[0])
     t.lexer.skip(1)
 
 # Build the lexer
lexer = lex.lex()
 
 
#To use the lexer, you first need to feed it some input text using its input() method. After that, repeated calls to token() produce tokens. The following code shows how this works:

 
 # Test it out

data = '''

'''
 
 # Give the lexer some input
lexer.input(data)
 
 # Tokenize
while True:
     tok = lexer.token()
     if not tok: 
         break      # No more input
     print(tok)
 
#When executed, the example will produce the following output:

