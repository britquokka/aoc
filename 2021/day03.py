import logging
import os
import time
from TestUtils import TestUtils

logger = logging.getLogger(__name__)


class Puzzle:

    @staticmethod
    def to_diagnostic_report(file):
        with open(file) as f:
            report = [line.strip() for line in f]
        return report

    def __init__(self, file):
        self.report = self.to_diagnostic_report(file)
        logger.debug(self.report)

    def compute_power_consumption(self):
        gamma_rate_string = self.find_gamma_rate(self.report)
        epsilon_rate_string = "".join([self.inv(c) for c in gamma_rate_string])
        gamma_rate = int(gamma_rate_string, 2)
        epsilon_rate = int(epsilon_rate_string, 2)
        logger.info(bin(gamma_rate))
        logger.info(bin(epsilon_rate))
        return gamma_rate * epsilon_rate

    @staticmethod
    def keep_numbers_by_column_value(wanted_bit, selected_column_values, numbers):
        # kept_numbers = []
        # for bit_num in range(len(selected_column_values)):
        #    if selected_column_values[bit_num] == wanted_bit:
        #        kept_numbers.append(numbers[bit_num])
        selected_rows = filter(lambda bit_num: selected_column_values[bit_num] == wanted_bit,
                               range(len(selected_column_values)))
        kept_numbers = [numbers[row_idx] for row_idx in selected_rows]
        return kept_numbers

    @staticmethod
    def filter_numbers(numbers: list, want_most_common_bit=True):
        filtered_numbers = numbers
        flag_exit_loop = False
        selected_column = 0
        while not flag_exit_loop:
            transposed_numbers = Puzzle.transpose(filtered_numbers)
            column_values = transposed_numbers[selected_column]
            most_common_bit = Puzzle.find_most_common_bit(column_values)
            wanted_bit = most_common_bit if want_most_common_bit else Puzzle.inv(most_common_bit)
            filtered_numbers = Puzzle.keep_numbers_by_column_value(wanted_bit, column_values, filtered_numbers)
            if len(filtered_numbers) == 1:
                flag_exit_loop = True
            selected_column += 1
        return filtered_numbers[0]

    def compute_life_support_rating(self):
        oxygen_str = self.filter_numbers(self.report)
        dioxygen_str = self.filter_numbers(self.report, False)
        oxygen_generator_rating = int(oxygen_str, 2)
        dioxygen_generator_rating = int(dioxygen_str, 2)
        logger.info(bin(oxygen_generator_rating))
        logger.info(bin(dioxygen_generator_rating))
        return oxygen_generator_rating * dioxygen_generator_rating

    @staticmethod
    def transpose(rows: list):
        return ["".join(col) for col in zip(*rows)]

    @staticmethod
    def find_most_common_bit(binary_string, preferred_bit='1'):
        bit_count = binary_string.count(preferred_bit)
        most_common_bit = preferred_bit if bit_count >= len(binary_string) / 2 else Puzzle.inv(preferred_bit)
        return most_common_bit

    @staticmethod
    def find_gamma_rate(report):
        transposed_report = Puzzle.transpose(report)
        game_rate_string = "".join([Puzzle.find_most_common_bit(line) for line in transposed_report])
        return game_rate_string

    @staticmethod
    def inv(c):
        return '0' if c == '1' else '1'


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    TEST_DATA_DIR = os.path.join(os.getcwd(), 'data')
    INPUT_FILE_EXAMPLE = os.path.join(TEST_DATA_DIR, 'day03', 'example.txt')
    INPUT_FILE = os.path.join(TEST_DATA_DIR, 'day03', 'input.txt')

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 1: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result_no_arg("part1", 198, puzzle.compute_power_consumption)
    print("part 1: execution time is ", time.time() - t0, " s")
    print("part 1: The power consumption of the submarine is ", result)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 1: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result_no_arg("part1", 2724524, puzzle.compute_power_consumption)
    print("part 1: execution time is ", time.time() - t0, " s")
    print("part 1: The power consumption of the submarine is ", result)

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 2: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result_no_arg("part2", 230, puzzle.compute_life_support_rating)
    print("part 2: execution time is ", time.time() - t0, " s")
    print("part 2: The power consumption of the submarine is ", result)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 2: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result_no_arg("part2", 2775870, puzzle.compute_life_support_rating)
    print("part 2: execution time is ", time.time() - t0, " s")
    print("part 2: The power consumption of the submarine is ", result)
