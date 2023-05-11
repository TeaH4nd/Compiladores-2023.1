'''
Trabalho desenvolvido para a aula de Compiladores - UFRJ

Analisador léxico para uma linguagem de expressões aritméticas com os seguintes elementos léxicos:

- Números em hexadecimal (0xABCDEF0123456789)
- Números em decimal
- Operadores: + - * / % ^
- Espaços em branco (espaço, tab, quebras de linha, etc)
- Comentário de linha: //
- Comentário de bloco: /* */

Alexandre A. Chamon
116142976
'''

import sys

from lexer import Lexer, TokenType 

# FILENAME = sys.argv[1]
FILENAME = 'input.txt'


if __name__ == "__main__":

    # Criar o lexer
    lexer = Lexer(FILENAME)

    # Analisar todos os tokens
    token = lexer.next()
    while token.tokenType != TokenType.TokEOF:
        print(token)
        token = lexer.next()
    print(token)
