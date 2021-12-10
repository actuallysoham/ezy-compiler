from ply import lex
from ply import yacc
import sys
import pprint

reserved = {
    'begin' : 'BEGIN_KW',
    'end' : 'END_KW',
    'var' : 'VAR_KW',
    'proc' : 'PROC_KW',
    'in' : 'IN_KW',
    'out' : 'OUT_KW',
    'inout' : 'INOUT_KW',
    'return' : 'RET_KW',
    'exit' : 'EXIT_KW',
    'if' : 'IF_KW',
    'goto' : 'GOTO_KW',
    'read' : 'READ_KW',
    'print' : 'PRINT_KW',
    'println' : 'PRINTLN_KW',
    'call' : 'CALL_KW',
    'return': 'RETURN_KW'
}

tokens = [
    'NUM',
    'ID',
    'STRING',
    'LPAR',
    'RPAR',
    'SEMICOL',
    'COLON',
    'COMMA',
    'EQUALS',
    'LTR',
    'GTR',
    'LEQ',
    'GEQ',
    'NEQ',
    'PLUS',
    'MINUS',
    'TIMES',
    'FW_SLASH',
    # 'QUOTE',
    # 'UNDERSCORE',
    # 'NEWLINE',
    # 'LABEL',
 ] + list(reserved.values())

t_LPAR = r'\('
t_RPAR = r'\)'
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_FW_SLASH  = r'/'
t_SEMICOL = r';'
t_COLON = r':'
t_COMMA = r','
t_EQUALS = r'='
t_LTR = r'<'
t_GTR = r'>'
t_LEQ = r'<='
t_GEQ = r'>='
t_NEQ = r'<>'
# t_QUOTE = r'"'
# t_UNDERSCORE = r'_'
# t_ignore_COMMENT = r'%[^\n]*'

def t_COMMENT(t):
    r'%[^\n]*'
    pass

def t_ID(t):
    r'[a-zA-Z][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')
    t.value = t.value
    return t
  
# def t_LABEL(t):
#     r'[a-zA-Z_0-9]+'
#     t.type = 'LABEL'
#     return t

def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

# regex for strings that don't contain quotes
def t_STRING(t):
    r'"[^"\n]*"'
    t.value = t.value[1:-1]
    return t

def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = ' \t'

lexer = lex.lex(debug=True)

variable_list = {}
procedure_list = {}
label_list = {}

def p_prog(p):
    'prog : vardecls procdecls BEGIN_KW stmtlist END_KW'
    print("Program Initialized")

def p_vardecls(p): # vardecls vardecl changed to vardecl vardecls to fix ambiguity? 
    """vardecls : vardecl vardecls
                | empty"""
    print("Variable Declarations")
    p[0] = p[1]

    # pprint.pprint(variable_list)

def p_vardecl(p):
    'vardecl : VAR_KW varlist SEMICOL'
    variable_list = p[2]
    print("Variable Declaration")

#TODO: handle duplicate variable declarations
#TODO: scope
def p_varlist(p):
    """varlist : ID COMMA varlist
               | ID"""
    print("New Variable")
    p[0] = list()
    p[0].append(p[1])
    if len(p) == 4:
        p[0].extend(p[3])
    variable_list[p[1]] = {'status': 'initialized', 'value': None}

def p_procdecls(p):
    """procdecls : procdecl procdecls 
                 | empty"""
    print("Procedure Declarations")
    p[0] = p[1]

def p_procdecl(p):
    'procdecl : PROC_KW ID LPAR paramlist RPAR vardecls pstmtlist'
    print("New Procedure")
    procedure_list[p[2]] = {'params': p[4], 'vardecls': p[6], 'pstmtlist': p[7]}

def p_paramlist(p):
    """paramlist : tparamlist
                 | empty"""
    print("Parameter List")
    p[0] = p[1]

def p_tparamlist(p):
    """tparamlist : param COMMA tparamlist
                  | param"""
    p[0] = list()
    p[0].append(p[1])
    if len(p) == 4:
        p[0].extend(p[3])

def p_param(p):
    """param : mode ID"""
    print("New Parameter")
    p[0] = {'mode': p[1], 'name': p[2]}

def p_mode(p):
    """mode : IN_KW
            | OUT_KW
            | INOUT_KW"""
    p[0] = p[1]

def p_pstmtlist(p):
    """pstmtlist : pstmt pstmtlist
                 | pstmt"""
    p[0] = list()
    p[0].append(p[1])
    if len(p) == 3:
        p[0].extend(p[2])

def p_stmtlist(p):
    """stmtlist : mstmt stmtlist
                | mstmt"""
    p[0] = list()
    p[0].append(p[1])
    if len(p) == 3:
        p[0].extend(p[2])

def p_pstmt(p):
    """pstmt : dlabel
             | stmt SEMICOL
             | RETURN_KW SEMICOL"""
    p[0] = p[1]

def p_mstmt(p):
    """mstmt : dlabel
             | stmt SEMICOL"""
    p[0] = p[1]

