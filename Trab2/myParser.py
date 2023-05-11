from lexer import TokenType

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.next_token()

    def parse(self):
        return self.expression()

    def expression(self):
        if self.current_token.token_type == TokenType.NUMBER:
            node = self.number()
        elif self.current_token.token_type == TokenType.LEFT_PAREN:
            node = self.parenthesized_expression()
        else:
            node = self.operator_expression()
        return node

    def parenthesized_expression(self):
        self.consume(TokenType.LEFT_PAREN)
        node = self.expression()
        self.consume(TokenType.RIGHT_PAREN)
        return node

    def operator_expression(self):
        operator = self.consume(TokenType.OPERATOR)
        left = self.expression()
        right = self.expression()
        return BinaryOperationNode(operator.value, left, right)

    def number(self):
        number = self.consume(TokenType.NUMBER)
        return NumberNode(number.value)

    def consume(self, expected_type):
        if self.current_token.token_type == expected_type:
            token = self.current_token
            self.current_token = self.lexer.next_token()
            return token
        else:
            raise Exception(f'Expected {expected_type}, found {self.current_token.token_type}')

class BinaryOperationNode:
    def __init__(self, operator, left, right):
        self.operator = operator
        self.left = left
        self.right = right

class NumberNode:
    def __init__(self, value):
        self.value = value
