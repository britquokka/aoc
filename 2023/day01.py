import logging
import os
import time

TEST_DATA_DIR = os.path.join(os.getcwd(), 'data')
logger = logging.getLogger(__name__)


class Puzzle:
    digit_by_text = dict(one="o1e", two="t2o", three="t3e", four="f4r", five="f5e", six="s6x", seven="s7n", eight="e8t",
                         nine="n9e")

    @staticmethod
    def convert_text_to_digit(text: str) -> str:
        for digit_word, digit in Puzzle.digit_by_text.items():
            text = text.replace(digit_word, digit)
        return text

    @staticmethod
    def to_calibration_values(file, need_convert_text_to_digit):
        calibration_values = []
        with open(file) as f:
            for line in f:
                if need_convert_text_to_digit:
                    line = Puzzle.convert_text_to_digit(line)
                # List comprehension offers a shorter syntax when you want
                # to create a new list based on the values of an existing list
                row = [c for c in line if c.isdigit()]
                calibration_value = row[0]+row[-1]
                calibration_values.append(int(calibration_value))
        return calibration_values

    def __init__(self, file, need_convert_text_to_digit=False):
        self.calibration_values = []
        self.calibration_values = self.to_calibration_values(file, need_convert_text_to_digit)
        logger.debug(self.calibration_values)

    def sum_calibration_values(self):
        return sum(self.calibration_values)


class TestUtils:

    @staticmethod
    def check_result(test_name: str, expected_result: int, method_to_check, argv):
        current_result = method_to_check(argv)
        assert current_result == expected_result, test_name + ': ' + '(current_result:' + str(
            current_result) + ') != (expected_result:' + str(expected_result) + ')'
        return current_result

    @staticmethod
    def check_result_no_arg(test_name: str, expected_result: int, method_to_check):
        current_result = method_to_check()
        assert current_result == expected_result, test_name + ': ' + '(current_result:' + str(
            current_result) + ') != (expected_result:' + str(expected_result) + ')'
        return current_result


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING)

    INPUT_FILE_EXAMPLE = os.path.join(TEST_DATA_DIR, 'day01', 'example.txt')
    INPUT_FILE_EXAMPLE_PART2 = os.path.join(TEST_DATA_DIR, 'day01', 'example_part2.txt')
    INPUT_FILE = os.path.join(TEST_DATA_DIR, 'day01', 'input.txt')

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 1: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    calibration_values_sum = TestUtils.check_result_no_arg("part1", 142, puzzle.sum_calibration_values)
    print("part 1: execution time is ", time.time() - start, " s")
    print("part 1: the sum of all the calibration values is ", calibration_values_sum)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 1: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    calibration_values_sum = TestUtils.check_result_no_arg("part1", 53334, puzzle.sum_calibration_values)
    print("part 1: execution time is ", time.time() - start, " s")
    print("part 1: the sum of all the calibration values is ", calibration_values_sum)

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE_PART2
    print("part 2: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file, True)
    calibration_values_sum = TestUtils.check_result_no_arg("part2", 281, puzzle.sum_calibration_values)
    print("part 2: execution time is ", time.time() - start, " s")
    print("part 2: the sum of all the calibration values is ", calibration_values_sum)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 2: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file, True)
    calibration_values_sum = TestUtils.check_result_no_arg("part2", 52834, puzzle.sum_calibration_values)
    print("part 2: execution time is ", time.time() - start, " s")
    print("part 2: the sum of all the calibration values is ", calibration_values_sum)
