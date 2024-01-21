import collections
import logging
import os
import time
import re


from TestUtils import TestUtils

logger = logging.getLogger(__name__)


class Puzzle:
    @staticmethod
    def to_input(file):
        # instructions = str()
        network = {}
        with open(file) as f:
            instructions = f.readline().strip()
            f.readline()
            for line in f:
                node, destinations = line.strip().split(' = ')
                destinations = destinations.strip("() ").split(", ")
                network[node] = destinations
        return instructions, network

    def __init__(self, file):
        self.instructions, self.network = self.to_input(file)
        logger.debug(self.instructions)
        logger.debug(self.network)

    def find_num_steps(self):
        flag_exit_loop = False
        idx = 0
        nb = len(self.instructions)
        start = 'AAA'
        target = 'ZZZ'
        current_node = start
        while not flag_exit_loop:
            instruction = self.instructions[idx % nb]
            idx_dst = 0 if instruction == 'L' else 1
            next_node = self.network[current_node][idx_dst]
            if next_node == target:
                flag_exit_loop = True
            idx += 1
            current_node = next_node

        return idx


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)
    TEST_DATA_DIR = os.path.join(os.getcwd(), 'data')
    INPUT_FILE_EXAMPLE = os.path.join(TEST_DATA_DIR, 'day08', 'example.txt')
    INPUT_FILE = os.path.join(TEST_DATA_DIR, 'day08', 'input.txt')

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 1: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    num_steps = TestUtils.check_result_no_arg("part1", 6, puzzle.find_num_steps)
    print("part 1: execution time is ", time.time() - t0, " s")
    print("part 1: The number of steps to reach 'ZZZ' is ", num_steps)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 1: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    num_steps = TestUtils.check_result_no_arg("part1", 18673, puzzle.find_num_steps)
    print("part 1: execution time is ", time.time() - t0, " s")
    print("part 1: The number of steps to reach 'ZZZ' is ", num_steps)
