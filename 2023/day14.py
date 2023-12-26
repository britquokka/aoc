import collections
import logging
import os
import time
from TestUtils import TestUtils
from collections import Counter

logger = logging.getLogger(__name__)


class Puzzle:

    @staticmethod
    def to_platform(file):
        columns = []
        with open(file) as f:
            nb_column = len(f.readline().strip())
            platform = [['#'] for i in range(nb_column)]
            f.seek(0)
            for line in f:
                row = str(line.strip())
                for item, column in zip(list(row), platform):
                    column.append(item)
            for column in platform:
                column.append('#')

        return platform

    def __init__(self, file):
        self.platform = self.to_platform(file)

    def compute_total_load(self):
        load = 0
        for column in self.platform:
            column.reverse()
            index_cube_rocks = [i for i, item in enumerate(column) if item == '#']
            for i in range(0, len(index_cube_rocks)-1, 1):
                begin = index_cube_rocks[i]
                end = index_cube_rocks[i + 1]
                nb_rounded_rock = column[begin:end].count('O')
                load += sum(range(end - nb_rounded_rock, end))
        return load


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    logging.basicConfig(level=logging.WARNING)
    TEST_DATA_DIR = os.path.join(os.getcwd(), 'data')
    INPUT_FILE_EXAMPLE = os.path.join(TEST_DATA_DIR, 'day14', 'example.txt')
    INPUT_FILE = os.path.join(TEST_DATA_DIR, 'day14', 'input.txt')

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 1: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    total_load = TestUtils.check_result_no_arg("part1", 136, puzzle.compute_total_load)
    print("part 1: execution time is ", time.time() - start, " s")
    print("part 1: The total load on the north support beams is  ", total_load)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 1: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    total_load = TestUtils.check_result_no_arg("part1", 109098, puzzle.compute_total_load)
    print("part 1: execution time is ", time.time() - start, " s")
    print("part 1: The total load on the north support beams is  ", total_load)