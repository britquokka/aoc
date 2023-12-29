import logging
import os
import time
from enum import IntEnum

from TestUtils import TestUtils


logger = logging.getLogger(__name__)


class Direction(IntEnum):
    NORTH = 0
    WEST = 1
    SOUTH = 2
    EAST = 3


class Puzzle:
    delta_by_dir = {Direction.NORTH: (-1, 0), Direction.WEST: (0, -1),
                    Direction.SOUTH: (1, 0), Direction.EAST: (0, 1)}

    @staticmethod
    def move(coord: tuple, delta: tuple):
        y, x, = coord
        delta_y, delta_x = delta
        return y + delta_y, x + delta_x

    def get_destination(self, coord: tuple, delta: tuple, next_rounded_rocks: set):
        flag_exit_loop = False
        prev_dst = coord
        next_dst = None
        while not flag_exit_loop:
            next_dst = self.move(prev_dst, delta)
            if next_dst in self.cube_shaped_rocks:
                next_dst = prev_dst
                flag_exit_loop = True
            elif next_dst in next_rounded_rocks:
                next_dst = prev_dst
                flag_exit_loop = True
            else:
                prev_dst = next_dst
        return next_dst

    def move_all(self, rounded_rocks: set, direction: Direction):
        next_rounded_rocks = set()
        delta = Puzzle.delta_by_dir[direction]
        prev_rounded_rocks = list(rounded_rocks)
        need_reverse = True if direction == Direction.EAST or direction == Direction.SOUTH else False
        prev_rounded_rocks.sort(reverse=need_reverse)
        for rock_coord in prev_rounded_rocks:
            next_dst = self.get_destination(rock_coord, delta, next_rounded_rocks)
            next_rounded_rocks.add(next_dst)
        return next_rounded_rocks

    @staticmethod
    def to_platform(file):
        platform = []
        with open(file) as f:
            nb_column = len(f.readline().strip()) + 2
            initial_row = '#' * nb_column
            platform.append(initial_row)
        with open(file) as f:
            for line in f:
                row = '#' + str(line.strip()) + '#'
                platform.append(row)
        platform.append(initial_row)
        return platform

    @staticmethod
    def to_rock_coords(file):
        cube_shaped_rocks = set()
        rounded_rocks = set()
        platform = Puzzle.to_platform(file)
        for y, line in enumerate(platform):
            for x, c in enumerate(line):
                if c == '#':
                    cube_shaped_rocks.add((y, x))
                elif c == 'O':
                    rounded_rocks.add((y, x))

        return cube_shaped_rocks, rounded_rocks, len(platform[0]), len(platform)

    def __init__(self, file):
        self.cube_shaped_rocks, self.rounded_rocks, self.x_len, self.y_len = self.to_rock_coords(file)

    def compute_load_on_north(self, rounded_rocks):
        load = 0
        for y, x in rounded_rocks:
            load += self.y_len - 1 - y

        return load

    def compute_total_load(self):
        self.rounded_rocks = self.move_all(self.rounded_rocks, Direction.NORTH)
        return self.compute_load_on_north(self.rounded_rocks)

    def cycle_roll(self, rr):
        for direction in Direction:
            rr = self.move_all(rr, direction)
        return rr

    def compute_total_load_after_x_cycles(self):
        flag_exit_loop = False
        cycle_by_rr, rr_by_cycle = {}, {}
        initial_cycle, cycle, found_cycle = 1, 1, 1
        rr = self.rounded_rocks

        while not flag_exit_loop:
            rr = self.cycle_roll(rr)
            rr_frozen = frozenset(rr)
            if rr_frozen in cycle_by_rr:
                initial_cycle = cycle_by_rr[rr_frozen]
                found_cycle = cycle
                flag_exit_loop = True
            else:
                cycle_by_rr[rr_frozen] = cycle
                rr_by_cycle[cycle] = rr_frozen
            cycle += 1

        logger.warning("Result is the same for cycle %d and %d", found_cycle, initial_cycle)

        # forecast for 1000000000
        cycle_len = found_cycle - initial_cycle
        target_cycle = (1000000000 - initial_cycle) % cycle_len + initial_cycle

        rounded_rocks = rr_by_cycle[target_cycle]
        logger.debug("Target cycle is %d", target_cycle)
        for cycle, rr in rr_by_cycle.items():
            logger.debug("cycle %d, load %d", cycle, self.compute_load_on_north(rr))

        return self.compute_load_on_north(rounded_rocks)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING)
    TEST_DATA_DIR = os.path.join(os.getcwd(), 'data')
    INPUT_FILE_EXAMPLE = os.path.join(TEST_DATA_DIR, 'day14', 'example.txt')
    INPUT_FILE = os.path.join(TEST_DATA_DIR, 'day14', 'input.txt')

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 1: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    total_load = TestUtils.check_result_no_arg("part1", 136, puzzle.compute_total_load)
    print("part 1: execution time is ", time.time() - start, " s")
    print("part 1: The total load on the north support beams is  ", total_load)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 1: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    total_load = TestUtils.check_result_no_arg("part1", 109098, puzzle.compute_total_load)
    print("part 1: execution time is ", time.time() - start, " s")
    print("part 1: The total load on the north support beams is  ", total_load)

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 2: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    total_load = TestUtils.check_result_no_arg("part2", 64, puzzle.compute_total_load_after_x_cycles)
    print("part 2: execution time is ", time.time() - start, " s")
    print("part 2: The total load on the north support beams is  ", total_load)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 2: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    total_load = TestUtils.check_result_no_arg("part2", 100064, puzzle.compute_total_load_after_x_cycles)
    print("part 2: execution time is ", time.time() - start, " s")
    print("part 2: The total load on the north support beams is  ", total_load)
