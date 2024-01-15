import collections
import logging
import os
import time
from TestUtils import TestUtils

logger = logging.getLogger(__name__)


class Puzzle:
    @staticmethod
    def to_grid(file):
        grid = []
        with open(file) as f:
            nb_column = len(f.readline().strip()) + 2
            initial_row = ['#'] * nb_column
            grid.append(initial_row)
            f.seek(0)
            for line in f:
                row = '#' + str(line.strip()) + '#'
                grid.append([c for c in row])
            grid.append(initial_row.copy())
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

    def build_neighbours(self, p):
        (y, x) = p
        neighbours = []
        all_neighbours = [(y - 1, x), (y, x + 1), (y + 1, x), (y, x - 1)]
        for r, c in all_neighbours:
            tile = self.grid[r][c]
            if tile != '#':
                neighbours.append((r, c))
        return neighbours

    def find_num_garden_plots(self, nb_steps):
        reachable = self.dfs(self.start, nb_steps)
        return len(reachable)

    def dfs(self, start, step_target):
        nb_path, step = 0, 0
        reachable, visited = set(), set()
        fifo = collections.deque()
        start_state = (start, step)
        visited.add(start_state)
        fifo.append(start_state)
        while fifo:
            node, step = fifo.pop()
            step += 1
            if step <= step_target:
                neighbours = self.build_neighbours(node)
                if step == step_target:
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
