# Brincando_com_Compilador_PY
Uma estrutura para um Compliador baseado em python seguindo estrutura - Enum -> Dicionário -> AST Node -> Lexer -> Parser -> Avaliador


# 🚽 Compilador Privada (Linguagem `.bosta`)

Um compilador/interpretador completo construído do zero em Python, com sua própria Análise Léxica, Sintática (AST) e Avaliador. O diferencial? Uma sintaxe 100% customizada e bem-humorada.

## 🛠️ Requisitos
* **Sistema:** Computador (Windows recomendado para o script `.bat`).
* **Python:** Versão 3.x instalada.
* **Dependências:** Não é necessário instalar nenhuma biblioteca externa (utiliza apenas código nativo).

---

## Modos de Executar

### 1. Terminal Interativo (REPL)
A maneira mais fácil de testar a linguagem linha por linha.
1. Dê dois cliques no arquivo `Executar.bat`.
2. O prompt interativo `bostinha>` vai aparecer aguardando seus comandos.
3. Para encerrar o terminal, digite `apertar`.

### 2. Rodar pela IDE
1. Abra o arquivo fonte `Compliador_Privada.Py` na sua IDE favorita (VSCode, PyCharm, etc.).
2. Execute o código diretamente pelo botão de "Run" da sua IDE.

---

## Explicação da Pasta

* `Compliador_Privada.Py`: Arquivo principal em Python onde há toda a programação, motor do compilador e regras da linguagem.
* `Executar.bat`: O executável do nosso programa que abre o terminal de forma rápida.
* `Mijo.bosta`: Arquivo de exemplo que contém o nosso código-fonte (a extensão oficial da linguagem é `.bosta`).

---

## Biblioteca e Sintaxe

> **Aviso:** Fora qualquer um dos nomes listados abaixo, o compilador tratará a palavra digitada como uma **variável comum**.

### Comandos Reservados
| Ação / Tradução | Comando em `.bosta` |
| :--- | :--- |
| `if` | `POSSIVELDIARREIA` |
| `then` | `DEUDIARREIA` |
| `else` | `NUMSAIU` |
| `end` | `DESCARGA` |
| `print` | `FOTOMERDA` |
| `var` | `BOSTAMOLE` |
| Atribuição (`=`) | `RECEBE` |

### Operadores Matemáticos
| Símbolo | Comando em `.bosta` |
| :---: | :--- |
| `+` | `CAGARMAIS` |
| `-` | `CAGARMENOS` |
| `*` | `MEGADIARREIA` |
| `/` | `SEGURARMERDA` |
| `^` | `PICA` |
| `>` | `CAGOMAIOR` |
| `<` | `CAGOMENOR` |

### Operadores Lógicos e Agrupamento
| Símbolo | Comando em `.bosta` |
| :---: | :--- |
| `==` | `MERDAIGUAL` |
| `and` | `CAGUEIECAGUEI?` |
| `or` | `CAGUEIOUCAGUEI` |
| `not` | `NAOCAGUEI` |
| `(` | `ABRECU` |
| `)` | `FECHACU` |

### Funções Customizadas Especiais
* **`CONTADOR`**: Soma `+1` ao valor de uma variável (Ex: `CONTADOR x`).
* **`%%`** (Quíntuplo): Multiplica os dois valores por 5 e depois os multiplica entre si. Ex: `x %% y` é o mesmo que `(x * 5) * (y * 5)`.

### Números
Os números arábicos puros não existem nesta linguagem. Use o vocabulário abaixo:
| Número | Valor em `.bosta` | Número | Valor em `.bosta` |
| :---: | :--- | :---: | :--- |
| **0** | `Sofia` | **5** | `Renoir` |
| **1** | `Gustave` | **6** | `Verso` |
| **2** | `Maelle` | **7** | `Aline` |
| **3** | `Lune` | **8** | `Monoco` |
| **4** | `Sciel` | **9** | `Esquie` |

---

## Exemplos de Execução

### Casos Corretos (Sucesso)

**Exemplo 1: Uso do CONTADOR**
```text
BOSTAMOLE x RECEBE Gustave 
CONTADOR x 
CONTADOR x 
FOTOMERDA x
```
**Resultado esperado: >>> [SAÍDA DO COMPILADOR_BOSTA]: 3**

**Exemplo 2: Operador Quíntuplo (%%)**
Lógica: (10 x 5) * (5 x 5) = 50 * 25 = 1250
```text
BOSTAMOLE x RECEBE Maelle 
BOSTAMOLE y RECEBE Gustave 
BOSTAMOLE z RECEBE x %% y 
FOTOMERDA z
```
**Resultado esperado: >>> [SAÍDA DO COMPILADOR_BOSTA]: 50**

**Exemplo 3: Matemática Simples**
 ```text
FOTOMERDA Gustave CAGARMAIS Maelle
```
**Resultado esperado: >>> [SAÍDA DO COMPILADOR_BOSTA]: 3**

**Exemplo 4: Variável e Multiplicação**
```text
BOSTAMOLE x RECEBE Renoir MEGADIARREIA Maelle 
FOTOMERDA x
```

**Resultado esperado: >>> [SAÍDA DO COMPILADOR_BOSTA]: 10**

**Exemplo 5: Condicional (If / Then / Else)**
```text
BOSTAMOLE nota RECEBE Monoco 
POSSIVELDIARREIA nota CAGOMAIOR Renoir DEUDIARREIA FOTOMERDA Gustave NUMSAIU FOTOMERDA Sofia DESCARGA
```
**Resultado esperado: >>> [SAÍDA DO COMPILADOR_BOSTA]: 1**

Casos Errados (Tratamento de Erros)

**Erro 1: Faltando a palavra "THEN" no IF**

```text
POSSIVELDIARREIA Gustave CAGOMAIOR Sofia FOTOMERDA Gustave DESCARGA
```
**Saída Esperada no Terminal: Erro Sintático: Esperado 'DEUDIARREIA', mas encontrou 'FOTOMERDA' (Token 4)**

**Erro 2: Uso de Variável Inexistente**

```text
FOTOMERDA Gustave CAGARMAIS imposto
```
**Saída Esperada no Terminal: Erro Crítico: Erro: Variável 'imposto' não foi definida.**

**Erro 3: Uso de Símbolo Proibido (Números reais ou caracteres especiais)**

```text
BOSTAMOLE valor RECEBE 100 @
```

**Saída Esperada no Terminal: Não não esse Numero/Simbulo Não: 1**
