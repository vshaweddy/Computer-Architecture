"""CPU functionality."""
import sys

SP = 7 # always at the end of the register to hold the current pointer
LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.registers = [0] * 8 # R0-R7
        self.registers[SP] = 0xF4
        self.pc = 0 # Program Counter (address of the currently executing instructions)
        self.branchtable = {}
        self.branchtable[LDI] = self.handle_ldi
        self.branchtable[PRN] = self.handle_prn
        self.branchtable[PUSH] = self.handle_push
        self.branchtable[POP] = self.handle_pop
        self.branchtable[MUL] = self.handle_mul
        self.branchtable[HLT] = self.handle_hlt

        # variables = registers

    def handle_hlt(self, operand_a, operand_b):
        running = False
        self.pc += 1

    def handle_ldi(self, operand_a, operand_b):
        self.registers[operand_a] = operand_b
        self.pc += 3

    def handle_prn(self, operand_a, operand_b):
        print(self.registers[operand_a])
        self.pc += 2

    def handle_push(self, operand_a, operand_b):
        # decrement the stack pointer (SP)
        self.registers[SP] -= 1
                
        given_register = self.ram_read(self.pc + 1)
        value_in_register = self.registers[given_register]

        # write the value of the given register to memory AT the SP location
        # self.ram_write(value_in_register, self.registers[SP])
        top_stack_address = self.registers[SP]
        self.ram[top_stack_address] = value_in_register

        # increment pc 
        self.pc += 2

    def handle_pop(self, operand_a, operand_b):
        given_register = self.ram_read(self.pc + 1)

        # Write the value in the memory at the top of the stack to the given register
        value_from_memory = self.ram_read(self.registers[SP])
        self.registers[given_register] = value_from_memory

        # increment stack pointer
        self.registers[SP] += 1
        self.pc += 2

    def handle_mul(self, operand_a, operand_b):
        # overwrite the first address value with new number
        self.registers[operand_a] = self.registers[operand_a] * self.registers[operand_b] 
        self.pc += 3

    # should accept the address to read and return the value stored there
    def ram_read(self, address):
        return self.ram[address]

    # should accept a value to write, and the address to write it to
    def ram_write(self, value, address):
        self.ram[address] = value

    def load(self):
        try:
            address = 0
            with open(sys.argv[1]) as file:
                for line in file:
                    # Split the current line on the # symbol
                    split_file = line.split('#')

                    # Removes whitespace and \n character
                    value = split_file[0].strip()

                    # Make sure that the value before the # symbol is not empty
                    if value == "":
                        continue

                    try:
                        instruction = int(value, 2) # Convert binary string to int
                    except ValueError:
                        print(f"Invalid number: {value}")
                        sys.exit(1)

                    self.ram[address] = instruction
                    address += 1

        except FileNotFoundError:
            print(f"{sys.argv[0]} {sys.argv[1]} file not found")
            sys.exit(2)

        # address = 0

        # # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        running = True
 
        while running:
            # read line by line from memory
            instruction = self.ram_read(self.pc)

            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if instruction in self.branchtable:
                self.branchtable[instruction](operand_a, operand_b)

            # Exit if it's crashed
            else:
                print(f"Unknown instruction: {instruction}")
                sys.exit(1)

# Notes:
# pointer is variable that hold an address
# address is the location in the memory
