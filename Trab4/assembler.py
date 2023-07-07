from opcodes import OpCode

class Assembler:
    def __init__(self):
        self.instructions = []  # Lista de instruções
        self.labels = {}  # Dicionário de labels e seus endereços

    def assemble(self, source_code):
        # Passagem 1: Parsing
        self.parse(source_code)

        # Passagem 2: Construção da representação interna binária
        binary_code = self.build_binary_code()

        # Passagem 3: Backpatching
        self.backpatch(binary_code)

        return binary_code
    
    def add_label(self, label):
        if label not in self.labels:
            self.labels[label] = len(self.instructions)
        else:
            raise Exception(f"Duplicate label: {label}")

    def parse(self, source_code):
        lines = source_code.split("\n")
        for line in lines:
            line = line.strip()
            if line:
                self.parse_line(line)

    def parse_line(self, line):
        if line.count(':') > 0:
            qnd_labels = line.count(':')
            parts = line.split(':')
            for i in range(qnd_labels):
                label = parts[i]
                self.add_label(label)
            line = parts[qnd_labels:][0].strip()
        parts = line.split()
        if len(parts) > 1:
            inst = parts[0]
            args = parts[1]
        else:
            inst = parts[0]
            args = None
        
        self.instructions.append((inst, args))

    def build_binary_code(self):
        binary_code = bytearray()
        for instruction, arg in self.instructions:
            binary_code.append(self.get_opcode(instruction))
            if arg:
                arg_encoded = self.encode_argument(arg, instruction)
                binary_code.extend(arg_encoded) # type: ignore
        return binary_code

    def get_opcode(self, instruction):
        try:
            opcode = OpCode[instruction].value
            return opcode
        except KeyError:
            raise Exception(f"Instrução desconhecida: {instruction}")

    def encode_argument(self, arg, inst):
        if inst == 'NUMBER':
            num_bytes = 4
        elif inst in ['LOAD', 'STORE']:
            num_bytes = 1
        elif inst.startswith("JUMP"):
            num_bytes = 2
        else:
            num_bytes = 0
            raise Exception(f"Instução [{inst}] não possui argumentos")
        if arg:
            if arg.isnumeric():
                value = int(arg)
                return value.to_bytes(num_bytes, 'big')
            elif arg.startswith("L"):
                label = arg
                if label in self.labels:
                    address = self.labels[label]
                    offset = int(address - len(self.instructions) - 1)
                    return offset.to_bytes(num_bytes, 'big', signed=True)
                else:
                    raise Exception(f"Label '{label}' não encontrado")
            else:
                raise Exception(f"Tipo de argumento desconhecido: {arg}")

    def backpatch(self, binary_code):
        binary_counter = 0
        for i, (instruction, args) in enumerate(self.instructions):
            if instruction == 'NUMBER':
                binary_counter += 4
            if instruction in ['LOAD', 'STORE']:
                binary_counter += 1
            if instruction.startswith("JUMP"):
                label = args
                if label in self.labels:
                    address = self.labels[label]
                    offset = address - i
                    binary_code[binary_counter + 1] = offset >> 8  # Byte de ordem alta do deslocamento
                    binary_code[binary_counter + 2] = offset & 0xFF  # Byte de ordem baixa do deslocamento
                    binary_counter += 2
                    continue
                else:
                    raise Exception(f"Label '{label}' não encontrado")
                
            binary_counter += 1

