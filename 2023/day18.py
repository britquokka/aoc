import logging
import os
import time
from TestUtils import TestUtils
import itertools
from enum import IntEnum

logger = logging.getLogger(__name__)


class Dir(IntEnum):
    R = 0
    D = 1
    L = 2
    U = 3


class Puzzle:
    @staticmethod
    def to_dig_plan(file):
        dig_plan = []
        with open(file) as f:
            for line in f:
                instruction = line.strip().split()
                dig_plan.append(instruction)
        return dig_plan

    def __init__(self, file, part2=False):
        dig_plan = self.to_dig_plan(file)
        if not part2:
            self.vertices, self.perimeter = self.to_vertices(dig_plan)
        else:
            self.vertices, self.perimeter = self.to_vertices_part2(dig_plan)
        logging.debug(self.vertices)

    @staticmethod
    def to_vertices(dig_plan):
        y, x = 1, 1
        vertices = [(y, x)]
        p = 0
        for direction, distance, _ in dig_plan:
            d = int(distance)
            p += d
            if direction == 'R':
                x += d
            elif direction == 'D':
                y += d
            elif direction == 'L':
                x -= d
            elif direction == 'U':
                y -= d
            vertices.append((y, x))
        return vertices, p

    @staticmethod
    def to_vertices_part2(dig_plan):
        y, x = 1, 1
        vertices = [(y, x)]
        p = 0
        for _, _, hexa_code in dig_plan:
            d = int(hexa_code[2:7], 16)
            direction = int(hexa_code[7])
            p += d
            if direction == Dir.R:
                x += d
            elif direction == Dir.D:
                y += d
            elif direction == Dir.L:
                x -= d
            elif direction == Dir.U:
                y -= d
            vertices.append((y, x))
        return vertices, p

    @staticmethod
    def shoelace_formula(vertices: list):
        res = 0
        for vertex, next_vertex in itertools.pairwise(vertices):
            res += vertex[1] * next_vertex[0] - vertex[0] * next_vertex[1]
        return abs(res) / 2

    def compute_lagoon_volume(self):
        # take into account perimeter with 1 m width. 1/2 m inside computed area
        # and 1/2 m outside computed area
        # need to add 1 to have the good result say Pick's Theorem
        return Puzzle.shoelace_formula(self.vertices) + self.perimeter / 2 + 1


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
    area = TestUtils.check_result_no_arg("part1", 62,
                                         puzzle.compute_lagoon_volume)
    print("part 1: execution time is ", time.time() - t0, " s")
    print("part 1: The numbers of cubic meters of lava is ", area)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 1: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    volume = TestUtils.check_result_no_arg("part1", 45159,
                                           puzzle.compute_lagoon_volume)
    print("part 1: execution time is ", time.time() - t0, " s")
    print("part 1: The numbers of cubic meters of lava is ", volume)

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 2: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file, part2=True)
    area = TestUtils.check_result_no_arg("part2", 952408144115,
                                         puzzle.compute_lagoon_volume)
    print("part 2: execution time is ", time.time() - t0, " s")
    print("part 2: The numbers of cubic meters of lava is ", area)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 2: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file, part2=True)
    area = TestUtils.check_result_no_arg("part2", 134549294799713,
                                         puzzle.compute_lagoon_volume)
    print("part 2: execution time is ", time.time() - t0, " s")
    print("part 2: The numbers of cubic meters of lava is ", area)
