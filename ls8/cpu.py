"""CPU functionality."""
import sys

LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.registers = [0] * 8 # R0-R7
        self.pc = 0 # Program Counter (address of the currently executing instructions)

        # variables = registers

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


    # def alu(self, op, reg_a, reg_b):
    #     """ALU operations."""

    #     if op == "ADD":
    #         self.reg[reg_a] += self.reg[reg_b]
    #     #elif op == "SUB": etc
    #     else:
    #         raise Exception("Unsupported ALU operation")

    # def trace(self):
    #     """
    #     Handy function to print out the CPU state. You might want to call this
    #     from run() if you need help debugging.
    #     """

    #     print(f"TRACE: %02X | %02X %02X %02X |" % (
    #         self.pc,
    #         #self.fl,
    #         #self.ie,
    #         self.ram_read(self.pc),
    #         self.ram_read(self.pc + 1),
    #         self.ram_read(self.pc + 2)
    #     ), end='')

    #     for i in range(8):
    #         print(" %02X" % self.reg[i], end='')

    #     print()

    def run(self):
        running = True
        pc = 0
        
        while running:
            # read line by line from memory
            instruction = self.ram_read(pc)
            # print(instruction)

            if instruction == LDI:
                reg_location = self.ram[pc + 1]
                num = self.ram[pc +2]
                self.ram_write(num, reg_location)
                pc += 3

            elif instruction == PRN:
                reg_location = self.ram[pc + 1]
                print(self.ram_read(reg_location))
                pc += 2

            # For Add but later
            # elif instruction == 0b10100000:
            #     reg_location1 = self.ram[pc + 1]
            #     reg_location2 = self.ram[pc + 2]
            #     new_num = self.ram_read(reg_location1) * self.ram_read(reg_location2)
            #     print(new_num)
            #     self.ram_write(new_num, self.ram[pc + 3])
            #     pc += 4

            elif instruction == MUL:
                reg_location1 = self.ram[pc + 1] # get the first number
                reg_location2 = self.ram[pc + 2] # get the second number
                new_num = self.ram_read(reg_location1) * self.ram_read(reg_location2)
                self.ram_write(new_num, self.ram[pc +1]) # overwrite the first address value with new number
                pc += 3
            
            elif instruction == HLT:
                running = False
                pc += 1

            # Exit if it's crashed
            else:
                print(f"Unknown instruction: {instruction}")
                sys.exit(1)

