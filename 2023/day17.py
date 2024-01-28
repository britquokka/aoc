import logging
import os
import time
from TestUtils import TestUtils
from enum import IntEnum
import collections

logger = logging.getLogger(__name__)


class Dir(IntEnum):
    N = 0
    E = 1
    S = 2
    W = 3


class Puzzle:
    @staticmethod
    def to_city_blocks(file):
        with open(file) as f:
            cities = f.read().splitlines()
        city_blocks = []
        for row in cities:
            city_blocks.append([int(c) for c in row])
        return city_blocks

    def __init__(self, file):
        self.city_blocks = self.to_city_blocks(file)
        self.cache_dfs_results = {}
        self.start = (0, 0)
        self.target = (len(self.city_blocks) - 1, len(self.city_blocks[0]) - 1)

    def dfs(self, start: tuple, target: tuple):
        min_heat_loss = float('inf')
        r, c = start
        heat_loss = self.city_blocks[r][c]
        lifo = collections.deque()
        lifo.append(((r+1, c), Dir.S, set(), 0))
        lifo.append(((r, c+1), Dir.E, set(), 0))
        while lifo:
            p, cur_dir, visited, curr_heat_loss = lifo.pop()
            visited.add((p, cur_dir))
            r, c = p
            curr_heat_loss += self.city_blocks[r][c]
            if p == target:
                min_heat_loss = min(min_heat_loss, curr_heat_loss)
            else:
                if curr_heat_loss < min_heat_loss:
                    neighbours = self.build_neighbours(p, cur_dir)
                    for neigh_p, neigh_dir in neighbours:
                        if (neigh_p, neigh_dir) not in visited:
                            lifo.append((neigh_p, neigh_dir, visited.copy(), curr_heat_loss))
        return min_heat_loss

    def find_least_heat_loss(self):
        min_heat_loss = self.dfs(self.start, self.target)
        return min_heat_loss

    def build_neighbours(self, p, direction: Dir):
        neighbours = []

        return neighbours


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)
    TEST_DATA_DIR = os.path.join(os.getcwd(), 'data')
    INPUT_FILE_EXAMPLE = os.path.join(TEST_DATA_DIR, 'day17', 'example.txt')
    INPUT_FILE = os.path.join(TEST_DATA_DIR, 'day17', 'input.txt')

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 1: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    least_heat_loss = TestUtils.check_result_no_arg("part1", 114, puzzle.find_least_heat_loss)
    print("part 1: execution time is ", time.time() - t0, " s")
    print("part 1: The least heat loss is ", least_heat_loss)


