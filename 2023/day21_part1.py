import collections
import logging
import os
import time
from TestUtils import TestUtils

logger = logging.getLogger(__name__)


class Puzzle:
    @staticmethod
    def to_grid(file):
        with open(file) as f:
            grid = f.read().splitlines()
        return grid

    @staticmethod
    def to_garden(file):
        start = None
        grid = Puzzle.to_grid(file)
        for y, row in enumerate(grid):
            for x, tile in enumerate(row):
                if tile == 'S':
                    start = (y, x)
        return grid, start

    def __init__(self, file):
        self.grid, self.start = self.to_garden(file)
        self.nb_row = len(self.grid)
        self.nb_column = len(self.grid[0])

    def build_neighbours(self, p):
        (y, x) = p
        neighbours = []
        all_neighbours = [(y - 1, x), (y, x + 1), (y + 1, x), (y, x - 1)]
        for r, c in all_neighbours:
            if (0 <= r < self.nb_row) and (0 <= c < self.nb_column):
                tile = self.grid[r][c]
                if tile != '#':
                    neighbours.append((r, c))
        return neighbours

    def find_num_garden_plots(self, nb_steps):
        reachable = self.dfs(self.start, nb_steps)
        return len(reachable)

    def dfs(self, start, step_target):
        nb_path, step = 0, step_target
        reachable, visited = set(), set()
        fifo = collections.deque()
        start_state = (start, step)
        visited.add(start_state)
        fifo.append(start_state)
        while fifo:
            node, step = fifo.pop()
            step -= 1
            if step >= 0:
                neighbours = self.build_neighbours(node)
                if step == 0:
                    nb_path += len(neighbours)
                    reachable.update(neighbours)
                else:
                    for neighbour in neighbours:
                        next_state = (neighbour, step)
                        if next_state not in visited:
                            visited.add(next_state)
                            fifo.append(next_state)
        logger.info("nb_path:%d", nb_path)
        return reachable


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)
    TEST_DATA_DIR = os.path.join(os.getcwd(), 'data')
    INPUT_FILE_EXAMPLE = os.path.join(TEST_DATA_DIR, 'day21', 'example.txt')
    INPUT_FILE_EXAMPLE_PART2 = os.path.join(TEST_DATA_DIR, 'day21', 'example_part2.txt')
    INPUT_FILE = os.path.join(TEST_DATA_DIR, 'day21', 'input.txt')

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 1: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    num_garden_plots = TestUtils.check_result("part1", 16, puzzle.find_num_garden_plots, 6)
    print("part 1: execution time is ", time.time() - t0, " s")
    print("part 1: The number of reachable garden plots in 6 steps is ", num_garden_plots)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 1: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    num_garden_plots = TestUtils.check_result("part1", 3709, puzzle.find_num_garden_plots, 64)
    print("part 1: execution time is ", time.time() - t0, " s")
    print("part 1: The number of reachable garden plots in 64 steps is ", num_garden_plots)
