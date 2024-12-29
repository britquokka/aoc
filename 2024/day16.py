import logging
import math
import os
import time
from enum import IntEnum
from TestUtils import TestUtils
import heapq
logger = logging.getLogger(__name__)


class Direction(IntEnum):
    NORTH = 0
    WEST = 1
    SOUTH = 2
    EAST = 3


class Maze:
    delta_by_dir = {Direction.NORTH: (-1, 0), Direction.WEST: (0, -1), Direction.SOUTH: (1, 0), Direction.EAST: (0, 1)}

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

    def is_inside_map(self, tile):
        y, x = tile
        return True if (0 <= y < self.nb_rows) and (0 <= x < self.nb_columns) else False

    def build_neighbours(self, node):
        neighbours = []
        (y0, x0), direction = node
        for next_dir in range(-1, 2):
            next_direction = Direction((direction + next_dir) % 4)
            dy, dx = Maze.delta_by_dir[next_direction]
            next_tile = (y, x) = (y0 + dy, x0 + dx)
            if self.is_inside_map(next_tile) and self.grid[y][x] != '#':
                neigh = (next_tile, next_direction)
                neighbours.append(neigh)
        return neighbours

    def dijkstra(self):
        best_score = math.inf
        best_seats = set()
        node = (self.start_tile, Direction.EAST)
        visited = set()
        queue = [(0, node, [])]
        while queue:
            score, node, seats = heapq.heappop(queue)
            tile, direction = node
            if tile == self.end_tile:
                best_score = min(best_score, score)
                if score == best_score:
                    best_seats.update(seats + [tile])
            else:
                neighbours = self.build_neighbours(node)
                for neighbor in neighbours:
                    next_tile, next_direction = neighbor
                    if neighbor not in visited:
                        visited.add(node)
                        path_score = score + 1 if next_direction == direction else score + 1001
                        heapq.heappush(queue, (path_score, neighbor, seats + [tile]))
        return best_score, len(best_seats)


class Puzzle:

    @staticmethod
    def to_maze(file):
        with open(file) as f:
            grid = [line.strip() for line in f]
        return grid

    def __init__(self, file):
        self.maze = Maze(Puzzle.to_maze(file))

    def find_best_path(self):
        best_score, _ = self.maze.dijkstra()
        return best_score

    def find_best_seats(self):
        _, nb_best_seats = self.maze.dijkstra()
        return nb_best_seats


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING)
    TEST_DATA_DIR = os.path.join(os.getcwd(), 'data')
    INPUT_FILE_EXAMPLE = os.path.join(TEST_DATA_DIR, 'day16', 'example.txt')
    INPUT_FILE = os.path.join(TEST_DATA_DIR, 'day16', 'input.txt')

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 1: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result_no_arg("part1", 11048,
                                           puzzle.find_best_path)
    print("part 1: execution time is ", time.time() - t0, " s")
    print("part 1: The lowest score a Reindeer could possibly get is", result)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 1: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result_no_arg("part1", 143564,
                                           puzzle.find_best_path)
    print("part 1: execution time is ", time.time() - t0, " s")
    print("part 1: The lowest score a Reindeer could possibly get is", result)

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 1: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result_no_arg("part2", 64,
                                           puzzle.find_best_seats)
    print("part 1: execution time is ", time.time() - t0, " s")
    print("part 1: The number of tile is", result)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 1: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result_no_arg("part2", 593,
                                           puzzle.find_best_seats)
    print("part 1: execution time is ", time.time() - t0, " s")
    print("part 1: The number of tile is", result)
