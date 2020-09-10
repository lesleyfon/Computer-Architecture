import sys

# Operation Codes
# OP Codes
PRINT_HELLO_WORLD = 1  # 0b00000001
HALT = 2  # 0b00000010
PRINT_NUM = 3  # 0b00000011
SAVE_REG = 4
PRINT_REG = 5
ADD = 6
PUSH = 8
POP = 9
CALL = 10
RET = 11
# ADD takes TWO registers, adds their values
# and stores the result in the first register given
# ​
# program that adds two numbers together
# return\

memory = [0] * 226
registers = [0] * 8
running = True
pc = 0
SP = 7
# Get file name from command line arguments
if len(sys.argv) != 2:
    print("Usage: example_cpu.py filename")
    sys.exit(1)


def load_memory(filename):
    # Open a file and load into memory
    address = 0
    try:
        with open(filename) as f:
            for line in f:
                # Split the current line on the # symbol
                split_line = line.split('#')
                # removes whitespace and \n character
                code_value = split_line[0].strip()
                # Make sure that the value before the # symbol is not empty
                if code_value == '':
                    continue
                num = int(code_value)
                memory[address] = num
                address += 1
    except FileNotFoundError:
        print(f"{sys.argv[1]} file not found")
        sys.exit(2)


load_memory(sys.argv[1])
while running:
    # Read line by line from memory
    instruction = memory[pc]
    if instruction == PRINT_HELLO_WORLD:
        # print Hello world
        # move the PC up 1 to the next instruction
        print("Hello World")
        pc += 1
    elif instruction == PRINT_NUM:
        # Print the number in the NEXT memory slot
        num = memory[pc + 1]
        print(num)
        pc += 2

    elif instruction == SAVE_REG:
        # Save some value to some register
        # First number after instruction will be the Value to store
        # second number after instruction will be register
        num = memory[pc + 1]
        reg_location = memory[pc + 2]
        registers[reg_location] = num

        pc += 3
    elif instruction == PRINT_REG:
        reg_location = memory[pc + 1]
        print(registers[reg_location])
        pc += 2
    elif instruction == ADD:
        # ADD takes TWO registers, adds their values
        # and stores the result in the first register given
        # Get register 1
        # get register 2
        # Add the values of both registers together
        # Store in register 1
        reg_1 = memory[pc + 1]
        reg_2 = memory[pc + 2]
        registers[reg_1] += registers[reg_2]
        pc += 3
    elif instruction == HALT:
        running = False
        pc += 1
    elif instruction == PUSH:
        given_reg = memory[pc + 1]

        value_in_reg = registers[given_reg]
        registers[7] -= 1

        pass
    elif instruction == CALL:
        '''
            Get the given register in the operand
            Sore the return address onto the stack
        '''
        given_reg = memory[pc + 1]

        registers[SP] -= 1
        memory[registers[SP]] = pc + 2

        pc = registers[given_reg]
    elif instruction == RET:
        '''
            Set PC to the value at the top of the stack
        '''
        pc = memory[registers[SP]]
        registers[SP] += 1
    else:
        print(f"Unknown instruction {instruction}")
        sys.exit(1)
