import collections
import logging
import os
import time
from enum import IntEnum
from collections import defaultdict
from TestUtils import TestUtils


logger = logging.getLogger(__name__)


class EPlotSide(IntEnum):
    N = 0
    E = 1
    S = 2
    W = 3


class Garden:

    def __init__(self, grid):
        self.grid = grid
        self.nb_rows = len(self.grid)
        self.nb_columns = len(self.grid[0])

    @staticmethod
    def count_initial_fence(side, plot, left_plot, fences_by_plot):
        count = 0
        # if left plot has not a fence on the same side then it is a new side
        if side in fences_by_plot[plot]:
            left_sides = fences_by_plot.get(left_plot)
            if left_sides is None:
                count += 1
            elif side not in left_sides:
                count += 1
        return count

    @staticmethod
    def count_sides(plot, fences_by_plot):
        nb_sides = 0
        r, c = plot
        # count if it is the first fence on a region side ( left plot shall have no fence on the same side)
        nb_sides += Garden.count_initial_fence(EPlotSide.N, (r, c), (r, c - 1), fences_by_plot)
        nb_sides += Garden.count_initial_fence(EPlotSide.E, (r, c), (r - 1, c), fences_by_plot)
        nb_sides += Garden.count_initial_fence(EPlotSide.S, (r, c), (r, c + 1), fences_by_plot)
        nb_sides += Garden.count_initial_fence(EPlotSide.W, (r, c), (r + 1, c), fences_by_plot)
        return nb_sides

    def bfs(self, start):
        r0, c0 = start
        plant_type = self.grid[r0][c0]
        visited = set()
        visited.add(start)
        fences_by_plot = defaultdict(set)
        fifo = collections.deque([start])
        while fifo:
            r0, c0 = plot = fifo.popleft()
            all_neighbours = [(r0-1, c0), (r0, c0+1), (r0+1, c0), (r0, c0-1)]
            for plot_side, (r, c) in zip(list(EPlotSide), all_neighbours):
                if (0 <= r < self.nb_rows) and (0 <= c < self.nb_columns):
                    if self.grid[r][c] == plant_type:
                        if (r, c) not in visited:
                            fifo.append((r, c))
                            visited.add((r, c))
                    else:
                        fences_by_plot[plot].add(plot_side)
                else:
                    fences_by_plot[plot].add(plot_side)

        nb_fences = sum([len(fences) for fences in fences_by_plot.values()])
        nb_sides = sum([self.count_sides(plot, fences_by_plot) for plot in fences_by_plot.keys()])

        return visited, nb_fences, nb_sides

    def all_plots(self):
        for r in range(self.nb_rows):
            for c in range(self.nb_columns):
                yield r, c

    def find_all_regions(self):
        seen = set()
        regions = []
        for plot in self.all_plots():
            if plot not in seen:
                region, nb_fences, nb_sides = self.bfs(plot)
                seen = seen.union(region)
                regions.append((region, nb_fences, nb_sides))
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
        price = sum(len(region) * nb_fences for region, nb_fences, _ in regions)
        return price

    def compute_new_fencing_price(self):
        regions = self.garden.find_all_regions()
        price = sum(len(region) * nb_sides for region, nb_fences, nb_sides in regions)
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

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 2: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result_no_arg("part2", 1206,
                                           puzzle.compute_new_fencing_price)
    print("part 2: execution time is ", time.time() - t0, " s")
    print("part 2: The new total price of fencing all regions is", result)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 2: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result_no_arg("part2", 872382,
                                           puzzle.compute_new_fencing_price)
    print("part 2: execution time is ", time.time() - t0, " s")
    print("part 2: The new total price of fencing all regions is", result)
