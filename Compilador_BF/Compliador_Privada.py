from enum import Enum
import sys


MEMORIA_GLOBAL = {} 

#memória global para armazenar variáveis e seus valores. É um dicionário onde a chave é o nome da variável e o valor é o valor atribuído a ela.

# ==============================
# ENUM (SEM auto)
# ==============================
class TipoToken(Enum):
    NUMERO_INTEIRO = 1
    IDENTIFICADOR = 2
    SOMA = 3
    SUBTRACAO = 4
    MULTIPLICACAO = 5
    DIVISAO = 6
    POTENCIA = 7
    MAIOR = 8
    MENOR = 9
    IGUAL_IGUAL = 10
    AND = 11
    OR = 12
    NOT = 13
    ABRE_PARENTESES = 14
    FECHA_PARENTESES = 15
    EOF = 16

    IF = 17
    THEN = 18
    ELSE = 19
    END = 20

    PRINT = 21 

    VAR = 22
    ATRIBUICAO = 23

#======= quetão 1 String====
    STRING = 24 

#====== question 3 Função contador======
    FUNCAOCONTADOR = 25

#=========quetão 2 C===============
    QUINTUPLO = 26 




NOMES_CUSTOMIZADOS = {
    TipoToken.IF: "POSSIVELDIARREIA",
    TipoToken.THEN: "DEUDIARREIA",
    TipoToken.ELSE: "NUMSAIU",
    TipoToken.END: "DESCARGA",
    TipoToken.PRINT: "FOTOMERDA",
    TipoToken.VAR: "BOSTAMOLE",
    TipoToken.ATRIBUICAO: "RECEBE",
    TipoToken.SOMA: "CAGARMAIS",
    TipoToken.SUBTRACAO: "CAGARMENOS",
    TipoToken.MULTIPLICACAO: "MEGADIARREIA",
    TipoToken.DIVISAO: "SEGURARMERDA",
    TipoToken.POTENCIA: "PICA",
    TipoToken.MAIOR: "CAGOMAIOR",
    TipoToken.MENOR: "CAGOMENOR",
    TipoToken.IGUAL_IGUAL: "MERDAIGUAL",
    TipoToken.ABRE_PARENTESES: "ABRECU",
    TipoToken.FECHA_PARENTESES: "FECHACU",
    TipoToken.EOF: "FIM DO ARQUIVO",

#Steing 
    TipoToken.STRING: "TEXTO_ENTRE_ASPAS",

# Função contador
    TipoToken.FUNCAOCONTADOR: "CONTADOR",

# Q2
    TipoToken.QUINTUPLO: "%%"



}
# ==============================
# TOKEN E NÓS DA AST 
# ==============================
class Token:
    def __init__(self, tipo, valor=None):
        self.tipo = tipo
        self.valor = valor
    def __repr__(self):
        return f"{self.tipo.name}({self.valor})"

class Number:
    def __init__(self, token):
        self.token = token
        self.valor = token.valor
    def __repr__(self):
        return f"Number({self.valor})"

class Var:
    def __init__(self, token):
        self.token = token
        self.nome = token.valor
    def __repr__(self):
        return f"Var({self.nome})"

class BinOp:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
    def __repr__(self):
        return f"BinOp(left={self.left}, op='{self.op.tipo.name}', right={self.right})"

class UnaryOp:
    def __init__(self, op, right):
        self.op = op
        self.right = right
    def __repr__(self):
        return f"UnaryOp(op='{self.op.tipo.name}', right={self.right})"
    
#============================= if-else ==============================
    
class IfNode:
    def __init__(self, condition, true_branch, false_branch):
        self.condition = condition
        self.true_branch = true_branch
        self.false_branch = false_branch
        
    def __repr__(self):
        return f"IfNode(cond={self.condition}, true={self.true_branch}, false={self.false_branch})"

#=====================================================================
#============================= print ==============================

class PrintNode:
    def __init__(self, expr):
        self.expr = expr
        
    def __repr__(self):
        return f"PrintNode({self.expr})"
    
#=============================== VAR ===============================

class AssignNode:
    def __init__(self, nome, value_node):
        self.nome = nome
        self.value_node = value_node
    def __repr__(self):
        return f"AssignNode({self.nome} = {self.value_node})"
    
#===============sting q1 ============
class StringNode:
    def __init__(self, token):
        self.valor = token.valor
    def __repr__(self):
        return f"StringNode('{self.valor}')"
    
#=============== FUNÇÃO CONTADOR ==============================
class ContadorNode:
    def __init__(self, nome_var):
        self.nome_var = nome_var # Guarda o nome da variável (ex: 'x')
        
    def __repr__(self):
        return f"ContadorNode({self.nome_var}++)"
    


    
