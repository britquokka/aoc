import collections
import logging
import os
import time
from TestUtils import TestUtils


logger = logging.getLogger(__name__)


class Garden:

    def __init__(self, grid):
        self.grid = grid
        self.nb_rows = len(self.grid)
        self.nb_columns = len(self.grid[0])

    def is_inside(self, p):
        (r, c) = p
        return True if (0 <= r < self.nb_rows) and (0 <= c < self.nb_columns) else False

    def build_neighbours(self, p):
        (r0, c0) = p
        all_neighbours = [(r0 - 1, c0), (r0, c0 + 1), (r0 + 1, c0), (r0, c0 - 1)]
        inside_neighbours = filter(lambda point: self.is_inside(point), all_neighbours)
        return list(inside_neighbours)

    def bfs(self, start):
        r0, c0 = start
        plant_type = self.grid[r0][c0]
        visited = set()
        visited.add(start)
        fences = 0
        fifo = collections.deque([start])
        while fifo:
            plot = fifo.popleft()
            neighbours = self.build_neighbours(plot)
            if len(neighbours) < 4:
                fences += 4 - len(neighbours)
            for neighbour in neighbours:
                r, c = neighbour
                if self.grid[r][c] == plant_type:
                    if neighbour not in visited:
                        fifo.append(neighbour)
                        visited.add(neighbour)
                else:
                    fences += 1
        return visited, fences

    def all_plots(self):
        for r in range(self.nb_rows):
            for c in range(self.nb_columns):
                yield r, c

    def find_all_regions(self):
        seen = set()
        regions = []
        for plot in self.all_plots():
            if plot not in seen:
                region, fences = self.bfs(plot)
                seen = seen.union(region)
                regions.append((region, fences))
        return regions


class Puzzle:

    @staticmethod
    def to_garden_grid(file):
        with open(file) as f:
            grid = [line.strip() for line in f]
        return grid

    def __init__(self, file):
        self.garden = Garden(Puzzle.to_garden_grid(file))

    def compute_fencing_price(self):
        regions = self.garden.find_all_regions()
        price = sum(len(region) * fences for region, fences in regions)
        return price


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING)
    TEST_DATA_DIR = os.path.join(os.getcwd(), 'data')
    INPUT_FILE_EXAMPLE = os.path.join(TEST_DATA_DIR, 'day12', 'example.txt')
    INPUT_FILE = os.path.join(TEST_DATA_DIR, 'day12', 'input.txt')

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 1: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result_no_arg("part1", 1930,
                                           puzzle.compute_fencing_price)
    print("part 1: execution time is ", time.time() - t0, " s")
    print("part 1: The total price of fencing all regions is", result)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 1: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result_no_arg("part1", 1456082,
                                           puzzle.compute_fencing_price)
    print("part 1: execution time is ", time.time() - t0, " s")
    print("part 1: The total price of fencing all regions is", result)
