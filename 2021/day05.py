import logging
import os
import time
from TestUtils import TestUtils
from collections import namedtuple
from collections import defaultdict


logger = logging.getLogger(__name__)

Line = namedtuple('Line', ['p1', 'p2'])
Point = namedtuple('Point', ['x', 'y'])


class Puzzle:

    @staticmethod
    def to_vents_lines(file):
        lines = []
        with open(file) as f:
            for line in f:
                numbers_str = line.strip().replace('->', ',').split(',')
                x1, y1, x2, y2 = [int(s) for s in numbers_str]
                lines.append(Line(Point(x1, y1), Point(x2, y2)))

        return lines

    def __init__(self, file):
        self.counter_by_point = defaultdict(lambda: defaultdict(int))
        self.vents_lines = self.to_vents_lines(file)
        logger.debug(self.vents_lines)

    def count_overlapped_points(self):
        # hv_lines = [line for line in self.vents_lines if (line.p1.x == line.p2.x) | (line.p1.y == line.p2.y)]
        hv_lines = filter(lambda line: (line.p1.x == line.p2.x) | (line.p1.y == line.p2.y), self.vents_lines)
        for li in hv_lines:
            self.draw_line(li)
        return self.count()

    def count(self):
        count = 0
        for row in self.counter_by_point.values():
            for counter in row.values():
                if counter > 1:
                    count += 1
        return count

    def draw_line(self, line):
        len_x = line.p2.x - line.p1.x
        len_y = line.p2.y - line.p1.y
        delta_x = 1 if len_x > 0 else -1 if len_x < 0 else 0
        delta_y = 1 if len_y > 0 else -1 if len_y < 0 else 0
        nb_vents = max(abs(len_x), abs(len_y))
        p = line.p1
        for i in range(nb_vents+1):
            self.counter_by_point[p.x][p.y] += 1
            p = Point(p.x + delta_x, p.y + delta_y)

    def count_overlapped_points_part2(self):
        for li in self.vents_lines:
            self.draw_line(li)
        return self.count()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    TEST_DATA_DIR = os.path.join(os.getcwd(), 'data')
    INPUT_FILE_EXAMPLE = os.path.join(TEST_DATA_DIR, 'day05', 'example.txt')
    INPUT_FILE = os.path.join(TEST_DATA_DIR, 'day05', 'input.txt')

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 1: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result_no_arg("part1", 5, puzzle.count_overlapped_points)
    print("part 1: execution time is ", time.time() - t0, " s")
    print("part 1: The number of overlapped points is ", result)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 1: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result_no_arg("part1", 4655, puzzle.count_overlapped_points)
    print("part 1: execution time is ", time.time() - t0, " s")
    print("part 1: The number of overlapped points is ", result)

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 2: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result_no_arg("part2", 12, puzzle.count_overlapped_points_part2)
    print("part 2: execution time is ", time.time() - t0, " s")
    print("part 2: The number of overlapped points is ", result)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 2: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result_no_arg("part2", 20500, puzzle.count_overlapped_points_part2)
    print("part 2: execution time is ", time.time() - t0, " s")
    print("part 2: The number of overlapped points is ", result)
