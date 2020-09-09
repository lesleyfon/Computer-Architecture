"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.register = [None] * 8
        self.ram = [None] * 256
        self.pc = 0  # Program Counter, address of the currently executing instruction
        self.stack_pointer = 0
        self.is_on = True
        self.instructions = {
            "LDI": 0b10000010,  # Set the value of a register to an integer.
            # Print numeric value stored in the given register.
            "PRN": 0b01000111,
            'HLT': 0b00000001,

            # MUL R0,R1 Multiply the values in two registers together and store the result in registerA.
            "MUL": 0b10100010



        }

    def load(self, program=[]):
        """Load a program into memory."""
        if len(program) == 0:
            return

        address = 0

        while True:
            instrunction = program[address]

            if instrunction == self.instructions["LDI"]:
                reg_index = int(program[address + 1])
                self.ram[reg_index] = int(program[address + 2])
                address += 3
            else:
                address += 1

            if address == len(program):
                break

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        '''
            Value = Args1 \n
            Address = Args2
        '''

        self.ram[address] = value

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

    def run(self):
        """
            Run the CPU.

        """
        file_name = sys.argv[1]

        program_instruction = []
        with open(f"/Users/lesley/code/Python/Projects/Computer-Architecture/ls8/examples/{file_name}") as f:
            for line in f:
                line = line.split("#")
                line = line[0]
                line = line.strip()

                if line == "":
                    continue
                else:
                    program_instruction.append(line)

        self.load(program_instruction)  # Loads the Ram

        while self.is_on:
            instruction = int(program_instruction[self.pc], 2)

            if instruction == self.instructions["LDI"]:

                self.ram_write(int(program_instruction[self.pc + 2], 2),
                               int(program_instruction[self.pc + 1], 2))
                self.pc += 3
            elif instruction == self.instructions["PRN"]:

                print(self.ram_read(int(program_instruction[self.pc + 1], 2)))
                self.pc += 2
            elif instruction == self.instructions["MUL"]:
                # convert R1 and R1 to Interger Numbers
                R1 = int(program_instruction[self.pc + 1], 2)
                R2 = int(program_instruction[self.pc + 2], 2)

                product = R1 * R2

                self.ram_write(product, int(
                    program_instruction[self.pc + 1], 2))

                self.pc += 3

            elif instruction == self.instructions["HLT"]:
                self.is_on = False
                self.pc += 1
            else:
                self.pc += 1
                if self.pc == len(program_instruction):
                    self.is_on = False