# ==============================
# PARSER segundo passo 2º para transformar os tokens em uma árvore de sintaxe abstrata AST 
# ==============================
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.erros = []

    def parse(self): # <- ler várias linhas (statements)
        nodes = []
        while self._current().tipo != TipoToken.EOF:
            node = self._parse_expression()
            nodes.append(node)
        return nodes

    def _current(self):
        # EOF que é sempre o último
        if self.pos >= len(self.tokens):
            return self.tokens[-1] 
        return self.tokens[self.pos]

    def _advance(self):
        # Só avança se não estivermos já no final
        if self.pos < len(self.tokens) - 1:
            self.pos += 1

    def _expect(self, tipo):
        token = self._current()
        if token.tipo != tipo:
            nome_esperado = NOMES_CUSTOMIZADOS.get(tipo, tipo.name)
            nome_encontrado = NOMES_CUSTOMIZADOS.get(token.tipo, token.tipo.name)
            
            self.erros.append(f"Erro Sintático: Esperado '{nome_esperado}', mas encontrou '{nome_encontrado}' (Token {self.pos})")
            self._sincronizar()
            return None # Retorna vazio para a árvore tentar continuar
        self._advance()
        return token

    def _parse_expression(self):
        node = self._parse_and()
        while self._current().tipo == TipoToken.OR:
            op = self._current()
            self._advance()
            right = self._parse_and()
            node = BinOp(node, op, right)
        return node

    def _parse_and(self):
        node = self._parse_compare()
        while self._current().tipo == TipoToken.AND:
            op = self._current()
            self._advance()
            right = self._parse_compare()
            node = BinOp(node, op, right)
        return node

    def _parse_compare(self):
        node = self._parse_term()
        while self._current().tipo in (TipoToken.MAIOR, TipoToken.MENOR, TipoToken.IGUAL_IGUAL):
            op = self._current()
            self._advance()
            right = self._parse_term()
            node = BinOp(node, op, right)
        return node
    
#+++++++++++ erro ++++++
    
    def _sincronizar(self):
        self._advance()
        
        while self._current().tipo != TipoToken.EOF:
            tipo_atual = self._current().tipo
            if tipo_atual in (TipoToken.IF, TipoToken.PRINT):
                return
            self._advance()
    
#------------ aqui mudamos de Associatividade à Esquerda(normal) para Associatividade à Direita (outro lado) -------------------------------------
#para mudar:
    def _parse_term(self):
        node = self._parse_factor()
        while self._current().tipo in (TipoToken.SOMA, TipoToken.SUBTRACAO): #'while'(Esquerda) por uma condicional 'if'(direita)
            op = self._current()
            self._advance()

            right = self._parse_factor() #_parse_factor (esquerda) por _parse_term (direita)
            
            node = BinOp(node, op, right)
        return node
    
#------------------------------------------------------

    def _parse_factor(self):
        node = self._parse_power()
        while self._current().tipo in (TipoToken.MULTIPLICACAO, TipoToken.DIVISAO ,TipoToken.QUINTUPLO): # Q2: Adiciona o operador '%%' como multiplicação
            op = self._current()
            self._advance()
            right = self._parse_power()
            node = BinOp(node, op, right)
        return node

    def _parse_power(self):
        node = self._parse_primary()
        if self._current().tipo == TipoToken.POTENCIA:
            op = self._current()
            self._advance()
            right = self._parse_power()
            return BinOp(node, op, right)
        return node

#---------------------------------------------

    def _parse_primary(self):
        token = self._current()

        if token.tipo == TipoToken.NUMERO_INTEIRO:
            self._advance()
            return Number(token)
        if token.tipo == TipoToken.IDENTIFICADOR:
            self._advance()
            return Var(token)
        if token.tipo == TipoToken.NOT:
            self._advance()
            right = self._parse_primary()
            return UnaryOp(token, right)
        if token.tipo == TipoToken.ABRE_PARENTESES:
            self._advance()
            node = self._parse_expression()
            self._expect(TipoToken.FECHA_PARENTESES)
            return node
        
        if token.tipo == TipoToken.IF:
            self._advance() 
            condition = self._parse_expression() 
            
            self._expect(TipoToken.THEN) 
            true_branch = self._parse_expression() 
            
            self._expect(TipoToken.ELSE) 
            false_branch = self._parse_expression() 
            
            self._expect(TipoToken.END)         
            return IfNode(condition, true_branch, false_branch)
        
        if token.tipo == TipoToken.PRINT:
            self._advance() 
            expr = self._parse_expression() # Lê toda a matemática/lógica que vem depois
            return PrintNode(expr)
        
