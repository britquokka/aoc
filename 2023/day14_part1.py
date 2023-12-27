import logging
import os
import time
from TestUtils import TestUtils


logger = logging.getLogger(__name__)


class Puzzle:

    @staticmethod
    def to_platform(file):
        platform = []
        with open(file) as f:
            nb_column = len(f.readline().strip()) + 2
            initial_row = ['#'] * nb_column
            platform.append(initial_row)
            f.seek(0)
            for line in f:
                row = '#' + str(line.strip()) + '#'
                platform.append([c for c in row])
            platform.append(initial_row.copy())

        return platform

    @staticmethod
    def transpose(matrix: list):
        result = [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]
        return result

    def __init__(self, file):
        self.platform = self.to_platform(file)

    def compute_total_load(self):
        # transpose row into column
        platform = self.transpose(self.platform)
        load = 0
        for column in platform:
            column.reverse()
            index_cube_rocks = [i for i, item in enumerate(column) if item == '#']
            for i in range(0, len(index_cube_rocks) - 1, 1):
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


