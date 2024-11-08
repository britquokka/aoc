import logging
import os
import time
from TestUtils import TestUtils
from collections import namedtuple
import heapq
from collections import defaultdict


logger = logging.getLogger(__name__)

Point = namedtuple('Point', ['x', 'y'])


class Cave:

    def __init__(self, risk_level_map, len_x: int, len_y: int):
        self.risk_level_map = risk_level_map
        self.len_x = len_x
        self.len_y = len_y
        self.destination = Point(self.len_x - 1, self.len_y - 1)

    @classmethod
    def build_cave(cls, risk_level_map):
        len_x = len(risk_level_map)
        len_y = len(risk_level_map[0])
        return cls(risk_level_map, len_x, len_y)

    def is_inside_map(self, p: Point):
        return True if (0 <= p.x < self.len_x) and (0 <= p.y < self.len_y) else False

    def build_neighbours(self, p: Point):
        all_neighbours = [Point(p.x - 1, p.y), Point(p.x, p.y - 1), Point(p.x, p.y + 1), Point(p.x + 1, p.y)]
        inside_neighbours = filter(lambda point: self.is_inside_map(point), all_neighbours)
        return inside_neighbours

    def get_risk_level(self, p: Point):
        return self.risk_level_map[p.x][p.y]

    def dijkstra(self, start: Point):
        distances = defaultdict(lambda: float('inf'))
        parents = dict()
        visited = set()
        queue = []

        distances[start] = 0
        parents[start] = None
        queue.append((0, start))  # priority queue

        while queue:
            d, node = heapq.heappop(queue)
            visited.add(node)
            neighbours = self.build_neighbours(node)
            for neighbor in neighbours:
                if neighbor not in visited:
                    new_d = d + self.get_risk_level(neighbor)
                    if new_d < distances[neighbor]:
                        distances[neighbor] = new_d
                        parents[neighbor] = node
                        heapq.heappush(queue, (new_d, neighbor))
        return distances, parents


class BiggerCave(Cave):

    def __init__(self, risk_level_map, bigger_coefficient=5):
        self.orig_len_x = len(risk_level_map)
        self.orig_len_y = len(risk_level_map[0])
        Cave.__init__(self, risk_level_map,  self.orig_len_x*bigger_coefficient, self.orig_len_y * bigger_coefficient)

    def get_risk_level(self, p: Point):
        div_x, mod_x = divmod(p.x, self.orig_len_x)
        div_y, mod_y = divmod(p.y, self.orig_len_y)
        orig_risk = self.risk_level_map[mod_x][mod_y]
        # risk is between [1..9] and modulo 9 is between [0..8]
        new_risk = (orig_risk + div_x + div_y - 1) % 9 + 1
        return new_risk


class Puzzle:
    @staticmethod
    def to_integers(line: str):
        return list(map(lambda c: int(c), line.strip()))

    @staticmethod
    def to_risk_level_map(file):
        with open(file) as f:
            risk_level_map = [Puzzle.to_integers(line) for line in f]
        return risk_level_map

    def __init__(self, file):
        self.risk_level_map = Puzzle.to_risk_level_map(file)

    def find_path_with_lowest_risk(self):
        cave = Cave.build_cave(self.risk_level_map)
        distances, _ = cave.dijkstra(Point(0, 0))
        return distances[cave.destination]

    def find_path_with_lowest_risk_part2(self):
        cave = BiggerCave(self.risk_level_map)
        distances, _ = cave.dijkstra(Point(0, 0))
        return distances[cave.destination]


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    TEST_DATA_DIR = os.path.join(os.getcwd(), 'data')
    INPUT_FILE_EXAMPLE = os.path.join(TEST_DATA_DIR, 'day15', 'example.txt')
    INPUT_FILE = os.path.join(TEST_DATA_DIR, 'day15', 'input.txt')

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 1: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result_no_arg("part1", 40, puzzle.find_path_with_lowest_risk)
    print("part 1: execution time is ", time.time() - t0, " s")
    print("part 1: The lowest total risk for the best path is", result)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 1: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result_no_arg("part1", 619, puzzle.find_path_with_lowest_risk)
    print("part 1: execution time is ", time.time() - t0, " s")
    print("part 1: The lowest total risk for the best path is", result)

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 2: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result_no_arg("part2", 315, puzzle.find_path_with_lowest_risk_part2)
    print("part 2: execution time is ", time.time() - t0, " s")
    print("part 2: The lowest total risk for the best path is", result)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 2: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result_no_arg("part2", 2922, puzzle.find_path_with_lowest_risk_part2)
    print("part 2: execution time is ", time.time() - t0, " s")
    print("part 2: The lowest total risk for the best path is", result)
