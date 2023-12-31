from dataclasses import dataclass
import logging
import os
import time
from itertools import combinations
from typing import List
import bisect

from TestUtils import TestUtils

logger = logging.getLogger(__name__)


@dataclass
class Image:
    galaxies_coords: list
    space_y_coords: list
    space_x_coords: list

    def compute_galaxy_real_coords(self, expansion_value):
        real_coords = []
        for y, x in self.galaxies_coords:
            # bisect idx gives the number of space expansion before the galaxy
            idx_x = bisect.bisect_right(self.space_x_coords, x)
            idx_y = bisect.bisect_right(self.space_y_coords, y)
            real_x = x + (idx_x * (expansion_value-1))
            real_y = y + (idx_y * (expansion_value-1))
            real_coords.append((real_y, real_x))
        return real_coords


class Puzzle:

    @staticmethod
    def to_galaxies_coords(rows: list):
        galaxies_coords = []
        for y, line in enumerate(rows):
            for x, c in enumerate(line):
                if c == '#':
                    galaxies_coords.append((y, x))
        return galaxies_coords

    @staticmethod
    def find_space_expansion_coords(image_lines: List[str]):
        space_coords = [y for y, line in enumerate(image_lines) if line.find('#') < 0]
        return space_coords

    @staticmethod
    def transpose(rows: list):
        return ["".join(col) for col in zip(*rows)]

    @staticmethod
    def to_image(file):
        with open(file) as f:
            rows = f.read().splitlines()
            columns = Puzzle.transpose(rows)
        galaxies_coords = Puzzle.to_galaxies_coords(rows)
        space_y_coords = Puzzle.find_space_expansion_coords(rows)
        space_x_coords = Puzzle.find_space_expansion_coords(columns)
        return Image(galaxies_coords, space_y_coords, space_x_coords)

    def __init__(self, file):
        self.image = self.to_image(file)

    @staticmethod
    def get_path_length(src: tuple, dst: tuple):
        return abs(dst[0]-src[0]) + abs(dst[1]-src[1])

    def compute_sum_of_path_between_galaxy(self, expansion_value=2):
        g_real_coords = self.image.compute_galaxy_real_coords(expansion_value)
        # for g1, g2 in combinations(g_real_coords, 2):
        #    total += Puzzle.get_path_length(g1, g2)
        # or
        total = sum([Puzzle.get_path_length(g1, g2) for g1, g2 in combinations(g_real_coords, 2)])
        return total


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING)
    TEST_DATA_DIR = os.path.join(os.getcwd(), 'data')
    INPUT_FILE_EXAMPLE = os.path.join(TEST_DATA_DIR, 'day11', 'example.txt')
    INPUT_FILE = os.path.join(TEST_DATA_DIR, 'day11', 'input.txt')

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 1: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    shortest_paths_sum = TestUtils.check_result_no_arg("part1", 374, puzzle.compute_sum_of_path_between_galaxy)
    print("part 1: execution time is ", time.time() - start, " s")
    print("part 1: The sum of the path length between galaxies is  ", shortest_paths_sum)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 1: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    shortest_paths_sum = TestUtils.check_result_no_arg("part1", 9418609, puzzle.compute_sum_of_path_between_galaxy)
    print("part 1: execution time is ", time.time() - start, " s")
    print("part 1: The sum of the path length between galaxies is  ", shortest_paths_sum)

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 2: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    shortest_paths_sum = TestUtils.check_result("part2", 1030, puzzle.compute_sum_of_path_between_galaxy, 10)
    print("part 2: execution time is ", time.time() - start, " s")
    print("part 2: The sum of the path length between galaxies is  ", shortest_paths_sum)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 2: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    shortest_paths_sum = TestUtils.check_result("part2", 593821230983,
                                                puzzle.compute_sum_of_path_between_galaxy, 1000000)
    print("part 2: execution time is ", time.time() - start, " s")
    print("part 2: The sum of the path length between galaxies is  ", shortest_paths_sum)
