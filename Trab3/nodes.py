class BinaryOperationNode:
    def __init__(self, operator, left, right):
        self.operator = operator
        self.left = left
        self.right = right

class UnaryOperationNode:
    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand

class NumberNode:
    def __init__(self, value):
        self.value = value

class VariableNode:
    def __init__(self, name):
        self.name = name

class PrintCommandNode:
    def __init__(self, expression):
        self.expression = expression

class VariableDeclarationNode:
    def __init__(self, name, expression):
        self.name = name
        self.expression = expression

class VariableAssignmentNode:
    def __init__(self, name, expression):
        self.name = name
        self.expression = expression

class WhileLoopNode:
    def __init__(self, condition, block):
        self.condition = condition
        self.block = block

class IfStatementNode:
    def __init__(self, condition, block, else_statement=None):
        self.condition = condition
        self.block = block
        self.else_statement = else_statement
