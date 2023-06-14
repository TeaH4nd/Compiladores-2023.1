from nodes import *
from lexer import OpType


class Interpreter:
    def __init__(self):
        self.variables = {}

    def interpret(self, node):
        if isinstance(node, list):
            for n in node:
                return self.verify_node(n)
        else:
            return self.verify_node(node)
                
    def verify_node(self, node):
        if isinstance(node, PrintCommandNode):
            return self.interpret_print(node)
        elif isinstance(node, VariableNode):
            return self.interpret_var(node)
        elif isinstance(node, VariableDeclarationNode):
            return self.interpret_var_declaration(node)
        elif isinstance(node, VariableAssignmentNode):
            return self.interpret_assignment(node)
        elif isinstance(node, WhileLoopNode):
            return self.interpret_while(node)
        elif isinstance(node, IfStatementNode):
            return self.interpret_if(node)
        # elif isinstance(node, ElseStatementNode):
        #     return self.interpret_else(node)
        elif isinstance(node, NumberNode):
            return node.value
        elif isinstance(node, BinaryOperationNode):
            return self.interpret_binary_operation(node)
        elif isinstance(node, UnaryOperationNode):
            return self.interpret_unary_operation(node)
        else:
            raise Exception("Invalid node type")

    def interpret_print(self, node):
        value = self.interpret(node.expression)
        print(value)

    def interpret_var(self, node):
        return self.variables[node.name]

    def interpret_var_declaration(self, node):
        var_name = node.name
        var_value = self.interpret(node.expression)
        self.variables[var_name] = var_value

    def interpret_assignment(self, node):
        var_name = node.name
        var_value = self.interpret(node.expression)
        self.variables[var_name] = var_value

    def interpret_while(self, node):
        while self.interpret(node.condition):
            self.interpret(node.block)

    def interpret_if(self, node):
        if node.condition:
            if self.interpret(node.condition):
                self.interpret(node.block)
            elif node.else_statement:
                self.interpret(node.else_statement)
        else:
            self.interpret(node.block)

    def interpret_block(self, node):
        for cmd in node.commands:
            self.interpret(cmd)

    def interpret_binary_operation(self, node):
        left_value = self.interpret(node.left)
        right_value = self.interpret(node.right)

        if node.operator == OpType.OpSum:
            return left_value + right_value
        elif node.operator == OpType.OpMinus:
            return left_value - right_value
        elif node.operator == OpType.OpMult:
            return left_value * right_value
        elif node.operator == OpType.OpDiv:
            return left_value / right_value
        elif node.operator == OpType.OpPow:
            return left_value ** right_value
        elif node.operator == OpType.OpEquals:
            return int(left_value == right_value)
        elif node.operator == OpType.OpNotEquals:
            return int(left_value != right_value)
        elif node.operator == OpType.OpLess:
            return int(left_value < right_value)
        elif node.operator == OpType.OpGreater:
            return int(left_value > right_value)
        elif node.operator == OpType.OpLessOrEquals:
            return int(left_value <= right_value)
        elif node.operator == OpType.OpGreaterOrEquals:
            return int(left_value >= right_value)
        elif node.operator == OpType.OpAnd:
            return int(left_value and right_value)
        elif node.operator == OpType.OpOr:
            return int(left_value or right_value)
        else:
            raise Exception(f'Operador inválido: {node.operator}')

    def interpret_unary_operation(self, node):
        operand_value = self.interpret(node.operand)
        operator = node.operator

        if operator == OpType.OpMinus:
            return -operand_value
        elif operator == OpType.OpNot:
            return int(not operand_value)