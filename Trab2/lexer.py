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

import sys

from enum import Enum

class TokenType(Enum):
    TokNumDec = 1
    TokNumHex = 2
    TokOp = 3
    TokEOF = 4
    TokLParen = 5
    TokRParen = 6

class OpType(Enum):
    OpSum = 1
    OpMinus = 2
    OpMult = 3
    OpDiv = 4
    OpMod = 5
    OpPow = 6

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
                return Token(TokenType.TokLParen, '(')
            if self.line[self.currentChar] == ')':
                self.currentChar += 1
                return Token(TokenType.TokRParen, ')')
            if self.line[self.currentChar].isdigit():
                start = self.currentChar
                is_hex = False

                # check if it's hexadecimal
                if self.line[start] == '0' and self.currentChar + 1 < len(self.line) and self.line[self.currentChar + 1] in 'xX':
                    self.currentChar += 2
                    is_hex = True

                # find end of number
                while self.currentChar < len(self.line) and (self.line[self.currentChar].isdigit() or (is_hex and self.line[self.currentChar].lower() in 'abcdef')):
                    self.currentChar += 1

                # return number token
                if is_hex:
                    return Token(TokenType.TokNumHex, self.line[start:self.currentChar])
                else:
                    return Token(TokenType.TokNumDec, int(self.line[start:self.currentChar]))

            raise Exception(f"Invalid character '{self.line[self.currentChar]}' at position {self.currentChar+1}")
