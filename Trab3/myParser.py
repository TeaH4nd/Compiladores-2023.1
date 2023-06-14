import sys

from lexer import Lexer, TokenType, Token, OpType
from nodes import *


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
        return self.parseCmds()

    def parseCmds(self):
        cmds = []
        while self.currentToken.tokenType in (TokenType.TokPrint, TokenType.TokVar, TokenType.TokNome, TokenType.TokWhile, TokenType.TokIf):
            cmds.append(self.parseCmd())
        return cmds

    def parseCmd(self):
        if self.currentToken.tokenType == TokenType.TokPrint:
            self.consume(TokenType.TokPrint)
            exp = self.parseExp()
            self.consume(TokenType.TokSemicolon)
            return PrintCommandNode(exp)
        elif self.currentToken.tokenType == TokenType.TokVar:
            self.consume(TokenType.TokVar)
            name = self.currentToken.value
            self.consume(TokenType.TokNome)
            self.consume(TokenType.TokOp)
            exp = self.parseExp()
            self.consume(TokenType.TokSemicolon)
            return VariableDeclarationNode(name, exp)
        elif self.currentToken.tokenType == TokenType.TokNome:
            name = self.currentToken.value
            self.consume(TokenType.TokNome)
            self.consume(TokenType.TokOp)
            exp = self.parseExp()
            self.consume(TokenType.TokSemicolon)
            return VariableAssignmentNode(name, exp)
        elif self.currentToken.tokenType == TokenType.TokWhile:
            self.consume(TokenType.TokWhile)
            condition = self.parseExp()
            block = self.parseBlock()
            return WhileLoopNode(condition, block)
        elif self.currentToken.tokenType == TokenType.TokIf:
            self.consume(TokenType.TokIf)
            condition = self.parseExp()
            block = self.parseBlock()
            elses = self.parseElses()
            return IfStatementNode(condition, block, elses)
        else:
            self.error(f"Invalid token {self.currentToken.tokenType}")

    def parseBlock(self):
        self.consume(TokenType.TokLBrace)
        cmds = self.parseCmds()
        self.consume(TokenType.TokRBrace)
        return cmds

    def parseElses(self):
        if self.currentToken.tokenType == TokenType.TokElse:
            self.consume(TokenType.TokElse)
            block = self.parseBlock()
            return IfStatementNode(None, block)
        elif self.currentToken.tokenType == TokenType.TokElif:
            self.consume(TokenType.TokElif)
            condition = self.parseExp()
            block = self.parseBlock()
            elses = self.parseElses()
            return IfStatementNode(condition, block, elses)
        else:
            return None


    def parseExp(self):
        return self.parseE1()

    def parseE1(self):
        e1 = self.parseE2()
        while self.currentToken.tokenType == TokenType.TokOp and self.currentToken.value in (OpType.OpOr,):
            op = self.currentToken.value
            self.consume(TokenType.TokOp)
            e2 = self.parseE2()
            e1 = BinaryOperationNode(op, e1, e2)
        return e1

    def parseE2(self):
        e2 = self.parseE3()
        while self.currentToken.tokenType == TokenType.TokOp and self.currentToken.value in (OpType.OpAnd,):
            op = self.currentToken.value
            self.consume(TokenType.TokOp)
            e3 = self.parseE3()
            e2 = BinaryOperationNode(op, e2, e3)
        return e2

    def parseE3(self):
        e3 = self.parseE4()
        while self.currentToken.tokenType == TokenType.TokOp and self.currentToken.value in (
                OpType.OpEquals, OpType.OpNotEquals, OpType.OpLess, OpType.OpGreater, OpType.OpLessOrEquals,
                OpType.OpGreaterOrEquals):
            op = self.currentToken.value
            self.consume(TokenType.TokOp)
            e4 = self.parseE4()
            e3 = BinaryOperationNode(op, e3, e4)
        return e3

    def parseE4(self):
        e4 = self.parseE5()
        while self.currentToken.tokenType == TokenType.TokOp and self.currentToken.value in (OpType.OpSum, OpType.OpMinus):
            op = self.currentToken.value
            self.consume(TokenType.TokOp)
            e5 = self.parseE5()
            e4 = BinaryOperationNode(op, e4, e5)
        return e4

    def parseE5(self):
        e5 = self.parseE6()
        while self.currentToken.tokenType == TokenType.TokOp and self.currentToken.value in (OpType.OpMult, OpType.OpDiv):
            op = self.currentToken.value
            self.consume(TokenType.TokOp)
            e6 = self.parseE6()
            e5 = BinaryOperationNode(op, e5, e6)
        return e5

    def parseE6(self):
        if self.currentToken.tokenType == TokenType.TokOp and self.currentToken.value == OpType.OpMinus:
            op = self.currentToken.value
            self.consume(TokenType.TokOp)
            e6 = self.parseE6()
            return UnaryOperationNode(op, e6)
        elif self.currentToken.tokenType == TokenType.TokOp and self.currentToken.value == OpType.OpNot:
            op = self.currentToken.value
            self.consume(TokenType.TokOp)
            e6 = self.parseE6()
            return UnaryOperationNode(op, e6)
        else:
            return self.parseE7()

    def parseE7(self):
        e7 = self.parseE8()
        while self.currentToken.tokenType == TokenType.TokOp and self.currentToken.value == OpType.OpPow:
            op = self.currentToken.value
            self.consume(TokenType.TokOp)
            e8 = self.parseE7()
            e7 = BinaryOperationNode(op, e7, e8)
        return e7

    def parseE8(self):
        if self.currentToken.tokenType == TokenType.TokLParen:
            self.consume(TokenType.TokLParen)
            exp = self.parseExp()
            self.consume(TokenType.TokRParen)
            return exp
        elif self.currentToken.tokenType == TokenType.TokNumDec:
            value = self.currentToken.value
            self.consume(TokenType.TokNumDec)
            return NumberNode(value)
        elif self.currentToken.tokenType == TokenType.TokNumHex:
            value = self.currentToken.value
            self.consume(TokenType.TokNumHex)
            return NumberNode(int(value, 16))
        elif self.currentToken.tokenType == TokenType.TokNome:
            name = self.currentToken.value
            self.consume(TokenType.TokNome)
            return VariableNode(name)
        else:
            self.error(f"Invalid token {self.currentToken.tokenType}")
