import logging
import os
import time
from TestUtils import TestUtils

logger = logging.getLogger(__name__)


class RangeMerger:

    @staticmethod
    def merge(initial_ranges):
        initial_ranges.sort()
        merged_ranges = [initial_ranges[0]]
        for curr in initial_ranges[1:]:
            curr_min, curr_max = curr
            last_min, last_max = merged_ranges[-1]
            # update last merged if overlap
            if curr_min <= last_max:
                last_max = max(last_max, curr_max)
                merged_ranges[-1] = [last_min, last_max]
            else:
                merged_ranges.append(curr)
        return merged_ranges


class Puzzle:

    @staticmethod
    def to_database(file):
        ranges = []
        with open(file) as f:
            for line in f:
                # empty line between ranges and IDs
                if line == '\n':
                    break
                else:
                    row = line.strip().split('-')
                    ranges.append([int(row[0]), int(row[1])])
            ids = [int(line.strip()) for line in f]
        return ranges, ids

    def __init__(self, file):
        self.ranges, self.IDs = Puzzle.to_database(file)
        self.merged_ranges = []

    def is_in_any_range(self, ingredient_id):
        return any(True for r_min, r_max in self.ranges if r_min <= ingredient_id <= r_max)

    def find_nb_of_fresh_av_ids(self):
        fresh_ids = [ingredient_id for ingredient_id in self.IDs if self.is_in_any_range(ingredient_id)]
        return len(fresh_ids)

    def find_nb_of_fresh_ingredient_ids(self):
        merged_ranged = RangeMerger.merge(self.ranges)
        nb = sum([max_r - min_r + 1 for min_r, max_r in merged_ranged])
        return nb


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    TEST_DATA_DIR = os.path.join(os.getcwd(), 'data')
    INPUT_FILE_EXAMPLE = os.path.join(TEST_DATA_DIR, 'day05', 'example.txt')
    INPUT_FILE = os.path.join(TEST_DATA_DIR, 'day05', 'input.txt')

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 1: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result_no_arg(test_name="part1", expected_result=3,
                                           method_to_check=puzzle.find_nb_of_fresh_av_ids)
    print("part 1: execution time is ", time.time() - t0, " s")
    print(f"part 1: The number of available ingredients IDs is {result}")

    print("-----------------")
    input_file = INPUT_FILE
    print("part 1: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result_no_arg(test_name="part1", expected_result=679,
                                           method_to_check=puzzle.find_nb_of_fresh_av_ids)
    print("part 1: execution time is ", time.time() - t0, " s")
    print(f"part 1: The number of available ingredients IDs is {result}")

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 2: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result_no_arg(test_name="part2", expected_result=14,
                                           method_to_check=puzzle.find_nb_of_fresh_ingredient_ids)
    print("part 2: execution time is ", time.time() - t0, " s")
    print(f"part 2: The number of fresh ingredients IDs is {result}")

    print("-----------------")
    input_file = INPUT_FILE
    print("part 2: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result_no_arg(test_name="part2", expected_result=358155203664116,
                                           method_to_check=puzzle.find_nb_of_fresh_ingredient_ids)
    print("part 2: execution time is ", time.time() - t0, " s")
    print(f"part 2: The number of fresh ingredients IDs is {result}")
