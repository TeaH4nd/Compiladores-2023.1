import sys

from assembler import Assembler
from interpreter import Interpreter

def main():
    if len(sys.argv) < 2:
        print("Usage: python aravm.py <program.arac>")
        return

    filename = sys.argv[1]
    try:
        with open(filename, "r") as file:
            source_code = file.read()
            assmblr = Assembler()
            program = assmblr.assemble(source_code)
    except IOError:
        print(f"Error: Failed to open file '{filename}'")
        return None
    
    if program is None:
        return

    interpreter = Interpreter(program)
    interpreter.run()

if __name__ == "__main__":
    main()
