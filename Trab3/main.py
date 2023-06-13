import sys

from lexer import Lexer, TokenType
from myParser import Parser
from interpreter import Interpreter

def main():
    print('Digite \'q\' para sair!')
    # Criação do interpretador
    interpreter = Interpreter()
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

                # Avaliação da árvore sintática
                interpreter.interpret(syntax_tree)
            except Exception as e:
                # Tratamento de erros
                print("Erro:", str(e))


if __name__ == "__main__":
    main()
