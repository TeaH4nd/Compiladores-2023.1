from nodes import *
from lexer import OpType


class Interpreter:
    def __init__(self):
        self.variables = {}

    def interpret(self, node):
        if isinstance(node, PrintCommandNode):
            return self.interpret_print(node)
        elif isinstance(node, VariableDeclarationNode):
            return self.interpret_var_declaration(node)
        elif isinstance(node, VariableAssignmentNode):
            return self.interpret_assignment(node)
        elif isinstance(node, WhileLoopNode):
            return self.interpret_while(node)
        elif isinstance(node, IfStatementNode):
            return self.interpret_if(node)
        elif isinstance(node, ElseStatementNode):
            return self.interpret_block(node)
        elif isinstance(node, NumberNode):
            return node.value
        elif isinstance(node, BinaryOperationNode):
            return self.interpret_binary_operation(node)

    def interpret_print(self, node):
        value = self.interpret(node.expression)
        print(value)

    def interpret_var_declaration(self, node):
        var_name = node.variable_name
        var_value = self.interpret(node.expression)
        self.variables[var_name] = var_value

    def interpret_assignment(self, node):
        var_name = node.variable_name
        var_value = self.interpret(node.expression)
        self.variables[var_name] = var_value

    def interpret_while(self, node):
        while self.interpret(node.condition):
            self.interpret(node.block)

    def interpret_if(self, node):
        if self.interpret(node.condition):
            self.interpret(node.block)
        elif node.else_block:
            self.interpret(node.else_block)

    def interpret_block(self, node):
        for cmd in node.commands:
            self.interpret(cmd)

    def interpret_binary_operation(self, node):
        left_value = self.interpret(node.left)
        right_value = self.interpret(node.right)

        if node.operator == '+':
            return left_value + right_value
        elif node.operator == '-':
            return left_value - right_value
        elif node.operator == '*':
            return left_value * right_value
        elif node.operator == '/':
            return left_value / right_value
        elif node.operator == '^':
            return left_value ** right_value
        elif node.operator == '==':
            return int(left_value == right_value)
        elif node.operator == '!=':
            return int(left_value != right_value)
        elif node.operator == '<':
            return int(left_value < right_value)
        elif node.operator == '>':
            return int(left_value > right_value)
        elif node.operator == '<=':
            return int(left_value <= right_value)
        elif node.operator == '>=':
            return int(left_value >= right_value)
        elif node.operator == 'and':
            return int(left_value and right_value)
        elif node.operator == 'or':
            return int(left_value or right_value)
        else:
            raise Exception(f'Operador inválido: {node.operator}')