#=============== String q1 ======================

        if token.tipo == TipoToken.STRING:
            self._advance()
            return StringNode(token)
#==============================================
#===============Função contador q3 =============

        if token.tipo == TipoToken.FUNCAOCONTADOR:
            self._advance()
            
            token_id = self._current()
            if token_id.tipo != TipoToken.IDENTIFICADOR:
                self.erros.append(f"Erro Sintático...")
                self._sincronizar()
                return Number(Token(TipoToken.NUMERO_INTEIRO, "0"))
                
            nome_var = token_id.valor
            self._advance()
            
            return ContadorNode(nome_var) # <--- Tem que ser assim!

#============================================

        
        if token.tipo == TipoToken.VAR:
            self._advance() # Pula 'var'
            
            # Pega o nome da variável
            token_id = self._current()
            if token_id.tipo != TipoToken.IDENTIFICADOR:
                self.erros.append(f"Erro Sintático: Esperado nome da variável, mas encontrou '{token_id.tipo.name}'")
                self._sincronizar()
                return Number(Token(TipoToken.NUMERO_INTEIRO, "0"))
                
            nome_var = token_id.valor
            self._advance() # Pula o nome da variável
            
            self._expect(TipoToken.ATRIBUICAO) # Garante que tem o '='
            valor_expr = self._parse_expression()
            return AssignNode(nome_var, valor_expr)
        
        # Erro customizado para o _parse_primary
        nome_encontrado = NOMES_CUSTOMIZADOS.get(token.tipo, token.tipo.name)
        self.erros.append(f"Erro Sintático: Comando inesperado '{nome_encontrado}' (Token {self.pos})")
        self._sincronizar()
        
        # Retorna um nó numérico falso (zero) apenas para a AST não quebrar e o Parser conseguir continuar
        return Number(Token(TipoToken.NUMERO_INTEIRO, "0"))

# ==============================
# LEXER - Priemiro passo 1º para transformar a string em tokens 
# ==============================
def tokenize(expressao):
    tokens = []
    i = 0
    while i < len(expressao):
        char = expressao[i]
        
        #Ignorar espaços
        if char.isspace():
            i += 1
            continue

#=================== Strings entre aspas ===================

        elif char == '"':
            i += 1 
            texto_string = ""
            while i < len(expressao) and expressao[i] != '"':
                texto_string += expressao[i]
                i += 1
            
            if i >= len(expressao):
                raise Exception("Erro Léxico: Aspas não fechadas!")
                
            tokens.append(Token(TipoToken.STRING, texto_string))
            i += 1 
            continue

#==================================================================
#============================Q2============================
        elif char == '%':
            if i + 1 < len(expressao) and expressao[i + 1] == '%':
                tokens.append(Token(TipoToken.QUINTUPLO, '%%'))
                i += 1 # Pula o segundo '%' para não ler duas vezes
            else:
                raise Exception("Caractere '%' isolado não é reconhecido. Correto: '%%'")
            
