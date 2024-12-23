import collections
import logging
import os
import time
from TestUtils import TestUtils


logger = logging.getLogger(__name__)


class MemorySpace:

    def __init__(self, grid_size):
        self.nb_rows = grid_size
        self.nb_columns = grid_size
        self.exit = (self.nb_columns - 1, self.nb_rows - 1)

    def is_inside_map(self, p):
        (x, y) = p
        return True if (0 <= y < self.nb_rows) and (0 <= x < self.nb_columns) else False

    def build_neighbours(self, c):
        (x0, y0) = c
        all_neighbours = [(x0 - 1, y0), (x0, y0 + 1), (x0 + 1, y0), (x0, y0 - 1)]
        inside_neighbours = filter(lambda point: self.is_inside_map(point), all_neighbours)
        return inside_neighbours

    def bfs(self, start, corrupted_coords):
        path = [start]
        has_exit = False
        nb_steps = -1
        fifo = collections.deque([(start, path)])
        seen = set(start).union(set(corrupted_coords))
        flag_exit_loop = False
        while not flag_exit_loop and fifo:
            coord, path = fifo.popleft()
            if coord == self.exit:
                has_exit = True
                flag_exit_loop = True
                nb_steps = len(path) - 1
            else:
                for neighbour in self.build_neighbours(coord):
                    if neighbour not in seen:
                        new_path = path.copy()
                        new_path.append(neighbour)
                        seen.add(neighbour)
                        fifo.append((neighbour, new_path))
        return has_exit, nb_steps


class Puzzle:

    @staticmethod
    def to_corrupted_memory_coords(file):
        coords = []
        with open(file) as f:
            for line in f:
                coord = [int(c) for c in line.strip().split(',')]
                coords.append(tuple(coord))
        return coords

    def __init__(self, file, grid_size, nb_falling_bytes=1024):
        self.corrupted_memory_coords = Puzzle.to_corrupted_memory_coords(file)
        self.memory_space = MemorySpace(grid_size)
        self.nb_falling_bytes = nb_falling_bytes
        self.start = (0, 0)

    def find_nb_steps_to_exit(self):
        _, nb_steps = self.memory_space.bfs(self.start, self.corrupted_memory_coords[0:self.nb_falling_bytes])
        return nb_steps

    def find_blocking_memory_coord(self):
        cut_off_byte_coord = None
        has_exit = True
        nb_bytes = self.nb_falling_bytes
        while has_exit:
            # find first corrupted byte which cut off the path to the exit.
            has_exit, nb_steps = self.memory_space.bfs(self.start, self.corrupted_memory_coords[0:nb_bytes])
            if not has_exit:
                cut_off_byte_coord = self.corrupted_memory_coords[nb_bytes - 1]
            nb_bytes += 1
        return cut_off_byte_coord


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING)
    TEST_DATA_DIR = os.path.join(os.getcwd(), 'data')
    INPUT_FILE_EXAMPLE = os.path.join(TEST_DATA_DIR, 'day18', 'example.txt')
    INPUT_FILE = os.path.join(TEST_DATA_DIR, 'day18', 'input.txt')

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 1: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file, grid_size=7, nb_falling_bytes=12)
    result = TestUtils.check_result_no_arg("part1", 22,
                                           puzzle.find_nb_steps_to_exit)
    print("part 1: execution time is ", time.time() - t0, " s")
    print("part 1: The minimum number of steps needed to reach the exit is", result)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 1: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file, grid_size=71, nb_falling_bytes=1024)
    result = TestUtils.check_result_no_arg("part1", 226,
                                           puzzle.find_nb_steps_to_exit)
    print("part 1: execution time is ", time.time() - t0, " s")
    print("part 1: The minimum number of steps needed to reach the exit is", result)

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 2: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file, grid_size=7, nb_falling_bytes=12)
    result = TestUtils.check_result_no_arg("part2", (6, 1),
                                           puzzle.find_blocking_memory_coord)
    print("part 2: execution time is ", time.time() - t0, " s")
    print("part 2: The coordinates of the first byte that will prevent the exit from being reachable is", result)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 2: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file, grid_size=71, nb_falling_bytes=1024)
    result = TestUtils.check_result_no_arg("part2", (60, 46),
                                           puzzle.find_blocking_memory_coord)
    print("part 2: execution time is ", time.time() - t0, " s")
    print("part 2: The coordinates of the first byte that will prevent the exit from being reachable is", result)
