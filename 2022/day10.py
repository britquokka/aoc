import collections
import logging
import os
import time
import math

TEST_DATA_DIR = os.path.join(os.getcwd(), 'data')

logger = logging.getLogger(__name__)


class Crt:

    def __init__(self, wide):
        self.wide = wide
        self.crt = []
        self.current_row = []

    def draw_pixel(self, cycle, x):
        position = (cycle - 1) % self.wide
        if position == 0:
            self.current_row = []
            self.crt.append(self.current_row)
        if x - 1 <= position <= x + 1:
            self.current_row.append("#")
        else:
            self.current_row.append(".")

    def display(self):
        for row in self.crt:
            print(row)


class Puzzle:
    nb_cycle_by_instruction = {'noop': 1, 'addx': 2}

    @staticmethod
    def to_instructions(file):
        instructions = []
        with open(file) as f:
            for line in f:
                row = line.strip().split()
                if row[0] == 'noop':
                    instruction = [row[0]]
                else:
                    instruction = [row[0], int(row[1])]
                instructions.append(instruction)
        return instructions

    def __init__(self, file):
        self.instructions = self.to_instructions(file)

    def sum_signal_strengths(self):
        x = 1
        cycle = sum_s = 0
        next_sample_time = 20
        sample_period = 40

        # check at each instruction but increment x after check
        for instruction in self.instructions:
            cycle += Puzzle.nb_cycle_by_instruction[instruction[0]]
            if cycle >= next_sample_time:
                sum_s += x * next_sample_time
                next_sample_time += sample_period
            if instruction[0] == 'addx':
                x += instruction[1]

        return sum_s

    def display_crt(self):
        x = 1
        cycle = 0
        crt = Crt(40)

        for instruction in self.instructions:
            cycle += 1
            crt.draw_pixel(cycle, x)
            if instruction[0] == 'addx':
                cycle += 1
                crt.draw_pixel(cycle, x)
                x += instruction[1]

        crt.display()

        return 0


class TestUtils:

    @staticmethod
    def check_result(test_name: str, expected_result: str, method_to_check, argv):
        current_result = method_to_check(argv)
        assert current_result == expected_result, test_name + ': ' + '(current_result:' + str(
            current_result) + ') != (expected_result:' + str(expected_result) + ')'
        return current_result

    @staticmethod
    def check_result_no_arg(test_name: str, expected_result: str, method_to_check):
        current_result = method_to_check()
        assert current_result == expected_result, test_name + ': ' + '(current_result:' + str(
            current_result) + ') != (expected_result:' + str(expected_result) + ')'
        return current_result


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING)

    INPUT_FILE_EXAMPLE = os.path.join(TEST_DATA_DIR, 'day10', 'example.txt')
    INPUT_FILE = os.path.join(TEST_DATA_DIR, 'day10', 'input.txt')

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 1: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    signal_strengths_sum = TestUtils.check_result_no_arg("part1", 13140, puzzle.sum_signal_strengths)
    print("part 1: execution time is ", time.time() - start, " s")
    print("part 1: the sum of these six signal strengths is ", signal_strengths_sum)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 1: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    signal_strengths_sum = TestUtils.check_result_no_arg("part1", 13680, puzzle.sum_signal_strengths)
    print("part 1: execution time is ", time.time() - start, " s")
    print("part 1: the sum of these six signal strengths is ", signal_strengths_sum)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 2: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    signal_strengths_sum = TestUtils.check_result_no_arg("part2", 0, puzzle.display_crt)
    print("part 2: execution time is ", time.time() - start, " s")
