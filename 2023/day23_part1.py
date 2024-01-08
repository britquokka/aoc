import collections
import logging
import os
import time
from TestUtils import TestUtils
from enum import IntEnum

logger = logging.getLogger(__name__)


class Dir(IntEnum):
    N = 0
    E = 1
    S = 2
    W = 3


class Puzzle:

    @staticmethod
    def to_grid(file):
        with open(file) as f:
            grid = f.read().splitlines()
        return grid

    def __init__(self, file, allow_climbing=False):
        self.grid = self.to_grid(file)
        self.begin = (0, 1)
        self.end = (len(self.grid) - 1, len(self.grid[0]) - 2)
        self.allow_climbing = allow_climbing

    def build_neighbours(self, node):
        (y, x) = node
        neighbours = set()
        all_neighbours = [(y - 1, x), (y, x + 1), (y + 1, x), (y, x - 1)]
        for direction in Dir:
            r, c = neighbour = all_neighbours[direction.value]
            tile = self.grid[r][c]
            if self.allow_climbing:
                if tile in '.>v':
                    neighbours.add(neighbour)
            else:
                if tile == '.':
                    neighbours.add(neighbour)
                elif tile == '>' and direction == Dir.E:
                    neighbours.add(neighbour)
                elif tile == 'v' and direction == Dir.S:
                    neighbours.add(neighbour)

        return neighbours

    def dfs(self):
        seen = set()
        max_s = 0
        lifo = collections.deque()

        # go to south
        seen.add(self.begin)
        y, x = self.begin
        first_node = (y + 1, x)
        seen.add(first_node)
        lifo.append((first_node, seen))
        while lifo:
            (node, seen) = lifo.pop()
            if node == self.end:
                max_s = max(max_s, len(seen))
            else:
                neighbours = self.build_neighbours(node)
                for neighbour in neighbours:
                    if neighbour not in seen:
                        if len(neighbours) > 1:
                            seen = seen.copy()
                        seen.add(node)
                        lifo.append((neighbour, seen))
        return max_s

    def find_max_steps(self):
        return self.dfs()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    logging.basicConfig(level=logging.WARNING)
    TEST_DATA_DIR = os.path.join(os.getcwd(), 'data')
    INPUT_FILE_EXAMPLE = os.path.join(TEST_DATA_DIR, 'day23', 'example.txt')
    INPUT_FILE_EXAMPLE_PART2 = os.path.join(TEST_DATA_DIR, 'day23', 'example_part2.txt')
    INPUT_FILE = os.path.join(TEST_DATA_DIR, 'day23', 'input.txt')

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 1: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    max_steps = TestUtils.check_result_no_arg("part1", 94, puzzle.find_max_steps)
    print("part 1: execution time is ", time.time() - start, " s")
    print("part 1: The number of the steps of the longest hike is ", max_steps)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 1: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    max_steps = TestUtils.check_result_no_arg("part1", 1930, puzzle.find_max_steps)
    print("part 1: execution time is ", time.time() - start, " s")
    print("part 1: The number of the steps of the longest hike is ", max_steps)

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 2: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file, allow_climbing=True)
    max_steps = TestUtils.check_result_no_arg("part2", 154, puzzle.find_max_steps)
    print("part 2: execution time is ", time.time() - start, " s")
    print("part 2: The number of the steps of the longest hike is ", max_steps)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 2: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file, allow_climbing=True)
    max_steps = TestUtils.check_result_no_arg("part2", 154, puzzle.find_max_steps)
    print("part 2: execution time is ", time.time() - start, " s")
    print("part 2: The number of the steps of the longest hike is ", max_steps)