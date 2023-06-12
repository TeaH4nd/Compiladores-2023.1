'''
Trabalho desenvolvido para a aula de Compiladores - UFRJ

Analisador léxico e sintático para uma linguagem de expressões aritméticas prefixadas, com os seguintes elementos léxicos:

- Números em hexadecimal (0xABCDEF0123456789)
- Números em decimal
- Operadores: + - * / % ^
- Espaços em branco (espaço, tab, quebras de linha, etc)
- Comentário de linha: //
- Comentário de bloco: /* */

Alexandre A. Chamon
116142976
'''

from myParser import BinaryOperationNode, NumberNode

class Interpreter:
    def interpret(self, node):
        if isinstance(node, BinaryOperationNode):
            return self.evaluate_binary_operation(node)
        elif isinstance(node, NumberNode):
            return node.value

    def evaluate_binary_operation(self, node):
        operator = node.operator
        left_value = self.interpret(node.left)
        right_value = self.interpret(node.right)

        if operator.name == 'OpSum':
            return left_value + right_value
        elif operator.name == 'OpMinus':
            return left_value - right_value
        elif operator.name == 'OpMult':
            return left_value * right_value
        elif operator.name == 'OpDiv':
            return left_value / right_value
        elif operator.name == 'OpMod':
            return left_value % right_value
        elif operator.name == 'OpPow':
            return left_value ** right_value
        else:
            raise Exception(f'Invalid operator: {operator}')
