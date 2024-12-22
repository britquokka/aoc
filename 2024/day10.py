import collections
import logging
import os
import time
from TestUtils import TestUtils


logger = logging.getLogger(__name__)


class Puzzle:

    @staticmethod
    def to_grid(file):
        reports = []
        with open(file) as f:
            for line in f:
                row = [int(c) for c in list(line.strip())]
                reports.append(row)
        return reports

    def __init__(self, file):
        self.grid = Puzzle.to_grid(file)
        self.nb_row = len(self.grid)
        self.nb_column = len(self.grid[0])

    def all_positions(self):
        for r in range(self.nb_row):
            for c in range(self.nb_column):
                yield r, c

    def is_inside_map(self, p):
        r, c = p
        return True if (0 <= r < self.nb_row) and (0 <= c < self.nb_column) else False

    def build_neighbours(self, p):
        (r0, c0) = p
        all_neighbours = [(r0 - 1, c0), (r0, c0 + 1), (r0 + 1, c0), (r0, c0 - 1)]
        inside_neighbours = filter(lambda point: self.is_inside_map(point), all_neighbours)
        neighbours = [(r, c) for r, c in inside_neighbours if self.grid[r][c] == (self.grid[r0][c0] + 1)]
        return neighbours

    def dfs(self, start):
        score = 0
        lifo = collections.deque([start])
        visited = set(start)
        while lifo:
            r, c = position = lifo.pop()
            if self.grid[r][c] == 9:
                score += 1
            for neighbour in self.build_neighbours(position):
                if neighbour not in visited:
                    lifo.append(neighbour)
                    visited.add(neighbour)
        return score

    def dfs_part2(self, start):
        score = 0
        lifo = collections.deque([start])
        # don't need visited set because we want all path
        while lifo:
            r, c = position = lifo.pop()
            if self.grid[r][c] == 9:
                score += 1
            for neighbour in self.build_neighbours(position):
                lifo.append(neighbour)
        return score

    def find_all_trailheads(self):
        score = sum([self.dfs((r, c)) for r, c in self.all_positions() if self.grid[r][c] == 0])
        return score

    def find_all_distinct_trailheads(self):
        rating = sum([self.dfs_part2((r, c)) for r, c in self.all_positions() if self.grid[r][c] == 0])
        return rating


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING)
    TEST_DATA_DIR = os.path.join(os.getcwd(), 'data')
    INPUT_FILE_EXAMPLE = os.path.join(TEST_DATA_DIR, 'day10', 'example.txt')
    INPUT_FILE = os.path.join(TEST_DATA_DIR, 'day10', 'input.txt')

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 1: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result_no_arg("part1", 36,
                                           puzzle.find_all_trailheads)
    print("part 1: execution time is ", time.time() - t0, " s")
    print("part 1: The sum of the score of all trailheads is", result)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 1: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result_no_arg("part1", 811,
                                           puzzle.find_all_trailheads)
    print("part 1: execution time is ", time.time() - t0, " s")
    print("part 1: The sum of the score of all trailheads is", result)

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 2: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result_no_arg("part1", 81,
                                           puzzle.find_all_distinct_trailheads)
    print("part 2: execution time is ", time.time() - t0, " s")
    print("part 2: The sum of the score of all trailheads is", result)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 2: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result_no_arg("part1", 1794,
                                           puzzle.find_all_distinct_trailheads)
    print("part 2: execution time is ", time.time() - t0, " s")
    print("part 2: The sum of the score of all trailheads is", result)
