#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()

cpu.load()
cpu.run()


# given_register = memory[pc + 1]
# value_in_register = registers[given_register]
# # decrement the Stack Pointer
# registers[SP] -= 1
# # write the value of the given register to memory AT the SP location
# memory[registers[SP]] = value_in_register
# pc += 2
