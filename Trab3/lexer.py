import sys
from enum import Enum

class TokenType(Enum):
    TokNumDec = 1
    TokNumHex = 2
    TokOp = 3
    TokEOF = 4
    TokLParen = 5
    TokRParen = 6
    TokPrint = 7
    TokVar = 8
    TokWhile = 9
    TokIf = 10
    TokElse = 11
    TokElif = 12
    TokNome = 13

class OpType(Enum):
    OpSum = 1
    OpMinus = 2
    OpMult = 3
    OpDiv = 4
    OpMod = 5
    OpPow = 6
    OpAnd = 7
    OpOr = 8
    OpEquals = 9
    OpNotEquals = 10
    OpLess = 11
    OpGreater = 12
    OpLessOrEquals = 13
    OpGreaterOrEquals = 14

class Token:
    def __init__(self, tokenType, value):
        self.tokenType = tokenType
        self.value = value

    def __str__(self):
        if hasattr(self.value, 'name'):
            return f"{self.tokenType.name} {self.value.name}"
        else:
            return f"{self.tokenType.name} {self.value}"

class Lexer:
    def __init__(self, line):
        self.line = line
        self.currentChar = 0

    def next(self):
        if not self.line:
            return Token(TokenType.TokEOF, None)
        while self.currentChar < len(self.line):
            if self.line[self.currentChar].isspace():
                self.currentChar += 1
                continue
            if self.line[self.currentChar] == '+':
                self.currentChar += 1
                return Token(TokenType.TokOp, OpType.OpSum)
            if self.line[self.currentChar] == '-':
                self.currentChar += 1
                return Token(TokenType.TokOp, OpType.OpMinus)
            if self.line[self.currentChar] == '*':
                self.currentChar += 1
                return Token(TokenType.TokOp, OpType.OpMult)
            if self.line[self.currentChar] == '/':
                # check for comment
                if self.currentChar + 1 < len(self.line) and self.line[self.currentChar + 1] == '/':
                    # ignore rest of the line
                    self.currentChar = len(self.line)
                    continue
                elif self.currentChar + 1 < len(self.line) and self.line[self.currentChar + 1] == '*':
                    # ignore comment block
                    self.currentChar += 2
                    while True:
                        if not self.line:
                                raise Exception("Unterminated comment block")
                        if '*/' in self.line[self.currentChar:]:
                            self.currentChar = self.line.index('*/', self.currentChar) + 2
                            break
                        else:
                            self.currentChar = 0
                            self.line = sys.stdin.readline()
                            if not self.line:
                                raise Exception("Unterminated comment block")
                    continue
                else:
                    self.currentChar += 1
                    return Token(TokenType.TokOp, OpType.OpDiv)
            if self.line[self.currentChar] == '%':
                self.currentChar += 1
                return Token(TokenType.TokOp, OpType.OpMod)
            if self.line[self.currentChar] == '^':
                self.currentChar += 1
                return Token(TokenType.TokOp, OpType.OpPow)
            if self.line[self.currentChar] == '(':
                self.currentChar += 1
                return Token(TokenType.TokLParen, None)
            if self.line[self.currentChar] == ')':
                self.currentChar += 1
                return Token(TokenType.TokRParen, None)
            if self.line[self.currentChar].isdigit():
                # check if decimal or hexadecimal number
                start = self.currentChar
                while self.currentChar < len(self.line) and self.line[self.currentChar].isdigit():
                    self.currentChar += 1
                if self.currentChar < len(self.line) and self.line[self.currentChar] == 'x':
                    self.currentChar += 1
                    while self.currentChar < len(self.line) and self.line[self.currentChar].isdigit():
                        self.currentChar += 1
                    return Token(TokenType.TokNumHex, self.line[start:self.currentChar])
                else:
                    return Token(TokenType.TokNumDec, int(self.line[start:self.currentChar]))
            if self.line[self.currentChar].isalpha():
                # check if keyword or variable name
                start = self.currentChar
                while self.currentChar < len(self.line) and (self.line[self.currentChar].isalpha() or self.line[self.currentChar].isdigit()):
                    self.currentChar += 1
                name = self.line[start:self.currentChar]
                if name == 'print':
                    return Token(TokenType.TokPrint, None)
                elif name == 'var':
                    return Token(TokenType.TokVar, None)
                elif name == 'while':
                    return Token(TokenType.TokWhile, None)
                elif name == 'if':
                    return Token(TokenType.TokIf, None)
                elif name == 'else':
                    return Token(TokenType.TokElse, None)
                elif name == 'elif':
                    return Token(TokenType.TokElif, None)
                else:
                    return Token(TokenType.TokNome, name)
            raise Exception(f"Invalid character: {self.line[self.currentChar]}")
        return Token(TokenType.TokEOF, None)
