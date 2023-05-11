from lexer import Lexer
from myParser import Parser
from interpreter import Interpreter

def main():
    # Leitura da expressão aritmética prefixada a partir da entrada padrão
    expression = input("Digite a expressão aritmética: ")

    # Criação do lexer
    lexer = Lexer(expression)

    # Criação do parser
    parser = Parser(lexer)

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
