import sys

from lexer import Lexer
from parser import Parser
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

        if parser.current_token:
            if parser.current_token.token_type == TokenType.TokEOF:
                print('End of File.')
                break
            try:
                # Análise sintática
                syntax_tree = parser.parse()

                # Criação do interpretador
                interpreter = Interpreter()

                # Avaliação da árvore sintática
                interpreter.interpret(syntax_tree)
            except Exception as e:
                # Tratamento de erros
                print("Erro:", str(e))


if __name__ == "__main__":
    main()
