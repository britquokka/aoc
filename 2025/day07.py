import logging
import os
import time
from TestUtils import TestUtils

logger = logging.getLogger(__name__)


class TachyonManifold:

    def __init__(self, grid):
        self.grid = grid
        self.nb_rows = len(self.grid)
        self.nb_columns = len(self.grid[0])

    def all_coords(self):
        for r in range(self.nb_rows):
            for c in range(self.nb_columns):
                yield r, c

    def is_inside_grid(self, p):
        y, x = p
        return True if (0 <= x < self.nb_columns) and (0 <= y < self.nb_rows) else False

    def emit_beam(self, start, seen: set):
        y, x = start
        while self.is_inside_grid((y, x)):
            if self.grid[y][x] == '^':
                if (y, x) not in seen:
                    seen.add((y, x))
                    return 1 + self.emit_beam((y, x+1), seen) + self.emit_beam((y, x-1), seen)
                else:
                    return 0
            else:
                y += 1
        return 0

    def emit_beam_until_exit(self, start, nb_paths_by_splitter):
        y, x = start
        while self.is_inside_grid((y, x)):
            if self.grid[y][x] == '^':
                if (y, x) in nb_paths_by_splitter.keys():
                    return nb_paths_by_splitter[(y, x)]
                else:
                    nb_paths = (self.emit_beam_until_exit((y, x + 1), nb_paths_by_splitter)
                                + self.emit_beam_until_exit((y, x - 1), nb_paths_by_splitter))
                    nb_paths_by_splitter[(y, x)] = nb_paths
                    return nb_paths
            else:
                y += 1
        return 1

    def find_start(self):
        start = None
        for y, x in self.all_coords():
            if self.grid[y][x] == 'S':
                start = (y, x)
                break
        return start


class Puzzle:

    @staticmethod
    def to_grid(file):
        with open(file) as f:
            grid = [list(line.strip()) for line in f]
        return grid

    def __init__(self, file):
        self.tachyonManifold = TachyonManifold(Puzzle.to_grid(file))

    def find_nb_of_split(self):
        start = self.tachyonManifold.find_start()
        nb_splits = self.tachyonManifold.emit_beam(start, set())
        return nb_splits

    def find_nb_timelines(self):
        start = self.tachyonManifold.find_start()
        nb_paths_by_splitter = dict()
        nb_timelines = self.tachyonManifold.emit_beam_until_exit(start, nb_paths_by_splitter)
        return nb_timelines


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    TEST_DATA_DIR = os.path.join(os.getcwd(), 'data')
    INPUT_FILE_EXAMPLE = os.path.join(TEST_DATA_DIR, 'day07', 'example.txt')
    INPUT_FILE = os.path.join(TEST_DATA_DIR, 'day07', 'input.txt')

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 1: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result_no_arg(test_name="part1", expected_result=21,
                                           method_to_check=puzzle.find_nb_of_split)
    print("part 1: execution time is ", time.time() - t0, " s")
    print(f"part 1: The beam will be split {result} times")

    print("-----------------")
    input_file = INPUT_FILE
    print("part 1: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result_no_arg(test_name="part1", expected_result=1566,
                                           method_to_check=puzzle.find_nb_of_split)
    print("part 1: execution time is ", time.time() - t0, " s")
    print(f"part 1: The beam will be split {result} times")

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 2: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result_no_arg(test_name="part2", expected_result=40,
                                           method_to_check=puzzle.find_nb_timelines)
    print("part 2: execution time is ", time.time() - t0, " s")
    print(f"part 2: The number of different timelines is {result}")

    print("-----------------")
    input_file = INPUT_FILE
    print("part 2: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result_no_arg(test_name="part2", expected_result=5921061943075,
                                           method_to_check=puzzle.find_nb_timelines)
    print("part 2: execution time is ", time.time() - t0, " s")
    print(f"part 2: The number of different timelines is {result}")
