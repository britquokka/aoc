import logging
import os
import time

from TestUtils import TestUtils


logger = logging.getLogger(__name__)


class Puzzle:

    @staticmethod
    def to_puzzle_input(file):
        with open(file) as f:
            h_positions = list(map(lambda c: int(c), f.readline().strip().split(',')))
        return h_positions

    def __init__(self, file):
        self.h_positions = self.to_puzzle_input(file)
        logging.debug(self.h_positions)

    def compute_cheapest_outcome(self):
        # take the crabs in the middle as best position
        # The crab in the middle should not move else the cost will increase at least +1
        median = self.h_positions[len(self.h_positions) // 2]
        min_cost = sum([abs(h-median) for h in self.h_positions])
        logger.info("The crabs must spend %d fuel to align to horizontal position %d", min_cost, median)
        return min_cost

    @staticmethod
    def first_integer_sum(n):
        return n * (n + 1) // 2

    def compute_cheapest_outcome_part2(self):
        min_p, max_p = min(self.h_positions), max(self.h_positions)
        min_cost, best_p = float('inf'), 0
        for p in range(min_p, max_p + 1):
            cost = sum([Puzzle.first_integer_sum(abs(h-p)) for h in self.h_positions])
            if min_cost > cost:
                min_cost = cost
                best_p = p

        logger.info("The crabs must spend %d fuel to align to horizontal position %d", min_cost, best_p)
        return min_cost


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    TEST_DATA_DIR = os.path.join(os.getcwd(), 'data')
    INPUT_FILE_EXAMPLE = os.path.join(TEST_DATA_DIR, 'day07', 'example.txt')
    INPUT_FILE = os.path.join(TEST_DATA_DIR, 'day07', 'input.txt')

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 1: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    fuel_cost = TestUtils.check_result_no_arg("part1", 37, puzzle.compute_cheapest_outcome)
    print("part 1: execution time is ", time.time() - t0, " s")
    print("part 1: The cheapest outcome is  ", fuel_cost, " fuel to align the crabs")

    print("-----------------")
    input_file = INPUT_FILE
    print("part 1: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    fuel_cost = TestUtils.check_result_no_arg("part1", 347011, puzzle.compute_cheapest_outcome)
    print("part 1: execution time is ", time.time() - t0, " s")
    print("part 1: The cheapest outcome is  ", fuel_cost, " fuel to align the crabs")

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 2: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    fuel_cost = TestUtils.check_result_no_arg("part1", 168, puzzle.compute_cheapest_outcome_part2)
    print("part 2: execution time is ", time.time() - t0, " s")
    print("part 2: The cheapest outcome is  ", fuel_cost, " fuel to align the crabs")

    print("-----------------")
    input_file = INPUT_FILE
    print("part 2: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    fuel_cost = TestUtils.check_result_no_arg("part1", 98363777, puzzle.compute_cheapest_outcome_part2)
    print("part 2: execution time is ", time.time() - t0, " s")
    print("part 2: The cheapest outcome is  ", fuel_cost, " fuel to align the crabs")