#==============================================================
            
        # Ler palavras 
        elif char.isalpha():
            texto = ""
            # Adicionado o '?' para ele conseguir ler a sua palavra 'CAGUEIECAGUEI?' inteira
            while i < len(expressao) and (expressao[i].isalpha() or expressao[i].isdigit() or expressao[i] == '?'):
                texto += expressao[i]
                i += 1

            # --- COMANDOS RESERVADOS ---
            if texto == "POSSIVELDIARREIA": 
                tokens.append(Token(TipoToken.IF, "if"))
            elif texto == "DEUDIARREIA":
                tokens.append(Token(TipoToken.THEN, "then"))
            elif texto == "NUMSAIU":
                tokens.append(Token(TipoToken.ELSE, "else"))
            elif texto == "DESCARGA": 
                tokens.append(Token(TipoToken.END, "end"))
            elif texto == "FOTOMERDA":
                tokens.append(Token(TipoToken.PRINT, "FOTOMERDA"))
            elif texto == "BOSTAMOLE":
                tokens.append(Token(TipoToken.VAR, "var"))

            elif texto == "CONTADOR":
                tokens.append(Token(TipoToken.FUNCAOCONTADOR, "CONTADOR"))
            
            # --- OPERADORES MATEMÁTICOS ---
            elif texto == "CAGARMAIS":
                tokens.append(Token(TipoToken.SOMA, '+'))
            elif texto == "CAGARMENOS":
                tokens.append(Token(TipoToken.SUBTRACAO, '-'))
            elif texto == "MEGADIARREIA":
                tokens.append(Token(TipoToken.MULTIPLICACAO, '*'))
            elif texto == "SEGURARMERDA":
                tokens.append(Token(TipoToken.DIVISAO, '/'))
            elif texto == "PICA":
                tokens.append(Token(TipoToken.POTENCIA, '^'))
            elif texto == "CAGOMAIOR":
                tokens.append(Token(TipoToken.MAIOR, '>'))
            elif texto == "CAGOMENOR":
                tokens.append(Token(TipoToken.MENOR, '<'))

            # --- OPERADORES LÓGICOS E ATRIBUIÇÃO ---
            elif texto == "RECEBE":
                tokens.append(Token(TipoToken.ATRIBUICAO, '='))
            elif texto == "MERDAIGUAL":
                tokens.append(Token(TipoToken.IGUAL_IGUAL, '=='))
            elif texto == "CAGUEIECAGUEI?":
                tokens.append(Token(TipoToken.AND, '&&'))
            elif texto == "CAGUEIOUCAGUE":
                tokens.append(Token(TipoToken.OR, '||'))
            elif texto == "NAOCAGUEI":
                tokens.append(Token(TipoToken.NOT, '!'))

            # --- PARÊNTESES ---
            elif texto == "ABRECU":
                tokens.append(Token(TipoToken.ABRE_PARENTESES, '('))
            elif texto == "FECHACU":
                tokens.append(Token(TipoToken.FECHA_PARENTESES, ')'))

            # --- NÚMEROS (Agora são nomes) ---
            elif texto == "Gustave":
                tokens.append(Token(TipoToken.NUMERO_INTEIRO, '1'))
            elif texto == "Maelle":
                tokens.append(Token(TipoToken.NUMERO_INTEIRO, '2'))
            elif texto == "Lune": 
                tokens.append(Token(TipoToken.NUMERO_INTEIRO, '3'))
            elif texto == "Sciel":
                tokens.append(Token(TipoToken.NUMERO_INTEIRO, '4'))
            elif texto == "Renoir":
                tokens.append(Token(TipoToken.NUMERO_INTEIRO, '5'))
            elif texto == "Verso":
                tokens.append(Token(TipoToken.NUMERO_INTEIRO, '6'))
            elif texto == "Aline":
                tokens.append(Token(TipoToken.NUMERO_INTEIRO, '7'))
            elif texto == "Monoco":
                tokens.append(Token(TipoToken.NUMERO_INTEIRO, '8'))
            elif texto == "Esquie":
                tokens.append(Token(TipoToken.NUMERO_INTEIRO, '9'))
            elif texto == "Sofia":
                tokens.append(Token(TipoToken.NUMERO_INTEIRO, '0'))

            # --- SE NÃO FOR NADA DISSO, É O NOME DE UMA VARIÁVEL COMUM ---

            else:
                tokens.append(Token(TipoToken.IDENTIFICADOR, texto))
            continue

        
        else:
            raise Exception(f"Não não esse Numero/Simbulo Não: {char}")
            
        i += 1
        
    tokens.append(Token(TipoToken.EOF, ""))
    return tokens

def evaluate(node):
    # Se receber uma lista de comandos (script), executa um por um
    if isinstance(node, list):
        ultimo_resultado = None
        for statement in node:
            ultimo_resultado = evaluate(statement)
        return ultimo_resultado

    # Base: Se for um número, retorna como inteiro
    if isinstance(node, Number):
        return int(node.valor)
        
    # Operações Unárias (Ex: ! ou futuramente o sinal de menos -5)
    if isinstance(node, UnaryOp):
        right_val = evaluate(node.right)
        if node.op.tipo == TipoToken.NOT:
            return not right_val  # Retorna True ou False do Python
            
    # Operações Binárias (Dois lados)
    if isinstance(node, BinOp):
        left_val = evaluate(node.left)
        right_val = evaluate(node.right)

        
        # Matemáticas
        if node.op.tipo == TipoToken.SOMA:
            return left_val + right_val
        elif node.op.tipo == TipoToken.SUBTRACAO:
            return left_val - right_val
        elif node.op.tipo == TipoToken.MULTIPLICACAO:
            return left_val * right_val
        elif node.op.tipo == TipoToken.DIVISAO:
            return left_val / right_val
        elif node.op.tipo == TipoToken.POTENCIA:
            return left_val ** right_val # Operador de potência no Python

#====================================q2==================
        #operador NOvo
        elif node.op.tipo == TipoToken.QUINTUPLO:
            return (left_val * 5) * (right_val * 5)
        
