import logging
import os
import time


TEST_DATA_DIR = os.path.join(os.getcwd(), 'data')

logger = logging.getLogger(__name__)


class Puzzle:
    @staticmethod
    def to_strategy_guide(file):
        strategy_guide = []
        with open(file) as f:
            for line in f:
                opponent_shape, my_shape = line.strip().split()
                strategy_guide.append((opponent_shape, my_shape))
        return strategy_guide

    def __init__(self, file):
        self.strategy_guide = self.to_strategy_guide(file)
        self.rate_card = {('A', 'X'): 4, ('A', 'Y'): 8, ('A', 'Z'): 3,
                          ('B', 'X'): 1, ('B', 'Y'): 5, ('B', 'Z'): 9,
                          ('C', 'X'): 7, ('C', 'Y'): 2, ('C', 'Z'): 6}
        logger.debug(self.strategy_guide)

    def compute_total_score(self):
        points = map(lambda rd: self.rate_card[rd], self.strategy_guide)
        return sum(points)


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

    INPUT_FILE_EXAMPLE = os.path.join(TEST_DATA_DIR, 'day2', 'example.txt')
    INPUT_FILE = os.path.join(TEST_DATA_DIR, 'day2', 'input.txt')

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 1: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    total_score = TestUtils.check_result_no_arg("part1", 15, puzzle.compute_total_score)
    print("part 1: execution time is ", time.time() - start, " s")
    print("part 1: the total score is", total_score)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 1: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    total_score = TestUtils.check_result_no_arg("part1", 13484, puzzle.compute_total_score)
    print("part 1: execution time is ", time.time() - start, " s")
    print("part 1: the total score is", total_score)
