import logging
import os
import time
from TestUtils import TestUtils
import math


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
        step, _ = self.find_targets('AAA', ['ZZZ'])
        return step

    def find_targets(self, start, targets):
        flag_exit_loop = False
        step = 0
        nb = len(self.instructions)
        current_node = start
        while not flag_exit_loop:
            instruction = self.instructions[step % nb]
            idx_dst = 0 if instruction == 'L' else 1
            next_node = self.network[current_node][idx_dst]
            if next_node in targets:
                flag_exit_loop = True
            step += 1
            current_node = next_node

        return step, current_node

    def find_num_steps_part2(self):
        start_nodes = set(filter(lambda n: 'A' in n, self.network.keys()))
        target_nodes = set(filter(lambda n: 'Z' in n, self.network.keys()))
        found_nodes = []
        for start in start_nodes:
            step, found_node = self.find_targets(start, target_nodes)
            found_nodes.append((step, found_node))
        logger.debug(start_nodes)
        logger.debug(target_nodes)
        logger.debug(found_nodes)
        steps = [step for step, _ in found_nodes]

        return math.lcm(*steps)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)
    TEST_DATA_DIR = os.path.join(os.getcwd(), 'data')
    INPUT_FILE_EXAMPLE = os.path.join(TEST_DATA_DIR, 'day08', 'example.txt')
    INPUT_FILE = os.path.join(TEST_DATA_DIR, 'day08', 'input.txt')
    INPUT_FILE_EXAMPLE_PART2 = os.path.join(TEST_DATA_DIR, 'day08', 'example_part2.txt')

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

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE_PART2
    print("part 2: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    num_steps = TestUtils.check_result_no_arg("part2", 6, puzzle.find_num_steps_part2)
    print("part 2: execution time is ", time.time() - t0, " s")
    print("part 2: The number of steps to reach 'Z' nodes is ", num_steps)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 2: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    num_steps = TestUtils.check_result_no_arg("part2", 17972669116327, puzzle.find_num_steps_part2)
    print("part 2: execution time is ", time.time() - t0, " s")
    print("part 2: The number of steps to reach 'Z' nodes is ", num_steps)
