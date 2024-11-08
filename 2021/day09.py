import collections
import logging
import os
import time
from collections import namedtuple
from math import prod

from TestUtils import TestUtils


logger = logging.getLogger(__name__)

Point = namedtuple('Point', ['x', 'y'])


class Floor:

    def __init__(self, heightmap):
        self.heightmap = heightmap
        self.max_x = len(self.heightmap) - 1
        self.max_y = len(self.heightmap[0]) - 1

    def is_inside_map(self, p: Point):
        return True if (0 <= p.x <= self.max_x) and (0 <= p.y <= self.max_y) else False

    def build_neighbours(self, p: Point):
        all_neighbours = [Point(p.x - 1, p.y), Point(p.x, p.y - 1), Point(p.x, p.y + 1), Point(p.x + 1, p.y)]
        inside_neighbours = filter(lambda point: self.is_inside_map(point), all_neighbours)
        return inside_neighbours

    def is_low_point(self, p: Point):
        inside_neighbours = self.build_neighbours(p)
        is_high_point = any(self.heightmap[p.x][p.y] >= self.heightmap[r][c] for r, c in inside_neighbours)
        return not is_high_point

    def get_height(self, p: Point):
        return self.heightmap[p.x][p.y]

    def bfs(self, start: Point, height_limit=9):
        if self.get_height(start) == height_limit:
            return [], [start]
        visited, fifo, basin = set(), collections.deque(), []
        visited.add(start)
        fifo.append(start)
        basin.append(start)
        while fifo:
            current = fifo.popleft()
            for neighbour in self.build_neighbours(current):
                if neighbour not in visited:
                    visited.add(neighbour)
                    if self.get_height(neighbour) < height_limit:
                        fifo.append(neighbour)
                        basin.append(neighbour)
        return basin, visited

    def all_points(self):
        for x in range(self.max_x+1):
            for y in range(self.max_y+1):
                p = Point(x, y)
                yield p

    def find_basins(self):
        visited = set()
        basins = []
        for p in self.all_points():
            if p not in visited:
                basin, new_visited = self.bfs(p)
                visited.update(new_visited)
                basins.append(basin)
        return basins

    def find_low_points(self):
        # low_points = filter(lambda p: self.is_low_point(p),  self.all_points())
        low_points = [p for p in self.all_points() if self.is_low_point(p)]
        return low_points


class Puzzle:

    @staticmethod
    def to_puzzle_input(file):
        heightmap = []
        with open(file) as f:
            for line in f:
                row = list(map(lambda c: int(c), line.strip()))
                heightmap.append(row)
        return heightmap

    def __init__(self, file):
        self.floor = Floor(self.to_puzzle_input(file))

    def find_and_sum_risk_levels(self):
        low_points = self.floor.find_low_points()
        low_point_heights = [self.floor.get_height(p) for p in low_points]
        return sum(low_point_heights) + len(low_points)

    def find_basins(self):
        basins = self.floor.find_basins()
        basin_sizes = [len(basin) for basin in basins]
        basin_sizes.sort(reverse=True)
        return prod(basin_sizes[0:3])


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
    risk_levels_sum = TestUtils.check_result_no_arg("part1", 15, puzzle.find_and_sum_risk_levels)
    print("part 1: execution time is ", time.time() - t0, " s")
    print("part 1: the sum of the risk levels of all low points is  ", risk_levels_sum)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 1: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    risk_levels_sum = TestUtils.check_result_no_arg("part1", 480, puzzle.find_and_sum_risk_levels)
    print("part 1: execution time is ", time.time() - t0, " s")
    print("part 1: the sum of the risk levels of all low points is  ", risk_levels_sum)

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 2: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result_no_arg("part2", 1134, puzzle.find_basins)
    print("part 2: execution time is ", time.time() - t0, " s")
    print("part 2: the result of the multiplication together the sizes of the three largest basins is  ", result)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 2: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result_no_arg("part2", 1045660, puzzle.find_basins)
    print("part 2: execution time is ", time.time() - t0, " s")
    print("part 2: the result of the multiplication together the sizes of the three largest basins is  ", result)
