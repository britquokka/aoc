
import logging
import os
import time

from TestUtils import TestUtils


logger = logging.getLogger(__name__)


class Dir:
    U: int = 0
    R: int = 1
    D: int = 2
    L: int = 3


class PathFinder:
    delta_by_dir = {Dir.U: (-1, 0), Dir.L: (0, -1), Dir.D: (1, 0), Dir.R: (0, 1)}

    def __init__(self, area):
        self.area = area

    @staticmethod
    def get_next_position(state):
        (y0, x0), direction = state
        (delta_y, delta_x) = PathFinder.delta_by_dir[direction]
        (y, x) = (y0 + delta_y, x0 + delta_x)
        return y, x

    def get_next_state(self, state):
        next_pos = self.get_next_position(state)
        prev_pos, direction = state

        if self.area.is_outside(next_pos):
            return None, True

        # turn right if obstacle
        if self.area.has_obstacle(next_pos):
            return (prev_pos, (direction + 1) % 4), False

        return (next_pos, direction), False

    def find_exit_path(self, initial_state):
        flag_exit_loop = False
        has_loop = False
        state = initial_state
        path = set()
        while not flag_exit_loop:
            path.add(state)
            next_state, has_exited = self.get_next_state(state)
            # already seen on path so it is a loop
            if not has_exited and next_state in path:
                has_loop = True
            flag_exit_loop = has_loop or has_exited
            state = next_state
        return path, has_loop


class Area:

    dir_by_symbol = {'>': Dir.R, '<': Dir.L,
                     'v': Dir.D, '^': Dir.U}
    dir_symbols = set(dir_by_symbol.keys())

    def __init__(self, grid):
        self.grid = grid
        self.nb_row = len(self.grid)
        self.nb_column = len(self.grid[0])

    def is_outside(self, p):
        (y, x) = p
        return False if (0 <= y < self.nb_row) and (0 <= x < self.nb_column) else True

    def has_obstacle(self, p):
        y, x = p
        return self.grid[y][x] == '#'

    def find_initial_guard_state(self):
        state = None
        for y in range(self.nb_row):
            for x in range(self.nb_column):
                v = self.grid[y][x]
                if v in Area.dir_symbols:
                    state = ((y, x), self.dir_by_symbol[v])
                    break
        return state


class Puzzle:

    @staticmethod
    def to_grid(file):
        with open(file) as f:
            grid = [list(line.strip()) for line in f]
        return grid

    def __init__(self, file):
        grid = Puzzle.to_grid(file)
        self.area = Area(grid)
        self.path_finder = PathFinder(self.area)

    def count_distinct_positions(self):
        initial_guard_state = self.area.find_initial_guard_state()
        path, _ = self.path_finder.find_exit_path(initial_guard_state)
        positions = [p for p, d in path]
        return len(set(positions))

    def count_obstruction_candidates(self):
        initial_guard_state = self.area.find_initial_guard_state()
        start, _ = initial_guard_state
        count = 0

        path, _ = self.path_finder.find_exit_path(initial_guard_state)
        positions = set([p for p, d in path])
        for (y, x) in positions:
            if (y, x) != start:
                prev = self.area.grid[y][x]
                self.area.grid[y][x] = '#'
                path, has_loop = self.path_finder.find_exit_path(initial_guard_state)
                if has_loop:
                    count += 1
                self.area.grid[y][x] = prev
        return count


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING)
    TEST_DATA_DIR = os.path.join(os.getcwd(), 'data')
    INPUT_FILE_EXAMPLE = os.path.join(TEST_DATA_DIR, 'day06', 'example.txt')
    INPUT_FILE = os.path.join(TEST_DATA_DIR, 'day06', 'input.txt')

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 1: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result_no_arg("part1", 41,
                                           puzzle.count_distinct_positions)
    print("part 1: execution time is ", time.time() - t0, " s")
    print("part 1: The number of distinct positions for the guard is", result)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 1: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result_no_arg("part1", 5177,
                                           puzzle.count_distinct_positions)
    print("part 1: execution time is ", time.time() - t0, " s")
    print("part 1: The number of distinct positions for the guard is", result)

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 2: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result_no_arg("part2", 6,
                                           puzzle.count_obstruction_candidates)
    print("part 2: execution time is ", time.time() - t0, " s")
    print("part 2: The number of different positions for the obstruction is", result)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 2: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result_no_arg("part2", 1686,
                                           puzzle.count_obstruction_candidates)
    print("part 2: execution time is ", time.time() - t0, " s")
    print("part 2: The number of different positions for the obstruction is", result)
