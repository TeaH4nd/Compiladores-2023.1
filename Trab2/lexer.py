import re

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0

    def next_token(self):
        while self.pos < len(self.text):
            if self.text[self.pos].isspace():
                self.pos += 1
                continue
            if self.text[self.pos] == '(':
                self.pos += 1
                return Token(TokenType.LEFT_PAREN, '(')
            if self.text[self.pos] == ')':
                self.pos += 1
                return Token(TokenType.RIGHT_PAREN, ')')
            if self.text[self.pos] in ['+', '-', '*', '/', '^']:
                self.pos += 1
                return Token(TokenType.OPERATOR, self.text[self.pos-1])
            if self.text[self.pos].isdigit():
                num = ''
                while self.pos < len(self.text) and self.text[self.pos].isdigit():
                    num += self.text[self.pos]
                    self.pos += 1
                return Token(TokenType.NUMBER, int(num))
            if self.text[self.pos] == '0' and self.pos+1 < len(self.text) and self.text[self.pos+1] == 'x':
                hex_num = ''
                self.pos += 2
                while self.pos < len(self.text) and re.match(r'[0-9a-fA-F]', self.text[self.pos]):
                    hex_num += self.text[self.pos]
                    self.pos += 1
                if hex_num:
                    return Token(TokenType.NUMBER, int(hex_num, 16))
                else:
                    raise Exception('Invalid hexadecimal number')
            if self.text[self.pos:self.pos+2] == '//':
                self.pos += 2
                while self.pos < len(self.text) and self.text[self.pos] != '\n':
                    self.pos += 1
                continue
            if self.text[self.pos:self.pos+2] == '/*':
                self.pos += 2
                while self.pos < len(self.text) and self.text[self.pos:self.pos+2] != '*/':
                    self.pos += 1
                if self.pos == len(self.text):
                    raise Exception('Unterminated comment block')
                self.pos += 2
                continue
            raise Exception(f'Invalid character: {self.text[self.pos]}')
        return Token(TokenType.EOF, '')

class Token:
    def __init__(self, token_type, value):
        self.token_type = token_type
        self.value = value

class TokenType:
    LEFT_PAREN = 'LEFT_PAREN'
    RIGHT_PAREN = 'RIGHT_PAREN'
    OPERATOR = 'OPERATOR'
    NUMBER = 'NUMBER'
    EOF = 'EOF'
