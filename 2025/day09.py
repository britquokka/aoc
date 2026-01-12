import logging
import os
import time
from itertools import combinations

from TestUtils import TestUtils

logger = logging.getLogger(__name__)


class Puzzle:

    @staticmethod
    def to_red_tiles(file):
        tiles = []
        with open(file) as f:
            for line in f:
                x, y = line.strip().split(',')
                tiles.append((int(x), int(y)))
        return tiles

    def __init__(self, file):
        self.red_tiles = Puzzle.to_red_tiles(file)

    @staticmethod
    def compute_rectangle_size(p1: tuple, p2: tuple):
        return (abs(p2[0] - p1[0]) + 1) * (abs(p2[1] - p1[1]) + 1)

    def find_largest_rectangle_bis(self):
        area_size = 0
        for p1, p2 in combinations(self.red_tiles, 2):
            current_area_size = (abs(p2[0] - p1[0]) + 1) * (abs(p2[1] - p1[1]) + 1)
            area_size = max(current_area_size, area_size)
        return area_size

    def find_largest_rectangle(self):
        return max([Puzzle.compute_rectangle_size(p1, p2) for p1, p2 in combinations(self.red_tiles, 2)])


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    TEST_DATA_DIR = os.path.join(os.getcwd(), 'data')
    INPUT_FILE_EXAMPLE = os.path.join(TEST_DATA_DIR, 'day09', 'example.txt')
    INPUT_FILE = os.path.join(TEST_DATA_DIR, 'day09', 'input.txt')

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 1: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result_no_arg(test_name="part1", expected_result=50,
                                           method_to_check=puzzle.find_largest_rectangle)
    print("part 1: execution time is ", time.time() - t0, " s")
    print(f"part 1: the largest area of any rectangle you can make is {result}")

    print("-----------------")
    input_file = INPUT_FILE
    print("part 1: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result_no_arg(test_name="part1", expected_result=4771508457,
                                           method_to_check=puzzle.find_largest_rectangle)
    print("part 1: execution time is ", time.time() - t0, " s")
    print(f"part 1: the largest area of any rectangle you can make is {result}")
