import sys
import re
from datetime import datetime
import ply.lex as lex
import ply.yacc as yacc

#
# --- 1) AST NODES ------------------------------------------------------------
#

class Number:
    def __init__(self, value): self.value = value

class Var:
    def __init__(self, name): self.name = name

class BinOp:
    def __init__(self, op, left, right):
        self.op, self.left, self.right = op, left, right

class UnaryOp:
    def __init__(self, op, expr):
        self.op, self.expr = op, expr

class Assign:
    def __init__(self, name, expr):
        self.name, self.expr = name, expr

class Return:
    def __init__(self, expr):
        self.expr = expr

class ExprStmt:
    def __init__(self, expr):
        self.expr = expr

class If:
    def __init__(self, cond, then_body):
        self.cond, self.then_body = cond, then_body

class While:
    def __init__(self, cond, body):
        self.cond, self.body = cond, body

class FuncDecl:
    def __init__(self, name, params, body):
        self.name, self.params, self.body = name, params, body

class FuncCall:
    def __init__(self, name, args):
        self.name, self.args = name, args

class Greet:
    def __init__(self, typ):
        # typ in {'bom_dia','boa_tarde','boa_noite'}
        self.typ = typ

class ReturnException(Exception):
    def __init__(self, value):
        self.value = value

#
# --- 2) LEXER ---------------------------------------------------------------
#

tokens = (
    # saudações
    'BOM_DIA', 'BOA_TARDE', 'BOA_NOITE',
    # controle
    'IF', 'ELSE', 'WHILE',
    # booleanos
    'TRUE', 'FALSE',
    # fim de comando
    'SEMI',
    # agrupamento
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',
    # operadores
    'PLUS', 'MINUS', 'MUL', 'DIV',
    'GE', 'LE', 'EQ', 'NE', 'GT', 'LT',
    'ASSIGN',
    # funções
    'FUNCTION', 'RETURN',
    # separador em listas
    'COMMA',
    # unário
    'UMINUS',
    # valores
    'NUMBER', 'ID',
)

t_ignore = ' \t\r\n'

def t_COMMENT_LINE(t):
    r'entre\ nos[^\n]*'
    pass

def t_COMMENT_BLOCK(t):
    r'/\*[\s\S]*?\*/'
    pass

def t_COMMENT_HASH(t):
    r'\#.*'
    pass

def t_SEMI(t):
    r',\s*ta ligado\??'
    return t

def t_LPAREN(t):
    r'\('
    return t

def t_RPAREN(t):
    r'\)'
    return t

def t_LBRACE(t):
    r'\{'
    return t

def t_RBRACE(t):
    r'\}'
    return t

def t_PLUS(t):
    r'maizi'
    return t

def t_MINUS(t):
    r'-'
    return t

def t_MUL(t):
    r'veiz'
    return t

def t_DIV(t):
    r'mei'
    return t

def t_GE(t):
    r'mais\ que\ uma\ ruma\ de'
    return t

def t_LE(t):
    r'menos\ que\ uma\ ruma\ de'
    return t

def t_EQ(t):
    r'se\ for'
    return t

def t_NE(t):
    r'pior\ que\ nao\ e'
    return t

def t_GT(t):
    r'mais\ maior\ que'
    return t

def t_LT(t):
    r'mais\ menor\ que'
    return t

def t_ASSIGN(t):
    r'eh'
    return t

def t_FUNCTION(t):
    r'funcao'
    return t

def t_RETURN(t):
    r'retorna'
    return t

def t_COMMA(t):
    r','
    return t

def t_UMINUS(t):
    r'serasa'
    t.type = 'UMINUS'
    return t

def t_TRUE(t):
    r'bitcoin'
    t.value = 1.0
    return t

def t_FALSE(t):
    r'nao_bitcoin'
    t.value = 0.0
    return t

def t_BOM_DIA(t):
    r'\bbom\s+dia\b'
    return t

def t_BOA_TARDE(t):
    r'\bboa\s+tarde\b'
    return t

def t_BOA_NOITE(t):
    r'\bboa\s+noite\b'
    return t

def t_IF(t):
    r'veja\ bem'
    return t

def t_ELSE(t):
    r'olha\ só'
    return t

def t_WHILE(t):
    r'so\ faz'
    return t

def t_NUMBER(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9]*'
    return t

def t_error(t):
    print(f"Illegal character {t.value[0]!r}")
    t.lexer.skip(1)

lexer = lex.lex(reflags=re.IGNORECASE)

