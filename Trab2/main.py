'''
Trabalho desenvolvido para a aula de Compiladores - UFRJ

Analisador léxico e sintático para uma linguagem de expressões aritméticas prefixadas, com os seguintes elementos léxicos:

- Números em hexadecimal (0xABCDEF0123456789)
- Números em decimal
- Operadores: + - * / % ^
- Espaços em branco (espaço, tab, quebras de linha, etc)
- Comentário de linha: //
- Comentário de bloco: /* */

* Entrada: uma expressão aritmética prefixada
* Saida: um número com o resultado da expressão aritmética


Alexandre A. Chamon
116142976
'''

import sys

from lexer import Lexer, TokenType
from myParser import Parser
from interpreter import Interpreter

def main():
    print('Digite \'q\' para sair!')
    while True:
        # Leitura da expressão aritmética prefixada a partir da entrada padrão
        try:
            expression = input()
            if expression == 'q':
                break
        except EOFError as e:
            expression = None
        # expression = sys.stdin.readline()

        # Criação do lexer
        lexer = Lexer(expression)

        # Criação do parser
        parser = Parser(lexer)

        if parser.currentToken:
            if parser.currentToken.tokenType == TokenType.TokEOF:
                print('End of File.')
                break
            try:
                # Análise sintática
                syntax_tree = parser.parse()

                # Criação do interpretador
                interpreter = Interpreter()

                # Avaliação da árvore sintática
                result = interpreter.interpret(syntax_tree)

                # Impressão do resultado
                print("Resultado:", result)
            except Exception as e:
                # Tratamento de erros
                print("Erro:", str(e))


if __name__ == "__main__":
    main()
