import logging
import os
import time
from TestUtils import TestUtils

logger = logging.getLogger(__name__)


class Puzzle:
    @staticmethod
    def to_dig_plan(file):
        dig_plan = []
        with open(file) as f:
            for line in f:
                instruction = line.strip().split()
                dig_plan.append(instruction)
        return dig_plan

    def __init__(self, file):
        dig_plan = self.to_dig_plan(file)
        self.vertices = self.to_vertices(dig_plan)
        logging.warning(self.vertices)

    @staticmethod
    def to_vertices(dig_plan):
        y, x = 0, 0
        vertices = [(y, x)]
        for direction, distance, _ in dig_plan:
            d = int(distance)
            if direction == 'R':
                x += d
            elif direction == 'D':
                y += d
            elif direction == 'L':
                x -= d
            elif direction == 'U':
                y -= d
            vertices.append((y, x))
        return vertices

    def find_numbers_of_lava_cubic_meters(self):
        pass


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)
    TEST_DATA_DIR = os.path.join(os.getcwd(), 'data')
    INPUT_FILE_EXAMPLE = os.path.join(TEST_DATA_DIR, 'day18', 'example.txt')
    INPUT_FILE = os.path.join(TEST_DATA_DIR, 'day18', 'input.txt')

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 1: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    least_heat_loss = TestUtils.check_result_no_arg("part1", 102, puzzle.find_numbers_of_lava_cubic_meters)
    print("part 1: execution time is ", time.time() - t0, " s")
    print("part 1: The numbers of cubic meters of lava is ", least_heat_loss)