#
# --- 3) PARSER --------------------------------------------------------------
#

precedence = (
    ('right', 'ASSIGN'),
    ('right', 'UMINUS'),
    ('left', 'GT', 'LT', 'GE', 'LE', 'EQ', 'NE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MUL', 'DIV'),
)

def p_program(p):
    'programa : stmt_list'
    p[0] = p[1]

def p_stmt_list_rec(p):
    'stmt_list : stmt_list statement'
    p[0] = p[1] + [p[2]]

def p_stmt_list_empty(p):
    'stmt_list : '
    p[0] = []

# Saudação como statement (com SEMI)
def p_statement_greet_bom(p):
    'statement : BOM_DIA SEMI'
    p[0] = Greet('bom_dia')

def p_statement_greet_tarde(p):
    'statement : BOA_TARDE SEMI'
    p[0] = Greet('boa_tarde')

def p_statement_greet_noite(p):
    'statement : BOA_NOITE SEMI'
    p[0] = Greet('boa_noite')

# Declaração de função
def p_statement_func_decl(p):
    'statement : FUNCTION ID LPAREN param_list RPAREN LBRACE stmt_list RBRACE SEMI'
    p[0] = FuncDecl(p[2], p[4], p[7])

# Return dentro de função
def p_statement_return(p):
    'statement : RETURN expr SEMI'
    p[0] = Return(p[2])

# If / While
def p_statement_if(p):
    'statement : IF LPAREN expr RPAREN LBRACE stmt_list RBRACE'
    p[0] = If(p[3], p[6])

def p_statement_while(p):
    'statement : WHILE LPAREN expr RPAREN LBRACE stmt_list RBRACE'
    p[0] = While(p[3], p[6])

# Expressão ou atribuição seguida de SEMI
def p_statement_expr(p):
    'statement : expr SEMI'
    p[0] = ExprStmt(p[1])

# Lista de parâmetros
def p_param_list_empty(p):
    'param_list : '
    p[0] = []

def p_param_list_one(p):
    'param_list : ID'
    p[0] = [p[1]]

def p_param_list_rec(p):
    'param_list : param_list COMMA ID'
    p[0] = p[1] + [p[3]]

# Lista de argumentos
def p_arg_list_empty(p):
    'arg_list : '
    p[0] = []

def p_arg_list_one(p):
    'arg_list : expr'
    p[0] = [p[1]]

def p_arg_list_rec(p):
    'arg_list : arg_list COMMA expr'
    p[0] = p[1] + [p[3]]

# Expressões
def p_expr_assign(p):
    'expr : ID ASSIGN expr'
    p[0] = Assign(p[1], p[3])

def p_expr_binop(p):
    '''
    expr : expr PLUS expr
         | expr MINUS expr
         | expr MUL expr
         | expr DIV expr
         | expr GE expr
         | expr LE expr
         | expr GT expr
         | expr LT expr
         | expr EQ expr
         | expr NE expr
    '''
    p[0] = BinOp(p[2], p[1], p[3])

def p_expr_uminus(p):
    'expr : MINUS expr %prec UMINUS'
    p[0] = UnaryOp('-', p[2])

def p_expr_group(p):
    'expr : LPAREN expr RPAREN'
    p[0] = p[2]

def p_expr_number(p):
    'expr : NUMBER'
    p[0] = Number(p[1])

def p_expr_funccall(p):
    'expr : ID LPAREN arg_list RPAREN'
    p[0] = FuncCall(p[1], p[3])

def p_expr_id(p):
    'expr : ID'
    p[0] = Var(p[1])

def p_error(p):
    if p:
        print(f"Syntax error at {p.value!r}")
    else:
        print("Syntax error at EOF")

parser = yacc.yacc()

#
# --- 4) INTERPRETER ---------------------------------------------------------
#

