"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.register = [None] * 8
        self.ram = [None] * 256
        self.pc = 0  # Program Counter, address of the currently executing instruction
        self.reg_counter = 0
        self.is_on = True
        self.instructions = {
            "LDI": 0b10000010,  # Set the value of a register to an integer.
            # Print numeric value stored in the given register.
            "PRN": 0b01000111,
            'HLT': 0b00000001,

            # MUL R0,R1 Multiply the values in two registers together and store the result in registerA.
            "MUL": 0b10100010



        }

    def load(self):
        """Load a program into memory."""

        file_name = sys.argv
        if len(file_name) == 1:
            print("Provide a file name ro read instructions from")
            sys.exit(1)
        address = 0
        with open(f"/Users/lesley/code/Python/Projects/Computer-Architecture/ls8/examples/{file_name[1]}") as f:
            for line in f:
                line = line.split("#")
                line = line[0]
                line = line.strip()

                if line == "":
                    continue
                else:
                    num = int(line, 2)
                    self.ram[address] = num
                    address += 1

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
        self.pc = 0
        """
            Run the CPU.

        """
        while self.is_on:
            instruction = self.ram[self.pc]

            if instruction == self.instructions["LDI"]:

                num = self.ram[self.pc + 2]
                reg_loc = self.ram[self.pc + 1]

                self.register[reg_loc] = num

                self.pc += 3

            elif instruction == self.instructions["PRN"]:

                print(self.register[self.ram[self.pc + 1]])

                self.pc += 2

            elif instruction == self.instructions["MUL"]:
                # convert R1 and R1 to Interger Numbers
                R1 = self.ram[self.pc + 1]
                R2 = self.ram[self.pc + 2]

                product = self.register[R1] * self.register[R2]
                self.register[R1] = product
                self.pc += 3

            elif instruction == self.instructions["HLT"]:
                self.is_on = False
                self.pc += 1
            elif instruction not in self.instructions:
                print(f"Unknown instruction {instruction}")
                sys.exit(1)
            else:
                self.pc += 1
                if self.pc == len(self.ram):
                    self.is_on = False
