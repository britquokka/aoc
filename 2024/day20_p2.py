import collections
import logging
import os
import time
from TestUtils import TestUtils

logger = logging.getLogger(__name__)

Cheats = collections.namedtuple('Cheats', ['start', 'end', 'time'])


class TrackMap:

    def __init__(self, grid):
        self.grid = grid
        for y, row in enumerate(self.grid):
            for x, tile_value in enumerate(row):
                if tile_value == 'S':
                    self.start_tile = (y, x)
                elif tile_value == 'E':
                    self.end_tile = (y, x)

    def build_neighbours(self, p, prev):
        (y0, x0) = p
        all_neighbours = [(y0 - 1, x0), (y0, x0 + 1), (y0 + 1, x0), (y0, x0 - 1)]
        neighbours = [(y, x) for y, x in all_neighbours if self.grid[y][x] != '#' and (y, x) != prev]
        return neighbours

    def dfs(self):
        prev_tile = None
        t = -1
        time_by_tile = {}
        lifo = collections.deque([self.start_tile])
        while lifo:
            tile = lifo.pop()
            t += 1
            time_by_tile[tile] = t
            neighbours = self.build_neighbours(tile, prev_tile)
            prev_tile = tile
            for neigh in neighbours:
                lifo.append(neigh)
        return time_by_tile

    @staticmethod
    def build_cheated_neighbours(tile, max_cheat_time):
        y0, x0 = tile
        max_ctime = max_cheat_time
        neighbours = []
        for dy in range(-max_ctime, max_ctime+1):
            for dx in range(-max_ctime, max_ctime+1):
                ctime = abs(dy)+abs(dx)
                if ctime <= max_ctime:
                    neighbours.append(((y0+dy, x0+dx), ctime))
        return neighbours

    def find_cheats(self, time_by_tile: dict, max_cheat_time):
        cheats = []
        visited = set()
        for start_tile in time_by_tile.keys():
            neighbours = self.build_cheated_neighbours(start_tile, max_cheat_time)
            visited.add(start_tile)
            for end_tile, ctime in neighbours:
                if end_tile in time_by_tile.keys() and end_tile not in visited:
                    cheats.append(Cheats(start_tile, end_tile, ctime))
        return cheats


class Puzzle:

    @staticmethod
    def to_track_map(file):
        with open(file) as f:
            grid = [line.strip() for line in f]
        return grid

    def __init__(self, file):
        self.trackMap = TrackMap(Puzzle.to_track_map(file))

    def find_nb_cheats(self, parameters):
        min_save_time, max_cheat_time = parameters
        time_by_tile = self.trackMap.dfs()
        cheats = self.trackMap.find_cheats(time_by_tile, max_cheat_time)
        save_times = [abs(time_by_tile[c.start] - time_by_tile[c.end]) - c.time for c in cheats]
        nb_cheats = sum([True for st in save_times if st >= min_save_time])
        return nb_cheats


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING)
    TEST_DATA_DIR = os.path.join(os.getcwd(), 'data')
    INPUT_FILE_EXAMPLE = os.path.join(TEST_DATA_DIR, 'day20', 'example.txt')
    INPUT_FILE = os.path.join(TEST_DATA_DIR, 'day20', 'input.txt')

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 1: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result(test_name="part1", expected_result=8,
                                    method_to_check=puzzle.find_nb_cheats, argv=(12, 2))
    print("part 1: execution time is ", time.time() - t0, " s")
    print("part 1: The number of cheats that would save you at least 12 picoseconds is", result)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 1: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result(test_name="part1", expected_result=1369,
                                    method_to_check=puzzle.find_nb_cheats, argv=(100, 2))
    print("part 1: execution time is ", time.time() - t0, " s")
    print("part 1: The number of cheats that would save you at least 100 picoseconds is", result)

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 2: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result(test_name="part1", expected_result=41,
                                    method_to_check=puzzle.find_nb_cheats, argv=(70, 20))
    print("part 2: execution time is ", time.time() - t0, " s")
    print("part 2: The number of cheats that would save you at least 70 picoseconds is", result)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 2: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result(test_name="part1", expected_result=979012,
                                    method_to_check=puzzle.find_nb_cheats, argv=(100, 20))
    print("part 2: execution time is ", time.time() - t0, " s")
    print("part 2: The number of cheats that would save you at least 100 picoseconds is", result)
