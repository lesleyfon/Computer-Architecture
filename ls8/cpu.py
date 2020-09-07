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
            'HLT': 0b00000001
        }

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        # Similar to memory array
        program = [
            # From print8.ls8

            0b10000010,  # LDI R0,8 => LDI register immediate,
            0b00000000,
            0b00001000,
            0b01000111,  # PRN R0 => register pseudo-instruction
            0b00000000,
            0b00000001,  # HLT => Halt the CPU (and exit the emulator).
            0b10000010,  # LDI R0,8 => LDI register immediate,
            0b00000010,
            0b00001010,


        ]
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
        with open("/Users/lesley/code/Python/Projects/Computer-Architecture/ls8/examples/print8.ls8") as f:
            program_inst = f.read()
        program_inst = program_inst.split()

        program_inst = [inst for inst in program_inst if len(
            inst) == 8 and inst[0] == "1" or inst[0] == "0"]

        while self.is_on:
            instruction = int(program_inst[self.pc], 2)

            if instruction == self.instructions["LDI"]:

                self.ram_write(int(program_inst[self.pc + 2], 2),
                               int(program_inst[self.pc + 1], 2))
                self.pc += 3
            elif instruction == self.instructions["PRN"]:

                print(self.ram_read(int(program_inst[self.pc + 1], 2)))
                self.pc += 2

            elif instruction == self.instructions["HLT"]:
                self.is_on = False
                self.pc += 1
