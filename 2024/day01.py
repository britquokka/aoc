import logging
import os
import time
from TestUtils import TestUtils


logger = logging.getLogger(__name__)


class Puzzle:

    @staticmethod
    def to_ids(file):
        left_ids = []
        right_ids = []
        with open(file) as f:
            for line in f:
                l, r = line.strip().split()
                left_ids.append(int(l))
                right_ids.append(int(r))
        return left_ids, right_ids

    def __init__(self, file):
        self.left_ids, self.right_ids = Puzzle.to_ids(file)

    def compute_total_distance_between_list(self):
        self.left_ids.sort()
        self.right_ids.sort()
        distances = [abs(right - left) for left, right in zip(self.left_ids, self.right_ids)]
        return sum(distances)

    def compute_similarity_score(self):
        scores = [left_id * self.right_ids.count(left_id) for left_id in self.left_ids]
        return sum(scores)


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
    result = TestUtils.check_result_no_arg("part1", 11,
                                           puzzle.compute_total_distance_between_list)
    print("part 1: execution time is ", time.time() - t0, " s")
    print("part 1: The total distance between the list error is", result)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 1: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result_no_arg("part1", 1765812,
                                           puzzle.compute_total_distance_between_list)
    print("part 1: execution time is ", time.time() - t0, " s")
    print("part 1: The total distance between the list error is", result)

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 1: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result_no_arg("part1", 31,
                                           puzzle.compute_similarity_score)
    print("part 1: execution time is ", time.time() - t0, " s")
    print("part 1: The similarity score between the list error is", result)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 2: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result_no_arg("part1", 20520794,
                                           puzzle.compute_similarity_score)
    print("part 2: execution time is ", time.time() - t0, " s")
    print("part 2: The similarity score between the list error is", result)
