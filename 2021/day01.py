import itertools
import logging
import os
import time
from TestUtils import TestUtils

logger = logging.getLogger(__name__)


class Puzzle:
    @staticmethod
    def to_depths(file):
        depths = []
        with open(file) as f:
            #    for line in f:
            #        depths.append(int(line.strip()))
            # or    depths = list(map(int, f))
            depths = [int(value) for value in f]
        return depths

    def __init__(self, file):
        self.depths = self.to_depths(file)
        logger.debug(self.depths)

    @staticmethod
    def count_if_larger_than_previous(results):
        is_larger_results = [a < b for a, b in itertools.pairwise(results)]
        count_larger = is_larger_results.count(True)
        return count_larger

    @staticmethod
    def count_if_larger_than_previous_bis(results):
        is_larger_results = [True for a, b in itertools.pairwise(results) if a < b]
        return len(is_larger_results)

    @staticmethod
    def count_if_larger_than_previous_other(results):
        # True is evaluated to 1 in sum
        count_larger = sum(a < b for a, b in itertools.pairwise(results))
        return count_larger

    def count_larger_measurement(self):
        return self.count_if_larger_than_previous_other(self.depths)

    def count_larger_sum(self):
        three_wise_list = [self.depths[i:i + 3] for i in range(len(self.depths) - 2)]
        three_wise_sums = [sum(three_wise) for three_wise in three_wise_list]
        return self.count_if_larger_than_previous(three_wise_sums)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    TEST_DATA_DIR = os.path.join(os.getcwd(), 'data')
    INPUT_FILE_EXAMPLE = os.path.join(TEST_DATA_DIR, 'day01', 'example.txt')
    INPUT_FILE = os.path.join(TEST_DATA_DIR, 'day01', 'input.txt')

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 1: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    count = TestUtils.check_result_no_arg("part1", 7, puzzle.count_larger_measurement)
    print("part 1: execution time is ", time.time() - t0, " s")
    print("part 1: The number of larger measurement than previous is ", count)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 1: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    count = TestUtils.check_result_no_arg("part1", 1564, puzzle.count_larger_measurement)
    print("part 1: execution time is ", time.time() - t0, " s")
    print("part 1: The number of larger measurement than previous is ", count)

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 2: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    count = TestUtils.check_result_no_arg("part1", 5, puzzle.count_larger_sum)
    print("part 2: execution time is ", time.time() - t0, " s")
    print("part 2: The number of larger three-wise sum than previous is ", count)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 2: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    count = TestUtils.check_result_no_arg("part1", 1611, puzzle.count_larger_sum)
    print("part 2: execution time is ", time.time() - t0, " s")
    print("part 2: The number of larger three-wise sum than previous is ", count)