#=====================================q2 =======================
            
        # Comparações (Retornam Booleano)
        elif node.op.tipo == TipoToken.MAIOR:
            return left_val > right_val
        elif node.op.tipo == TipoToken.MENOR:
            return left_val < right_val
        elif node.op.tipo == TipoToken.IGUAL_IGUAL:
            return left_val == right_val
            
        # Lógicas
        elif node.op.tipo == TipoToken.AND:
            return left_val and right_val
        elif node.op.tipo == TipoToken.OR:
            return left_val or right_val
        
        # Operação Condicional (If / Else)
    if isinstance(node, IfNode):
        cond_val = evaluate(node.condition)
        if cond_val:
            return evaluate(node.true_branch)
        else:
            return evaluate(node.false_branch)
#=========================================
        # Comando de Print
    if isinstance(node, PrintNode):
        valor_calculado = evaluate(node.expr)
        print(f">>> [SAÍDA DO COMPILADOR_BOSTA]: {valor_calculado}") # Imprime na tela do usuário
        return None
#===========================================

        #função contador
    if isinstance(node, ContadorNode):
        nome_var = node.nome_var
        if nome_var not in MEMORIA_GLOBAL:
            MEMORIA_GLOBAL[nome_var] = 1
        else:
            MEMORIA_GLOBAL[nome_var] += 1
        return MEMORIA_GLOBAL[nome_var]
    
#==================================================
# =========== String q1 =======================
    if isinstance(node, StringNode):
        return str(node.valor)
#=========================================== para o PY
    #var 
    # LER VARIÁVEL: Quando encontrar um nó Var, busca o valor no dicionário
    if isinstance(node, Var):
        if node.nome in MEMORIA_GLOBAL:
            return MEMORIA_GLOBAL[node.nome]
        raise Exception(f"Erro: Variável '{node.nome}' não foi definida.")

    #salva var
    # GUARDAR VARIÁVEL: Quando encontrar um AssignNode, salva no dicionário
    if isinstance(node, AssignNode):
        valor = evaluate(node.value_node)
        MEMORIA_GLOBAL[node.nome] = valor
        return valor # Retorna o valor para o terminal mostrar se quiser
    


    raise Exception(f"Erro no Avaliador: Nó ou operador não suportado.")


#===================


# ==============================
# MOTOR DE EXECUÇÃO E TERMINAL INTERATIVO (REPL)
# ==============================

def rodar_codigo(codigo_fonte):
    try:
        tokens = tokenize(codigo_fonte)
        meu_parser = Parser(tokens)
        arvore = meu_parser.parse()

        if len(meu_parser.erros) > 0:
            print("Erros de Compilação:")
            for erro in meu_parser.erros:
                print("  ->", erro)
        else:
            resultado = evaluate(arvore)
            # Imprime o resultado direto na tela (igual ao terminal do Python)
            if resultado is not None:
                print(resultado)
                
    except Exception as e:
        print(f"Erro Crítico: {e}")


def executar_arquivo(nome_arquivo):
  
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
            codigo_fonte = arquivo.read()
    except FileNotFoundError:
        print(f"Erro: O arquivo '{nome_arquivo}' não foi encontrado.")
        return

    print(f"=== Executando código de: {nome_arquivo} ===\n")
    rodar_codigo(codigo_fonte)


def modo_interativo():

    print("=========================================")
    print("          Terminal Do Bosta              ")
    print("   Digite 'apertar' para descarga.       ")
    print("=========================================\n")
    
    while True:
        try:
            # Fica aguardando o usuário digitar no terminal
            entrada = input("bostinha>")
            
            # Condição de parada
            if entrada.strip().lower() == 'apertar':
                print("Dando descarga...")
                break
                
            # Se o usuário der apenas "Enter" sem digitar nada, ignora
            if not entrada.strip():
                continue
                
            # Envia o que o usuário digitou para o compilador
            rodar_codigo(entrada)
            
        except KeyboardInterrupt:
            # Captura se o usuário apertar Ctrl+C
            print("\nSaindo à força...")
            break


# ==============================
# PONTO DE ENTRADA DO PROGRAMA
# ==============================
if __name__ == "__main__":
    # O sys.argv guarda os argumentos do terminal.
    # O índice [0] é o próprio nome do script (A-Compliador-bat.py).
    # O índice [1] seria o nome do arquivo, se existir.
    
    if len(sys.argv) >= 2:
        # Se passou um arquivo (ex: teste.garrafa), lê o arquivo
        executar_arquivo(sys.argv[1])
    else:
        # Se não passou nenhum arquivo, abre o terminal interativo!
        modo_interativo()