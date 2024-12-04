import logging
import os
import time
from TestUtils import TestUtils
from collections import namedtuple
import re

logger = logging.getLogger(__name__)

Instruction = namedtuple('Instruction', ['name', 'operands'])


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

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE_PART2
    print("part 2: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result_no_arg("part2", 48,
                                           puzzle.run_program_part2)
    print("part 2: execution time is ", time.time() - t0, " s")
    print("part 2: the sum of the multiplications is", result)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 2: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result_no_arg("part2", 82045421,
                                           puzzle.run_program_part2)
    print("part 2: execution time is ", time.time() - t0, " s")
    print("part 2: The sum of the multiplications is", result)
