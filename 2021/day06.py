import logging
import os
import time
from collections import defaultdict

from TestUtils import TestUtils


logger = logging.getLogger(__name__)


class Puzzle:

    @staticmethod
    def to_puzzle_input(file):
        with open(file) as f:
            timers = list(map(lambda c: int(c), f.readline().strip().split(',')))
        return timers

    def __init__(self, file):
        self.timers = self.to_puzzle_input(file)
        logging.debug(self.timers)

    def compute_nb_fishes(self, nb_days):
        nb_fishes_by_timer = defaultdict(int)

        for t in self.timers:
            nb_fishes_by_timer[t] += 1

        while nb_days > 0:
            nb_days -= 1
            tmp_dict = defaultdict(int)
            for t in range(9):
                if t == 0:
                    tmp_dict[8] = nb_fishes_by_timer[0]
                    tmp_dict[6] = nb_fishes_by_timer[0]
                else:
                    tmp_dict[t-1] += nb_fishes_by_timer[t]
            nb_fishes_by_timer = tmp_dict
        return sum(nb_fishes_by_timer.values())


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    TEST_DATA_DIR = os.path.join(os.getcwd(), 'data')
    INPUT_FILE_EXAMPLE = os.path.join(TEST_DATA_DIR, 'day06', 'example.txt')
    INPUT_FILE = os.path.join(TEST_DATA_DIR, 'day06', 'input.txt')

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 1: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    nb = TestUtils.check_result("part1", 5934, puzzle.compute_nb_fishes, 80)
    print("part 1: execution time is ", time.time() - t0, " s")
    print("part 1: The number of lanternfishes after 80 days is ", nb)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 1: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    nb = TestUtils.check_result("part1", 373378, puzzle.compute_nb_fishes, 80)
    print("part 1: execution time is ", time.time() - t0, " s")
    print("part 1: The number of lanternfishes after 80 days is ", nb)

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 2: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    nb = TestUtils.check_result("part2", 26984457539, puzzle.compute_nb_fishes, 256)
    print("part 2: execution time is ", time.time() - t0, " s")
    print("part 2: The number of lanternfishes after 256 days is ", nb)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 2: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    nb = TestUtils.check_result("part2", 1682576647495, puzzle.compute_nb_fishes, 256)
    print("part 2: execution time is ", time.time() - t0, " s")
    print("part 2: The number of lanternfishes after 256 days is ", nb)
