
import logging
import os
import time
from TestUtils import TestUtils
from enum import IntEnum
from collections import defaultdict
import collections


logger = logging.getLogger(__name__)


class Dir(IntEnum):
    N = 0
    W = 1
    S = 2
    E = 3


class Route:
    delta_by_dir = {Dir.N: (-1, 0), Dir.W: (0, -1),
                    Dir.S: (1, 0), Dir.E: (0, 1)}

    def __init__(self):
        self.table = defaultdict(lambda: defaultdict(list))
        self.table[Dir.N]['-'].extend([Dir.W, Dir.E])
        self.table[Dir.N]['/'].append(Dir.E)
        self.table[Dir.N]['\\'].append(Dir.W)
        self.table[Dir.N]['|'].append(Dir.N)
        self.table[Dir.N]['.'].append(Dir.N)

        self.table[Dir.S]['-'].extend([Dir.W, Dir.E])
        self.table[Dir.S]['/'].append(Dir.W)
        self.table[Dir.S]['\\'].append(Dir.E)
        self.table[Dir.S]['|'].append(Dir.S)
        self.table[Dir.S]['.'].append(Dir.S)

        self.table[Dir.E]['-'].append(Dir.E)
        self.table[Dir.E]['/'].append(Dir.N)
        self.table[Dir.E]['\\'].append(Dir.S)
        self.table[Dir.E]['|'].extend([Dir.N, Dir.S])
        self.table[Dir.E]['.'].append(Dir.E)

        self.table[Dir.W]['-'].append(Dir.W)
        self.table[Dir.W]['/'].append(Dir.S)
        self.table[Dir.W]['\\'].append(Dir.N)
        self.table[Dir.W]['|'].extend([Dir.N, Dir.S])
        self.table[Dir.W]['.'].append(Dir.W)

    @staticmethod
    def move(src: tuple, direction: Dir):
        y, x = src
        delta_y, delta_x = Route.delta_by_dir[direction]
        return y + delta_y, x + delta_x


class Puzzle:

    @staticmethod
    def to_grid(file):
        with open(file) as f:
            grid = f.read().splitlines()
        return grid

    def __init__(self, file):
        self.grid = self.to_grid(file)
        self.y_len = len(self.grid)
        self.x_len = len(self.grid[0])
        self.route = Route()

    def in_grid(self, point):
        y, x = point
        return (x >= 0) and (x < self.x_len) and (y >= 0) and (y < self.y_len)
    
    def call_dfs(self, entry_point, entry_dir):
        return self.dfs(entry_point, entry_dir)

    def dfs(self, entry_point: tuple, entry_dir: Dir):
        seen = set()
        tiles_seen = list()
        lifo = collections.deque()
        lifo.append((entry_point, entry_dir))
        while lifo:
            p, cur_dir = lifo.pop()
            py, px = p
            seen.add((p, cur_dir))
            tiles_seen.append(p)
            tile = self.grid[py][px]
            next_dirs = self.route.table[cur_dir][tile]
            for next_dir in next_dirs:
                next_p = self.route.move(p, next_dir)
                if self.in_grid(next_p):
                    if (next_p, next_dir) not in seen:
                        lifo.append((next_p, next_dir))
        return len(set(tiles_seen))

    def count_energized_tiles(self):
        count = self.call_dfs(entry_point=(0, 0), entry_dir=Dir.E)
        return count

    def find_best_configuration(self):
        max_count = 0
        for x in range(self.x_len):
            max_count = max(max_count, self.call_dfs((0, x), Dir.S))
            max_count = max(max_count, self.call_dfs((self.y_len-1, x), Dir.N))

        for y in range(self.y_len):
            max_count = max(max_count, self.call_dfs((y, 0), Dir.E))
            max_count = max(max_count, self.call_dfs((y, self.x_len-1), Dir.W))

        return max_count


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING)
    TEST_DATA_DIR = os.path.join(os.getcwd(), 'data')
    INPUT_FILE_EXAMPLE = os.path.join(TEST_DATA_DIR, 'day16', 'example.txt')
    INPUT_FILE = os.path.join(TEST_DATA_DIR, 'day16', 'input.txt')

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 1: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    energized_tiles = TestUtils.check_result_no_arg("part1", 46, puzzle.count_energized_tiles)
    print("part 1: execution time is ", time.time() - start, " s")
    print("part 1: The total of tiles energized is  ", energized_tiles)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 1: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    energized_tiles = TestUtils.check_result_no_arg("part1", 7307, puzzle.count_energized_tiles)
    print("part 1: execution time is ", time.time() - start, " s")
    print("part 1: The total of tiles energized is  ", energized_tiles)

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 2: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    energized_tiles = TestUtils.check_result_no_arg("part2", 51, puzzle.find_best_configuration)
    print("part 2: execution time is ", time.time() - start, " s")
    print("part 2: The total of tiles energized with best cfg is  ", energized_tiles)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 2: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    energized_tiles = TestUtils.check_result_no_arg("part2", 7635, puzzle.find_best_configuration)
    print("part 2: execution time is ", time.time() - start, " s")
    print("part 2: The total of tiles energized with best cfg is  ", energized_tiles)
