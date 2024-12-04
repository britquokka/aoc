import logging
import os
import time
from TestUtils import TestUtils
from collections import namedtuple
import re

logger = logging.getLogger(__name__)

Instruction = namedtuple('Instruction', ['name', 'operands'])


class MemoryScanner:

    def __init__(self, program_memory):
        self.program_memory = program_memory

    @staticmethod
    def extract_operands(start, line):
        operands = None
        eat = 0
        sub_end = min(start + 8, len(line))
        sub_string = line[start: sub_end]
        idx = sub_string.find(')')
        if idx != -1:
            eat = idx
            numbers_str = sub_string[:idx].split(',')
            if len(numbers_str) == 2:
                numbers = [int(s) for s in numbers_str if s.isdigit()]
                if len(numbers) == 2:
                    operands = (numbers[0], numbers[1])
        return operands, eat

    @staticmethod
    def extract_mul_instructions(offset, line):
        instructions = []
        start = 0
        end_line = len(line) - 1
        flag_exit_loop = False
        while not flag_exit_loop:
            idx = line.find("mul(", start, end_line)
            if idx != -1:
                start = idx + len("mul(")
                operands, eat = MemoryScanner.extract_operands(start, line)
                start = start + eat
                if operands:
                    instructions.append((offset + idx, Instruction(name='mul', operands=operands)))
            else:
                flag_exit_loop = True
        return instructions

    @staticmethod
    def extract_other_instructions(offset, line, name):
        instructions = []
        start = 0
        end_line = len(line) - 1
        flag_exit_loop = False
        while not flag_exit_loop:
            idx = line.find(name, start, end_line)
            if idx != -1:
                start = idx + len(name)
                instructions.append((idx + offset, Instruction(name=name, operands=None)))
            else:
                flag_exit_loop = True
        return instructions

    def get_mul_instructions(self):
        instructions = []
        offset = 0
        for line in self.program_memory:
            instructions.extend(self.extract_mul_instructions(offset, line))
            offset += len(line)
        return instructions

    def get_other_instructions(self, name):
        instructions = []
        offset = 0
        for line in self.program_memory:
            instructions.extend(self.extract_other_instructions(offset, line, name))
            offset += len(line)
        return instructions


class Puzzle:
    @staticmethod
    def to_program_memory(file):
        with open(file) as f:
            memory = f.read()
        return memory

    def __init__(self, file):
        self.program_memory = Puzzle.to_program_memory(file)

    def run_program(self):
        total = 0
        for instruction in re.findall(r'mul\(\d+,\d+\)', self.program_memory):
            op1, op2 = instruction[4:-1].split(',')
            total += int(op1) * int(op2)
        return total

    def run_program_part2(self):
        total = 0
        enable = True
        for instruction in re.findall(r'mul\(\d+,\d+\)|don\'t\(\)|do\(\)', self.program_memory):
            match instruction:
                case 'do()':
                    enable = True
                case  'don\'t()':
                    enable = False
                case _:
                    if enable:
                        op1, op2 = instruction[4:-1].split(',')
                        total += int(op1) * int(op2)
        return total


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING)
    TEST_DATA_DIR = os.path.join(os.getcwd(), 'data')
    INPUT_FILE_EXAMPLE = os.path.join(TEST_DATA_DIR, 'day03', 'example.txt')
    INPUT_FILE_EXAMPLE_PART2 = os.path.join(TEST_DATA_DIR, 'day03', 'example_part2.txt')
    INPUT_FILE = os.path.join(TEST_DATA_DIR, 'day03', 'input.txt')

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 1: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result_no_arg("part1", 161,
                                           puzzle.run_program)
    print("part 1: execution time is ", time.time() - t0, " s")
    print("part 1: The sum of the multiplications is", result)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 1: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result_no_arg("part1", 161085926,
                                           puzzle.run_program)
    print("part 1: execution time is ", time.time() - t0, " s")
    print("part 1: The sum of the multiplications is", result)

    # print("-----------------")
    # input_file = INPUT_FILE_EXAMPLE_PART2
    # print("part 2: input file is ", input_file)
    # t0 = time.time()
    # puzzle = Puzzle(input_file)
    # result = TestUtils.check_result_no_arg("part2", 48,
    #                                        puzzle.run_program_part2)
    # print("part 2: execution time is ", time.time() - t0, " s")
    # print("part 2: The sum of the multiplications is", result)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 2: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result_no_arg("part2", 82045421,
                                           puzzle.run_program_part2)
    print("part 2: execution time is ", time.time() - t0, " s")
    print("part 2: The sum of the multiplications is", result)
