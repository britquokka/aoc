import logging
import os
import time
from TestUtils import TestUtils

logger = logging.getLogger(__name__)


class Puzzle:

    @staticmethod
    def to_rotations(file):
        with open(file) as f:
            rotations = [line.strip() for line in f]
        return rotations

    def __init__(self, file):
        self.rotations = Puzzle.to_rotations(file)

    def find_password(self):
        p = 50
        hundred_modulo_counter = 0

        for rotation in self.rotations:
            d = int(rotation[1:])
            p = (p - d) if rotation[0] == 'L' else (p + d)
            if p % 100 == 0:
                hundred_modulo_counter += 1

        return hundred_modulo_counter

    def find_password_p2(self):
        p = 50
        crossover_counter = 0

        for rotation in self.rotations:
            prev = p
            d = int(rotation[1:])
            crossover_counter = crossover_counter + d // 100
            remainder = d % 100
            if rotation[0] == 'L':
                p = p - remainder
                if (p <= 0) & (prev > 0):
                    crossover_counter += 1
            else:
                p = p + remainder
                if p >= 100:
                    crossover_counter += 1
            p = p % 100

        return crossover_counter


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING)
    TEST_DATA_DIR = os.path.join(os.getcwd(), 'data')
    INPUT_FILE_EXAMPLE = os.path.join(TEST_DATA_DIR, 'day01', 'example.txt')
    INPUT_FILE = os.path.join(TEST_DATA_DIR, 'day01', 'input.txt')

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 1: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result_no_arg(test_name="part1", expected_result=3,
                                           method_to_check=puzzle.find_password)
    print("part 1: execution time is ", time.time() - t0, " s")
    print("part 1: The password to open the door is", result)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 1: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result_no_arg(test_name="part1", expected_result=1076,
                                           method_to_check=puzzle.find_password)
    print("part 1: execution time is ", time.time() - t0, " s")
    print("part 1: The password to open the door is", result)

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 2: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result_no_arg(test_name="part2", expected_result=6,
                                           method_to_check=puzzle.find_password_p2)
    print("part 2: execution time is ", time.time() - t0, " s")
    print("part 2: Using password method 0x434C49434B, the password found to open the door is", result)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 2: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result_no_arg(test_name="part2", expected_result=6379,
                                           method_to_check=puzzle.find_password_p2)
    print("part 2: execution time is ", time.time() - t0, " s")
    print("part 2: Using password method 0x434C49434B, the password found to open the door is", result)
