from opcodes import OpCode

class Interpreter:
    def __init__(self, program):
        self.program = program
        self.pc = 0
        self.stack = []
        self.top = 0
        self.vars = {}

    def run(self):
        while self.pc < len(self.program):
            opcode = self.program[self.pc]
            self.pc += 1

            if opcode == OpCode.EXIT.value:
                return
            elif opcode == OpCode.NUMBER.value:
                number = self.decode_argument(4)
                self.push(number)
            elif opcode == OpCode.ADD.value:
                self.binary_operation(lambda a, b: a + b)
            elif opcode == OpCode.SUB.value:
                self.binary_operation(lambda a, b: a - b)
            elif opcode == OpCode.MUL.value:
                self.binary_operation(lambda a, b: a * b)
            elif opcode == OpCode.DIV.value:
                self.binary_operation(lambda a, b: a // b)
            elif opcode == OpCode.POW.value:
                self.binary_operation(lambda a, b: a ** b)
            elif opcode == OpCode.NOT.value:
                self.unary_operation(lambda a: not a)
            elif opcode == OpCode.NEG.value:
                self.unary_operation(lambda a: -a)
            elif opcode == OpCode.EQ.value:
                self.binary_operation(lambda a, b: a == b)
            elif opcode == OpCode.NEQ.value:
                self.binary_operation(lambda a, b: a != b)
            elif opcode == OpCode.LE.value:
                self.binary_operation(lambda a, b: a < b)
            elif opcode == OpCode.LEQ.value:
                self.binary_operation(lambda a, b: a <= b)
            elif opcode == OpCode.GE.value:
                self.binary_operation(lambda a, b: a > b)
            elif opcode == OpCode.GEQ.value:
                self.binary_operation(lambda a, b: a >= b)
            elif opcode == OpCode.LOAD.value:
                index = self.program[self.pc]
                self.pc += 1
                value = self.load_variable(index)
                self.stack.append(value)
            elif opcode == OpCode.STORE.value:
                index = self.program[self.pc]
                self.pc += 1
                value = self.stack.pop()
                self.store_variable(index, value)
            elif opcode == OpCode.POP.value:
                self.pop()
            elif opcode == OpCode.DUP.value:
                value = self.peek()
                self.push(value)
            elif opcode == OpCode.PRINT.value:
                value = self.pop()
                print(value)
            elif opcode == OpCode.JUMP.value:
                offset = self.decode_argument(2)
                self.pc += offset
            elif opcode == OpCode.JUMP_TRUE.value:
                offset = self.decode_argument(2)
                value = self.pop()
                if value != 0:
                    self.pc += offset
            elif opcode == OpCode.JUMP_FALSE.value:
                offset = self.decode_argument(2)
                value = self.pop()
                if value == 0:
                    self.pc += offset

    def push(self, value):
        self.stack.append(value)
        self.top += 1

    def pop(self):
        if self.top > 0:
            value = self.stack.pop()
            self.top -= 1
            return value
        else:
            raise Exception("Pilha vazia")

    def peek(self):
        if self.top > 0:
            return self.stack[self.top - 1]
        else:
            raise Exception("Pilha vazia")

    # def load_variable(self, index):
    #     if 0 <= index < len(self.stack):
    #         return self.stack[index]
    #     else:
    #         raise Exception("Índice inválido para variável")

    # def store_variable(self, index, value):
    #     if 0 <= index < len(self.stack):
    #         self.stack[index] = value
    #     else:
    #         raise Exception("Índice inválido para variável")

    def load_variable(self, index):
        if index in self.vars.keys():
            self.push(self.vars[index])
        else:
            raise Exception(f"Var {index} not in memory")

    def store_variable(self, index, value):
        self.vars[index] = value

    def binary_operation(self, operation):
        b = self.pop()
        a = self.pop()
        result = operation(a, b)
        self.push(result)

    def unary_operation(self, operation):
        a = self.pop()
        result = operation(a)
        self.push(result)

    def decode_argument(self, num_bytes):
        argument = int.from_bytes(self.program[self.pc : self.pc + num_bytes], byteorder="big", signed=True)
        self.pc += num_bytes
        return argument
