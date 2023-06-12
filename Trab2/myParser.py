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

from lexer import TokenType

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.currentToken = self.lexer.next()

    def error(self, message):
        raise Exception(message)

    def consume(self, tokenType):
        if self.currentToken.tokenType == tokenType:
            self.currentToken = self.lexer.next()
        else:
            self.error(f"Expected token {tokenType}, but found {self.currentToken.tokenType}")

    def parse(self):
        # self.currentToken = self.lexer.next()
        return self.parse_e()

    def parse_e(self):
        if self.currentToken.tokenType in (TokenType.TokNumDec, TokenType.TokNumHex):
            node = NumberNode(self.currentToken.value)
            self.consume(self.currentToken.tokenType)
            return node
        elif self.currentToken.tokenType == TokenType.TokLParen:
            self.consume(TokenType.TokLParen)
            node = self.parse_e()
            self.consume(TokenType.TokRParen)
            return node
        elif self.currentToken.tokenType == TokenType.TokOp:
            op = self.currentToken.value
            self.consume(TokenType.TokOp)
            left = self.parse_e()
            right = self.parse_e()
            return BinaryOperationNode(op, left, right)
        else:
            self.error(f"Invalid token {self.currentToken.tokenType}")


class BinaryOperationNode:
    def __init__(self, operator, left, right):
        self.operator = operator
        self.left = left
        self.right = right

class NumberNode:
    def __init__(self, value):
        self.value = value
