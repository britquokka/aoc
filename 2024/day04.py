
import logging
import os
import time
from TestUtils import TestUtils


logger = logging.getLogger(__name__)


class Puzzle:

    @staticmethod
    def to_letter_grid(file):
        with open(file) as f:
            grid = [line.strip() for line in f]
        return grid

    def __init__(self, file):
        self.grid = Puzzle.to_letter_grid(file)
        self.nb_row = len(self.grid)
        self.nb_column = len(self.grid[0])
        self.directions = [(r, c) for r in range(-1, 2) for c in range(-1, 2)]
        self.xmas_word = 'XMAS'

    def is_inside_map(self, p):
        (r, c) = p
        return True if (0 <= r < self.nb_row) and (0 <= c < self.nb_column) else False

    def build_line(self, start, direction):
        (r, c) = start
        (dr, dc) = direction
        all_points = [(r + dr*d, c + dc*d) for d in range(len(self.xmas_word))]
        points = list(filter(lambda point: self.is_inside_map(point), all_points))
        return points

    def build_x_mas_line(self, start, direction):
        (r, c) = start
        (dr, dc) = direction
        all_points = [(r + dr * d, c + dc * d) for d in range(-1, 2)]
        points = list(filter(lambda point: self.is_inside_map(point), all_points))
        return points

    def build_candidate(self, start, direction):
        line = self.build_line(start, direction)
        letters = [self.grid[r][c] for r, c in line]
        candidate = "".join(letters)
        return candidate

    def find_xmas(self, start, direction):
        return self.build_candidate(start, direction) == self.xmas_word

    def build_x_mas_candidate(self, start, direction):
        line = self.build_x_mas_line(start, direction)
        letters = [self.grid[r][c] for r, c in line]
        candidate = "".join(letters)
        return candidate

    def find_x_mas(self, start):
        directions = [(1, 1), (-1, 1)]
        is_found = True
        for direction in directions:
            candidate = self.build_x_mas_candidate(start, direction)
            is_found &= candidate == 'MAS' or candidate == 'SAM'
        return is_found

    def count_xmas(self):
        all_start = [(r, c) for r in range(self.nb_row) for c in range(self.nb_column) if self.grid[r][c] == 'X']
        count = sum(self.find_xmas(start, direction) for direction in self.directions for start in all_start)
        return count

    def count_x_mas(self):
        all_start = [(r, c) for r in range(self.nb_row) for c in range(self.nb_column) if self.grid[r][c] == 'A']
        count = sum(self.find_x_mas(start) for start in all_start)
        return count


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING)
    TEST_DATA_DIR = os.path.join(os.getcwd(), 'data')
    INPUT_FILE_EXAMPLE = os.path.join(TEST_DATA_DIR, 'day04', 'example.txt')
    INPUT_FILE = os.path.join(TEST_DATA_DIR, 'day04', 'input.txt')

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 1: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result_no_arg("part1", 18,
                                           puzzle.count_xmas)
    print("part 1: execution time is ", time.time() - t0, " s")
    print("part 1:  The number of times XMAS appear is", result)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 1: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result_no_arg("part1", 2654,
                                           puzzle.count_xmas)
    print("part 1: execution time is ", time.time() - t0, " s")
    print("part 1: The number of times XMAS appear is", result)

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 2: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result_no_arg("part2", 9,
                                           puzzle.count_x_mas)
    print("part 2: execution time is ", time.time() - t0, " s")
    print("part 2: The number of times X-MAS appear is", result)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 2: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result_no_arg("part2", 1990,
                                           puzzle.count_x_mas)
    print("part 2: execution time is ", time.time() - t0, " s")
    print("part 2: The number of times X-MAS appear is", result)