def p_dlabel(p):
    'dlabel : ID COLON'
    print("New Label")
    label_list[p[1]] = {'status': 'initialized', 'value': p.lineno(1)+1}

def p_stmt(p):
    """stmt : assign
            | condjump
            | jump
            | readstmt
            | printstmt
            | callstmt
            | EXIT_KW"""
    print("New Statement")
    p[0] = p[1]

def p_assign(p):
    """assign : ID EQUALS opd arithop opd"""
    print("Assignment")
    if p[1] in variable_list:
        if p[4] == '+':
            variable_list[p[1]]['value'] = p[3] + p[5]
        elif p[4] == '-':
            variable_list[p[1]]['value'] = p[3] - p[5]
        elif p[4] == '*':
            variable_list[p[1]]['value'] = p[3] * p[5]
        elif p[4] == '/':
            variable_list[p[1]]['value'] = p[3] / p[5]
        else:
            print("Invalid Operator")
    else:
        print("assign", f"Variable {p[1]} not declared")

def p_opd(p):
    """opd : ID"""
    print("Operand (ID)")
    if p[1] in variable_list:
        p[0] = variable_list[p[1]]['value']
    else:
        print("opd", f"Variable {p[1]} not declared")
        p[0] = -1

def p_opd_2(p):
    """opd : NUM"""
    print("Operand (NUM)")
    p[0] = p[1]

# TODO: replace all lineno modifications with AST syntax
def p_condjump(p):
    """condjump : IF_KW ID cmpop ID jump"""
    print("Conditional Jump")
    if p[2] in variable_list:
        if p[4] == '=':
            if variable_list[p[2]]['value'] == variable_list[p[5]]['value']:
                print("Jumping to label")
        elif p[4] == '<':
            if variable_list[p[2]]['value'] < variable_list[p[5]]['value']:
                print("Jumping to label")
        elif p[4] == '>':
            if variable_list[p[2]]['value'] > variable_list[p[5]]['value']:
                print("Jumping to label")
        elif p[4] == '<=':
            if variable_list[p[2]]['value'] <= variable_list[p[5]]['value']:
                print("Jumping to label")
        elif p[4] == '>=':
            if variable_list[p[2]]['value'] >= variable_list[p[5]]['value']:
                print("Jumping to label")
        elif p[4] == '<>':
            if variable_list[p[2]]['value'] != variable_list[p[5]]['value']:
                print("Jumping to label")
        else:
            print("Invalid Operator")
    else:
        print("condjump", "Variable not declared")



def p_jump(p):
    """jump : GOTO_KW ID"""
    print("Jump")
    # p.lexer.lineno = label_list[p[2]]['value'] - 1
    p[0] = {'type': 'jump', 'label': p[2]}
    print(p[0])

def p_readstmt(p):
    """readstmt : READ_KW ID"""
    print("Read Statement")
    if p[2] in variable_list:
        variable_list[p[2]]['value'] = int(input())
    else:
        print("read", "Variable not declared")

def p_printstmt(p):
    """printstmt : PRINT_KW printarg
                 | PRINTLN_KW"""
    print("Print Statement")
    if p[1] == 'print':
        print(p[2])
    else:
        print("")

def p_printarg_1(p):
    """printarg : ID"""
    print("Print Argument")
    if p[1] in variable_list:
        print(variable_list[p[1]]['value'])
    else:
        print("printarg", "Variable not declared")

def p_printarg_2(p):
    """printarg : STRING"""
    print("Print Argument")
    print(p[1].strip('"'))

def p_callstmt(p):
    "callstmt : CALL_KW ID LPAR arglist RPAR"
    print("Call Statement")
    if p[2] in procedure_list:
        if len(p[4]) == len(procedure_list[p[2]]['params']):
            procedure_list[p[2]]['args'] = p[4]
            # for i in range(len(p[4])):
            #     if p[4][i] in variable_list:
            #         procedure_list[p[2]]['arg_list'][i] = variable_list[p[4][i]]['value']
            #     else:
            #         print("call", "Variable not declared")
            # procedure_list[p[2]]['function'](*procedure_list[p[2]]['arg_list'])
        else:
            print("Invalid number of arguments")
    else:
        print("Function not declared")
    
def p_arglist(p):
    """arglist : targlist
               | empty"""
    print("Argument List")
    p[0] = p[1]

def p_targlist(p):
    """targlist : ID COMMA targlist
                | ID"""
    p[0] = list()
    p[0].append(p[1])
    if len(p) == 4:
        p[0].extend(p[3])

def p_cmpop(p):
    """cmpop : EQUALS
             | LTR
             | GTR
             | LEQ
             | GEQ
             | NEQ"""
    p[0] = p[1]

def p_arithop(p):
    """arithop : PLUS
               | MINUS
               | TIMES
               | FW_SLASH"""
    p[0] = p[1]

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    print("Syntax error", p)

parser = yacc.yacc(debug=True, start='prog')

with open(sys.argv[1], 'r') as f:
    data = f.read()

yacc.parse(data)

pprint.pprint(variable_list)
pprint.pprint(procedure_list)