def eval_node(node, global_env, local_env, functions):
    if isinstance(node, Number):
        return node.value
    if isinstance(node, Var):
        if node.name in local_env:
            return local_env[node.name]
        if node.name in global_env:
            return global_env[node.name]
        raise NameError(f"Variável não definida: {node.name}")
    if isinstance(node, Assign):
        val = eval_node(node.expr, global_env, local_env, functions)
        global_env[node.name] = val
        return val
    if isinstance(node, BinOp):
        a = eval_node(node.left,  global_env, local_env, functions)
        b = eval_node(node.right, global_env, local_env, functions)
        op = node.op
        if   op == 'maizi':               return a + b
        elif op == '-':                   return a - b
        elif op == 'veiz':                return a * b
        elif op == 'mei':                 return a / b if b != 0 else (_ for _ in ()).throw(ZeroDivisionError("não pode dividir por 0"))
        elif op == 'mais que uma ruma de':return 1.0 if a >= b else 0.0
        elif op == 'menos que uma ruma de':return 1.0 if a <= b else 0.0
        elif op == 'mais maior que':     return 1.0 if a >  b else 0.0
        elif op == 'mais menor que':     return 1.0 if a <  b else 0.0
        elif op == 'se for':             return 1.0 if a == b else 0.0
        elif op == 'pior que nao e':     return 1.0 if a != b else 0.0
        else:
            raise RuntimeError(f"Operador desconhecido {op!r}")
    if isinstance(node, UnaryOp):
        return -eval_node(node.expr, global_env, local_env, functions)
    if isinstance(node, FuncCall):
        if node.name not in functions:
            raise NameError(f"Função não definida: {node.name}")
        decl = functions[node.name]
        if len(node.args) != len(decl.params):
            raise TypeError(f"{node.name} espera {len(decl.params)} args, recebeu {len(node.args)}")
        vals = [eval_node(arg, global_env, local_env, functions) for arg in node.args]
        new_loc = dict(zip(decl.params, vals))
        try:
            for stmt in decl.body:
                eval_stmt(stmt, global_env, new_loc, functions)
        except ReturnException as ret:
            return ret.value
        return None
    raise RuntimeError(f"Não consegui avaliar nó: {node!r}")

def eval_stmt(stmt, global_env, local_env, functions):
    if isinstance(stmt, ExprStmt):
        val = eval_node(stmt.expr, global_env, local_env, functions)
        if val is not None:
            print(val)
        return
    if isinstance(stmt, If):
        cond = eval_node(stmt.cond, global_env, local_env, functions)
        if cond == 1.0:
            for s in stmt.then_body:
                eval_stmt(s, global_env, local_env, functions)
        return
    if isinstance(stmt, While):
        while eval_node(stmt.cond, global_env, local_env, functions) == 1.0:
            for s in stmt.body:
                eval_stmt(s, global_env, local_env, functions)
        return
    if isinstance(stmt, Return):
        val = eval_node(stmt.expr, global_env, local_env, functions)
        raise ReturnException(val)
    if isinstance(stmt, FuncDecl):
        return
    if isinstance(stmt, Greet):
        agora = datetime.now()
        h = agora.hour
        if stmt.typ == 'bom_dia':
            if 5 <= h < 12:
                print("Bom dia, está coerente com o horário.")
            else:
                print(f"Saudação incorreta. Hora atual: {agora:%H:%M}")
                sys.exit(1)
        elif stmt.typ == 'boa_tarde':
            if 12 <= h < 18:
                print("Boa tarde, está coerente com o horário.")
            else:
                print(f"Saudação incorreta. Hora atual: {agora:%H:%M}")
                sys.exit(1)
        elif stmt.typ == 'boa_noite':
            if (18 <= h <= 23) or (0 <= h < 5):
                print("Boa noite, está coerente com o horário.")
            else:
                print(f"Saudação incorreta. Hora atual: {agora:%H:%M}")
                sys.exit(1)
        return
    raise RuntimeError(f"Statement desconhecido: {stmt!r}")

#
# --- 5) MAIN: SCRIPT vs REPL -----------------------------------------------
#

if __name__ == '__main__':
    global_env = {}
    functions  = {}

    if len(sys.argv) > 1:
        # Executa todo o script do arquivo
        filename = sys.argv[1]
        with open(filename, 'r', encoding='utf-8') as f:
            data = f.read()
        stmts = parser.parse(data, lexer=lexer)
        for st in stmts:
            if isinstance(st, FuncDecl):
                functions[st.name] = st
        for st in stmts:
            if not isinstance(st, FuncDecl):
                eval_stmt(st, global_env, {}, functions)
    else:
        # Modo interativo
        print("Digite expressões (termine cada com ', ta ligado?').")
        print("Para sair, digite 'exit' ou Ctrl+D.")
        while True:
            try:
                data = input("> ")
            except EOFError:
                break
            if not data or data.strip().lower() == 'exit':
                break
            stmts = parser.parse(data + "\n", lexer=lexer)
            for st in stmts:
                if isinstance(st, FuncDecl):
                    functions[st.name] = st
            for st in stmts:
                if not isinstance(st, FuncDecl):
                    eval_stmt(st, global_env, {}, functions)
        print("Tchau!")
 