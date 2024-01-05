import collections
import logging
import os
import time
from TestUtils import TestUtils
from enum import IntEnum
from collections import defaultdict

logger = logging.getLogger(__name__)


class Dir(IntEnum):
    N = 0
    E = 1
    S = 2
    W = 3


class Route:
    delta_by_dir = {Dir.N: (-1, 0), Dir.W: (0, -1),
                    Dir.S: (1, 0), Dir.E: (0, 1)}
    pipe_by_dirs = {(Dir.N, Dir.S): '|',
                    (Dir.E, Dir.W): '-',
                    (Dir.N, Dir.E): 'L',
                    (Dir.N, Dir.W): 'J',
                    (Dir.S, Dir.W): '7',
                    (Dir.E, Dir.S): 'F'}

    def __init__(self):
        self.table = defaultdict(lambda: defaultdict(int))
        self.table[Dir.N]['|'] = Dir.N
        self.table[Dir.N]['F'] = Dir.E
        self.table[Dir.N]['7'] = Dir.W

        self.table[Dir.S]['|'] = Dir.S
        self.table[Dir.S]['L'] = Dir.E
        self.table[Dir.S]['J'] = Dir.W

        self.table[Dir.W]['-'] = Dir.W
        self.table[Dir.W]['F'] = Dir.S
        self.table[Dir.W]['L'] = Dir.N

        self.table[Dir.E]['-'] = Dir.E
        self.table[Dir.E]['J'] = Dir.N
        self.table[Dir.E]['7'] = Dir.S

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
            flag_exit_loop, y = False, 0
            while not flag_exit_loop:
                idx = grid[y].find('S')
                if idx >= 0:
                    start_pos = (y, idx)
                    flag_exit_loop = True
                y += 1
        return start_pos, grid

    def __init__(self, file):
        self.start_pos, self.grid = self.to_grid(file)
        self.route = Route()

    def find_initial_pipe_shape(self, initial_pos: tuple):
        dirs = []
        for d in Dir:
            (y, x) = Route.move(initial_pos, d)
            next_pipe = self.grid[y][x]
            if d == Dir.N and next_pipe in '|7F':
                dirs.append(d)
            elif d == Dir.S and next_pipe in '|LJ':
                dirs.append(d)
            elif d == Dir.W and next_pipe in 'FL-':
                dirs.append(d)
            elif d == Dir.E and next_pipe in '7J-':
                dirs.append(d)

        # N,E,S,W
        (dir1, dir2) = tuple(dirs)
        initial_pipe_shape = Route.pipe_by_dirs[(dir1, dir2)]

        return initial_pipe_shape, dirs

    def find_loop_path(self):
        loop = set()
        # find initial pipe shape
        initial_pipe_shape, dirs = self.find_initial_pipe_shape(self.start_pos)

        # go into the loop
        lifo = collections.deque()
        lifo.append((self.start_pos, dirs[0]))
        loop.add(self.start_pos)
        while lifo:
            (pos, direction) = lifo.pop()
            (y, x) = next_p = self.route.move(pos, direction)
            pipe = self.grid[y][x]
            if next_p not in loop:
                next_d = self.route.table[direction][pipe]
                lifo.append((next_p, next_d))
                loop.add(next_p)
        # logger.warning(loop)
        return loop, initial_pipe_shape

    def find_num_steps(self):
        loop, _ = self.find_loop_path()
        return (len(loop)) / 2

    def build_work_grid(self, loop, initial_pipe_shape):
        # replaces  all pipe not in the loop by '.'
        work_grid = []
        for y, row in enumerate(self.grid):
            work_row = []
            for x, c in enumerate(row):
                work_row.append(c if (y, x) in loop else '.')
            work_grid.append(work_row)

        # replace S by its real pipe shape
        (y, x) = self.start_pos
        work_grid[y][x] = initial_pipe_shape

        return work_grid

    def count_enclosed_tiles(self):
        loop, initial_pipe_shape = self.find_loop_path()

        # find enclosed tiles
        # work grid -> replace S by pipe and replace all pipes not in the loop by '.'
        work_grid = self.build_work_grid(loop, initial_pipe_shape)
        inside = False
        inside_tiles = []

        for y, row in enumerate(work_grid):
            store_c = None
            for x, c in enumerate(row):
                if c == '|':
                    inside = not inside
                elif store_c == 'F' and c == 'J':
                    inside = not inside
                    store_c = None
                elif store_c == 'F' and c == '7':
                    inside = inside
                    store_c = None
                elif store_c == 'L' and c == 'J':
                    inside = inside
                    store_c = None
                elif store_c == 'L' and c == '7':
                    inside = not inside
                    store_c = None
                elif c == 'F':
                    store_c = c
                elif c == 'L':
                    store_c = c
                elif c == '.':
                    if inside:
                        inside_tiles.append((y, x))

        return len(inside_tiles)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    logging.basicConfig(level=logging.WARNING)
    TEST_DATA_DIR = os.path.join(os.getcwd(), 'data')
    INPUT_FILE_EXAMPLE = os.path.join(TEST_DATA_DIR, 'day10', 'example.txt')
    INPUT_FILE_EXAMPLE_PART2 = os.path.join(TEST_DATA_DIR, 'day10', 'example_part2.txt')
    INPUT_FILE = os.path.join(TEST_DATA_DIR, 'day10', 'input.txt')

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 1: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    num_steps = TestUtils.check_result_no_arg("part1", 8, puzzle.find_num_steps)
    print("part 1: execution time is ", time.time() - start, " s")
    print("part 1: The number of steps from S points to the farthest point is ", num_steps)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 1: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    num_steps = TestUtils.check_result_no_arg("part1", 6846, puzzle.find_num_steps)
    print("part 1: execution time is ", time.time() - start, " s")
    print("part 1: The number of steps from S points to the farthest point is ", num_steps)

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE_PART2
    print("part 2: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    num_enclosed_tiles = TestUtils.check_result_no_arg("part2", 10, puzzle.count_enclosed_tiles)
    print("part 2: execution time is ", time.time() - start, " s")
    print("part 2: The number of tiles enclosed by the loop is ", num_enclosed_tiles)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 2: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    num_enclosed_tiles = TestUtils.check_result_no_arg("part2", 325, puzzle.count_enclosed_tiles)
    print("part 2: execution time is ", time.time() - start, " s")
    print("part 2: The number of tiles enclosed by the loop is ", num_enclosed_tiles)
