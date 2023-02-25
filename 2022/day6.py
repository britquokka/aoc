import collections
import logging
import os
import time

TEST_DATA_DIR = os.path.join(os.getcwd(), 'data')
logger = logging.getLogger(__name__)


class Puzzle:

    @staticmethod
    def to_datastream(file):
        with open(file) as f:
            for line in f:
                datastream = line.strip()
        return datastream

    def __init__(self, file):
        self.datastream = self.to_datastream(file)

    def find_separator(self, nb_distinct_char):
        idx_after_sep = None
        for i in range(0, len(self.datastream) - nb_distinct_char):
            extract = set(self.datastream[i:i+nb_distinct_char])
            if len(extract) == nb_distinct_char:
                idx_after_sep = i + nb_distinct_char
                break
        return idx_after_sep


class TestUtils:

    @staticmethod
    def check_result(test_name: str, expected_result: int, method_to_check, arg):
        current_result = method_to_check(arg)
        assert current_result == expected_result, test_name + ': ' + '(current_result:' + str(
            current_result) + ') != (expected_result:' + str(expected_result) + ')'
        return current_result


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING)

    INPUT_FILE_EXAMPLE = os.path.join(TEST_DATA_DIR, 'day6', 'example.txt')
    INPUT_FILE = os.path.join(TEST_DATA_DIR, 'day6', 'input.txt')

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 1: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    number = TestUtils.check_result("part1", 11, puzzle.find_separator, 4)
    print("part 1: execution time is ", time.time() - start, " s")
    print("part 1: the number of characters need to be processed before the first start-of-packet is", number)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 1: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    number = TestUtils.check_result("part1", 1235, puzzle.find_separator, 4)
    print("part 1: execution time is ", time.time() - start, " s")
    print("part 1: the number of characters need to be processed before the first start-of-packet is", number)

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 2: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    number = TestUtils.check_result("part1", 26, puzzle.find_separator, 14)
    print("part 2: execution time is ", time.time() - start, " s")
    print("part 2: the number of characters need to be processed before the first start-of-message is", number)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 2: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    number = TestUtils.check_result("part1", 3051, puzzle.find_separator, 14)
    print("part 2: execution time is ", time.time() - start, " s")
    print("part 2: the number of characters need to be processed before the first start-of-message is", number)
