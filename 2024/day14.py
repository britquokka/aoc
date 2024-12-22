import logging
import os
import time
from TestUtils import TestUtils
import re
from collections import namedtuple


logger = logging.getLogger(__name__)
Robot = namedtuple('Robot', ['x', 'y', 'vx', 'vy'])


class Puzzle:

    @staticmethod
    def to_robots(file):
        robots = []
        with open(file) as f:
            for line in f:
                numbers_str = re.findall(r'-?\d+', line.strip())
                numbers = [int(s) for s in numbers_str]
                robots.append(Robot(*numbers))
        return robots

    def __init__(self, file, nb_tiles_wide, nb_tiles_tall):
        self.robots = Puzzle.to_robots(file)
        # logger.warning(self.robots)
        self.nb_rows = nb_tiles_tall
        self.nb_columns = nb_tiles_wide

    def get_dest(self, robot: Robot, t: int):
        dst_x = (robot.x + robot.vx * t) % self.nb_columns
        dst_y = (robot.y + robot.vy * t) % self.nb_rows
        return dst_x, dst_y

    def find_safety_factor(self):
        dsts = [self.get_dest(r, 100) for r in self.robots]
        my = self.nb_rows // 2
        mx = self.nb_columns // 2
        q1 = sum([True for x, y in dsts if y < my and x < mx])
        q2 = sum([True for x, y in dsts if y < my and x > mx])
        q3 = sum([True for x, y in dsts if y > my and x < mx])
        q4 = sum([True for x, y in dsts if y > my and x > mx])
        return q1 * q2 * q3 * q4


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING)
    TEST_DATA_DIR = os.path.join(os.getcwd(), 'data')
    INPUT_FILE_EXAMPLE = os.path.join(TEST_DATA_DIR, 'day14', 'example.txt')
    INPUT_FILE = os.path.join(TEST_DATA_DIR, 'day14', 'input.txt')

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 1: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file, nb_tiles_wide=11, nb_tiles_tall=7)
    result = TestUtils.check_result_no_arg("part1", 12,
                                           puzzle.find_safety_factor)
    print("part 1: execution time is ", time.time() - t0, " s")
    print("part 1: The safety factor after 100 seconds is", result)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 1: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file, nb_tiles_wide=101, nb_tiles_tall=103)
    result = TestUtils.check_result_no_arg("part1", 228457125,
                                           puzzle.find_safety_factor)
    print("part 1: execution time is ", time.time() - t0, " s")
    print("part 1: The safety factor after 100 seconds is", result)
