# Katrina Huang | S2739565
# Introduction to Theoretical Computer Science F24
# Coursework 1: Question 3

# Goal #1: Implement a simulator for register machines.

# Goal #2: Write a register machine to implement squares.

import sys

class RegisterMachine:
    def __init__(self):
        self.registers = []
        self.program = []
        self.labels = {}

    def load_program(self, input_lines):
        # read the register initialization line
        reg_line = input_lines[0].strip().split()
        if reg_line[0] != 'registers':
            raise ValueError("Invalid input")
        self.registers = [int(x) for x in reg_line[1:]]

        # parse
        for i, line in enumerate(input_lines[1:], start=0):
            line = line.strip()
            if line.startswith("#") or not line:
                continue
            if ":" in line:  # labeling
                label, instruction = line.split(":")
                self.labels[label.strip()] = len(self.program)
                if instruction.strip():
                    self.program.append(instruction.strip())
            else:
                self.program.append(line)

    def run(self, trace=False):
        pc = 0 
        while pc < len(self.program):
            inst = self.program[pc]
            if trace:
                print(f"Executing: {inst}")

            if inst.startswith('inc'):
                _, reg = inst.split()
                reg_num = int(reg[1:])
                self.ensure_register_exists(reg_num)
                self.registers[reg_num] += 1
                pc += 1
            elif inst.startswith('decjz'):
                _, reg, label = inst.split()
                reg_num = int(reg[1:])
                self.ensure_register_exists(reg_num)
                if self.registers[reg_num] == 0:
                    pc = self.labels.get(label, pc + 1) 
                else:
                    self.registers[reg_num] -= 1
                    pc += 1
            elif inst == "HALT":
                break
            else:
                raise ValueError(f"Unknown instruction: {inst}")

    def ensure_register_exists(self, reg_num):
        if reg_num >= len(self.registers):
            self.registers.extend([0] * (reg_num - len(self.registers) + 1))

    def print_registers(self):
        print(f"registers {' '.join(map(str, self.registers))}")

def main():
    input_lines = sys.stdin.read().splitlines()
    machine = RegisterMachine()
    machine.load_program(input_lines)
    trace_flag = '-t' in sys.argv
    machine.run(trace=trace_flag)
    machine.print_registers()

if __name__ == "__main__":
    main()