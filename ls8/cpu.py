"""CPU functionality."""
import sys
import os.path

SP = 7 # always at the end of the register to hold the current pointer
LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
ADD =  0b10100000
CMP = 0b10100111 # ALU OP
JMP = 0b01010100 # PC MUTATOR
JEQ = 0b01010101 # PC MUTATOR
JNE = 0b01010110 # PC MUTATOR

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.registers = [0] * 8 # R0-R7
        self.registers[SP] = 0xF4
        self.pc = 0 # Program Counter (address of the currently executing instructions)
        self.running = False
        
        self.branchtable = {}
        self.branchtable[LDI] = self.handle_ldi
        self.branchtable[PRN] = self.handle_prn
        self.branchtable[PUSH] = self.handle_push
        self.branchtable[POP] = self.handle_pop
        self.branchtable[MUL] = self.handle_mul
        self.branchtable[HLT] = self.handle_hlt
        self.branchtable[ADD] = self.handle_add
        self.branchtable[CALL] = self.handle_call
        self.branchtable[RET] = self.handle_ret
        self.branchtable[MUL] = self.handle_mul
        self.branchtable[CMP] = self.handle_cmp
        self.branchtable[JMP] = self.handle_jmp
        self.branchtable[JEQ] = self.handle_jeq
        self.branchtable[JNE] = self.handle_jne

        # variables = registers

    def handle_hlt(self, operand_a, operand_b):
        self.running = False
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
        self.op_helper("MUL")

    def handle_add(self, operand_a, operand_b):
        self.op_helper("ADD")

    def handle_call(self, operand_a, operand_b):
        given_register = self.ram[self.pc + 1]

        # decrement the stack pointer
        self.registers[SP] -= 1
        
        # address of the next instruction 
        next_address_instruction = self.pc + 2

        # store it in the stack
        self.ram[self.registers[SP]] = next_address_instruction

        # find the register that we'll be calling from and the address that is in that register
        next_address = self.registers[given_register]

        # set the pc to the next address
        self.pc = next_address

    def handle_ret(self, operand_a, operand_b):
        # pop the stack pointer from the reg
        address_to_pop = self.ram[self.registers[SP]]

        # set the pc to that address
        self.pc = address_to_pop

        # increment the sp after popping
        self.registers[SP] += 1

    # compare the values in two registers
    def handle_cmp(self, operand_a, operand_b):
        self.alu("CMP", operand_a, operand_b)
        self.pc += 3

    # jump to the address that stored in the given register
    def handle_jmp(self, operand_a, operand_b):
        self.pc = self.registers[operand_a]

    # if equal, jump to the address in the given register
    def handle_jeq(self, operand_a, operand_b):
        if self.flag == 0b00000001:
            self.pc = self.registers[operand_a]
        else:
            self.pc += 2

    # if E flag is clear (false, 0), jump to the address in the given register
    def handle_jne(self, operand_a, operand_b):
        if self.flag != 0b00000001:
            self.pc = self.registers[operand_a]
        else:
            self.pc += 2

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

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.registers[reg_a] += self.registers[reg_b]
        elif op == "CMP":
            if self.registers[reg_a] < self.registers[reg_b]:
                # less than flag
                self.flag = 0b00000100 
            if self.registers[reg_a] > self.registers[reg_b]:
                # greater than flag
                self.flag = 0b00000010 
            if self.registers[reg_a] == self.registers[reg_b]:
                # equal flag
                self.flag = 0b00000001 
        else:
            raise Exception("Unsupported ALU operation")

    def op_helper(self, op):
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        self.alu(op, operand_a, operand_b)
        self.pc += 3


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
        self.running = True
 
        while self.running:
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
