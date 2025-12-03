import logging
import os
import time
from TestUtils import TestUtils

logger = logging.getLogger(__name__)


class Puzzle:

    @staticmethod
    def to_banks(file):
        banks = []
        with open(file) as f:
            for line in f:
                bank = [int(c) for c in line.strip()]
                banks.append(bank)
        return banks

    def __init__(self, file):
        self.banks = Puzzle.to_banks(file)

    @staticmethod
    def find_high_joltage_in_bank(bank):
        d1 = d2 = 0
        nb_batteries = len(bank)
        for idx_b, b_joltage in enumerate(bank):
            if (b_joltage > d1) & (idx_b < (nb_batteries - 1)):
                d1 = b_joltage
                d2 = 0
            elif b_joltage > d2:
                d2 = b_joltage
        return d1*10 + d2

    def compute_total_output_joltage(self):
        total = sum([self.find_high_joltage_in_bank(bank) for bank in self.banks])
        return total

    @staticmethod
    def find_high_joltage_in_bank_p2(bank):
        nb_batteries_on = 12
        digits = [0] * nb_batteries_on
        nb_batteries = len(bank)
        for idx_b, b_joltage in enumerate(bank):
            for idx_digit, digit in enumerate(digits):
                # check if this battery joltage is higher than prev or go to next digit
                idx_limit = nb_batteries - (nb_batteries_on - 1 - idx_digit)
                if (b_joltage > digit) & (idx_b < idx_limit):
                    digits[idx_digit] = b_joltage
                    # new high joltage is found , raz next digits
                    raz_idx_begin = idx_digit + 1
                    digits[raz_idx_begin:] = [0] * (nb_batteries_on - raz_idx_begin)
                    break
        digits_str = ''.join([str(d) for d in digits])
        return int(digits_str)

    def compute_total_output_joltage_p2(self):
        total = sum([self.find_high_joltage_in_bank_p2(bank) for bank in self.banks])
        return total


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING)
    TEST_DATA_DIR = os.path.join(os.getcwd(), 'data')
    INPUT_FILE_EXAMPLE = os.path.join(TEST_DATA_DIR, 'day03', 'example.txt')
    INPUT_FILE = os.path.join(TEST_DATA_DIR, 'day03', 'input.txt')

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 1: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result_no_arg(test_name="part1", expected_result=357,
                                           method_to_check=puzzle.compute_total_output_joltage)
    print("part 1: execution time is ", time.time() - t0, " s")
    print("part 1: The total output joltage is", result)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 1: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result_no_arg(test_name="part1", expected_result=17403,
                                           method_to_check=puzzle.compute_total_output_joltage)
    print("part 1: execution time is ", time.time() - t0, " s")
    print("part 1: The total output joltage is", result)

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 2: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result_no_arg(test_name="part2", expected_result=3121910778619,
                                           method_to_check=puzzle.compute_total_output_joltage_p2)
    print("part 2: execution time is ", time.time() - t0, " s")
    print("part 2: The total output joltage is", result)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 2: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result_no_arg(test_name="part2", expected_result=173416889848394,
                                           method_to_check=puzzle.compute_total_output_joltage_p2)
    print("part 2: execution time is ", time.time() - t0, " s")
    print("part 2: The total output joltage is", result)
