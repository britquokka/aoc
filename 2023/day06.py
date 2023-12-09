import logging
import os
import time
from TestUtils import TestUtils
import math
from math import sqrt

logger = logging.getLogger(__name__)


class Puzzle:

    @staticmethod
    def to_puzzle_input(file):
        with open(file) as f:
            _, raw_times = f.readline().strip().split(':')
            times = list(map(lambda x: int(x), raw_times.strip().split()))
            time_p2 = int(''.join(raw_times.strip().split()))
            _, raw_distances = f.readline().strip().split(':')
            distances = list(map(lambda x: int(x), raw_distances.strip().split()))
            distance_p2 = int(''.join(raw_distances.strip().split()))

        return times, distances, time_p2, distance_p2

    def __init__(self, file):
        (self.times, self.distances,
         self.time_p2, self.distance_p2) = self.to_puzzle_input(file)

    @staticmethod
    def compute_quadratic_equation_roots(a: int, b: int, c: float):
        delta = b*b - 4*a*c
        x1 = (-b + sqrt(delta)) / 2*a
        x2 = (-b - sqrt(delta)) / 2*a
        return x1, x2

    def multiply_number_of_win_ways(self):
        result = 1

        # f(t) = a*t +b
        # if wait_time = w = 2 then f(2) = 0 and f(3) = 2
        # or f(w) = 0 and f(w+1) = w
        # a*w +b = 0 ==> b = -a*w
        # a*(w+1) +b = w == > a = w
        # f(t) = w*t - w^2
        # now w is the variable and T and D fix
        # f(x) = T*x - x^2
        # It is a parable f(x) = a*x^2 + b*x +c
        # we want all value of x for who allow D < T*x - x^2
        # we have to solve a*x^2 + bx +c = 0 with a = -1 , b= T and c = -D
        # https://campussaintjean.be/IMG/pdf/chapitre_3_la_fonction_du_second_degre_1_.pdf
        # answers are range between the roots x1 and x2
        # with delta = b^2 - 4ac
        # x1 = (-b + sqrt(delta)) / 2a
        # x2 = (-b - sqrt(delta)) / 2a

        for T, D in zip(self.times, self.distances):
            c = -(D + float(0.000001))
            x1, x2 = Puzzle.compute_quadratic_equation_roots(-1, T, c)
            r = range(math.ceil(x1), int(x2))
            logger.debug("range=", r)
            result *= len(r) + 1

        return result

    def count_win_ways(self):
        a, b, c = -1, self.time_p2,  -(self.distance_p2 + float(0.000001))
        x1, x2 = Puzzle.compute_quadratic_equation_roots(a, b, c)
        r = range(math.ceil(x1), int(x2))
        return len(r) + 1


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    logging.basicConfig(level=logging.WARNING)
    TEST_DATA_DIR = os.path.join(os.getcwd(), 'data')
    INPUT_FILE_EXAMPLE = os.path.join(TEST_DATA_DIR, 'day06', 'example.txt')
    INPUT_FILE = os.path.join(TEST_DATA_DIR, 'day06', 'input.txt')

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 1: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    number_of_win_ways_mul = TestUtils.check_result_no_arg("part1", 288, puzzle.multiply_number_of_win_ways)
    print("part 1: execution time is ", time.time() - start, " s")
    print("part 1: if you multiply the number of ways you can beat the record, you get ", number_of_win_ways_mul)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 1: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    number_of_win_ways_mul = TestUtils.check_result_no_arg("part1", 5133600, puzzle.multiply_number_of_win_ways)
    print("part 1: execution time is ", time.time() - start, " s")
    print("part 1: if you multiply the number of ways you can beat the record, you get ", number_of_win_ways_mul)

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 2: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    number_of_win_ways = TestUtils.check_result_no_arg("part2", 71503, puzzle.count_win_ways)
    print("part 2: execution time is ", time.time() - start, " s")
    print("part 2: the number of ways is ", number_of_win_ways)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 2: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    number_of_win_ways = TestUtils.check_result_no_arg("part2", 40651271, puzzle.count_win_ways)
    print("part 2: execution time is ", time.time() - start, " s")
    print("part 2: the number of ways is ", number_of_win_ways)