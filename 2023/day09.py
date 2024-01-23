import logging
import os
import time
from TestUtils import TestUtils

logger = logging.getLogger(__name__)


class Puzzle:
    @staticmethod
    def to_histories(file):
        # instructions = str()
        histories = []
        with open(file) as f:
            for line in f:
                history = list(map(lambda x: int(x), line.strip().split(' ')))
                histories.append(history)
        return histories

    def __init__(self, file):
        self.histories = self.to_histories(file)

    def find_extrapolate_value(self, history):
        ext_value = 0
        if any(history):
            new_history = [v2 - v1 for v1, v2 in zip(history, history[1:])]
            next_history_ext_value = self.find_extrapolate_value(new_history)
            ext_value = history[-1] + next_history_ext_value

        return ext_value

    def compute_sum_ext_values(self):
        values = [self.find_extrapolate_value(h) for h in self.histories]
        logger.warning(values)
        return sum(values)

    def find_extrapolate_value_part2(self, history):
        ext_value = 0
        if any(history):
            new_history = [v2 - v1 for v1, v2 in zip(history, history[1:])]
            next_history_ext_value = self.find_extrapolate_value_part2(new_history)
            ext_value = history[0] - next_history_ext_value

        return ext_value

    def compute_sum_ext_values_part2(self):
        values = [self.find_extrapolate_value_part2(h) for h in self.histories]
        logger.debug(values)
        return sum(values)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)
    TEST_DATA_DIR = os.path.join(os.getcwd(), 'data')
    INPUT_FILE_EXAMPLE = os.path.join(TEST_DATA_DIR, 'day09', 'example.txt')
    INPUT_FILE = os.path.join(TEST_DATA_DIR, 'day09', 'input.txt')

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 1: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    sum_ext_values = TestUtils.check_result_no_arg("part1", 114, puzzle.compute_sum_ext_values)
    print("part 1: execution time is ", time.time() - t0, " s")
    print("part 1: The sum of the extrapolated values is ", sum_ext_values)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 1: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    sum_ext_values = TestUtils.check_result_no_arg("part1", 1938800261, puzzle.compute_sum_ext_values)
    print("part 1: execution time is ", time.time() - t0, " s")
    print("part 1: The sum of the extrapolated values is ", sum_ext_values)

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 2: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    sum_ext_values = TestUtils.check_result_no_arg("part2", 2, puzzle.compute_sum_ext_values_part2)
    print("part 2: execution time is ", time.time() - t0, " s")
    print("part 2: The sum of the extrapolated values is ", sum_ext_values)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 2: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    sum_ext_values = TestUtils.check_result_no_arg("part2", 1112, puzzle.compute_sum_ext_values_part2)
    print("part 2: execution time is ", time.time() - t0, " s")
    print("part 2: The sum of the extrapolated values is ", sum_ext_values)
