import collections
import logging
import os
import time
from TestUtils import TestUtils

logger = logging.getLogger(__name__)


class TrackMap:

    def __init__(self, grid):
        self.grid = grid
        self.nb_rows = len(self.grid)
        self.nb_columns = len(self.grid[0])
        for t in self.all_tiles():
            y, x = t
            if self.grid[y][x] == 'S':
                self.start_tile = t
            elif self.grid[y][x] == 'E':
                self.end_tile = t

    def all_tiles(self):
        for r in range(self.nb_rows):
            for c in range(self.nb_columns):
                yield r, c

    def is_border(self, p):
        (y, x) = p
        return y == 0 or y == self.nb_rows-1 or x == 0 or x == self.nb_columns-1

    def get_next_destination(self, p, prev):
        (y0, x0) = p
        all_neighbours = [(y0 - 1, x0), (y0, x0 + 1), (y0 + 1, x0), (y0, x0 - 1)]
        candidate_walls = [(y, x) for y, x in all_neighbours if self.grid[y][x] == '#' and not self.is_border((y, x))]
        neighbours = [(y, x) for y, x in all_neighbours if self.grid[y][x] != '#' and (y, x) != prev]
        return neighbours, candidate_walls

    def dfs(self):
        prev_tile = None
        t = -1
        time_by_tile = {}
        tiles_by_wall = collections.defaultdict(list)
        lifo = collections.deque([self.start_tile])
        while lifo:
            tile = lifo.pop()
            t += 1
            time_by_tile[tile] = t
            neighbours, walls = self.get_next_destination(tile, prev_tile)
            prev_tile = tile
            for neigh in neighbours:
                lifo.append(neigh)
            for w in walls:
                tiles_by_wall[w].append(tile)
        return time_by_tile, tiles_by_wall


class Puzzle:

    @staticmethod
    def to_track_map(file):
        with open(file) as f:
            grid = [line.strip() for line in f]
        return grid

    def __init__(self, file):
        self.trackMap = TrackMap(Puzzle.to_track_map(file))

    def find_nb_cheats(self, min_save_time):
        time_by_tile, tiles_by_wall = self.trackMap.dfs()
        cheat_tiles = [tiles for tiles in tiles_by_wall.values() if len(tiles) == 2]
        save_times = [abs(time_by_tile[tile1] - time_by_tile[tile2]) - 2 for tile1, tile2 in cheat_tiles]
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
                                    method_to_check=puzzle.find_nb_cheats, argv=12)
    print("part 1: execution time is ", time.time() - t0, " s")
    print("part 1: The number of cheats that would save you at least 100 picoseconds is", result)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 1: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result(test_name="part1", expected_result=1369,
                                    method_to_check=puzzle.find_nb_cheats, argv=100)
    print("part 1: execution time is ", time.time() - t0, " s")
    print("part 1: The number of cheats that would save you at least 100 picoseconds is", result)
