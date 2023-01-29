import logging
import os
import time
from dataclasses import dataclass

TEST_DATA_DIR = os.path.join(os.getcwd(), 'data')

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Point:
    x: int
    y: int
    z: int

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        z = self.z + other.z
        return Point(x, y, z)


class Range3d:

    def __init__(self):
        self.min_x = self.min_y = self.min_z = float("inf")
        self.max_x = self.max_y = self.max_z = -float("inf")
        self.margin = 1

    def is_inside(self, p: Point):
        return True if (self.min_x <= p.x <= self.max_x
                        and self.min_y <= p.y <= self.max_y
                        and self.min_z <= p.z <= self.max_z) else False

    def update(self, p: Point):
        self.min_x = min(self.min_x, p.x-self.margin)
        self.min_y = min(self.min_y, p.y-self.margin)
        self.min_z = min(self.min_z, p.z-self.margin)

        self.max_x = max(self.max_x, p.x+self.margin)
        self.max_y = max(self.max_y, p.y+self.margin)
        self.max_z = max(self.max_z, p.z+self.margin)

    def get_min_point(self):
        return Point(int(self.min_x), int(self.min_y), int(self.min_y))

    def get_volume(self):
        return (self.max_x+1 - self.min_x) * (self.max_y+1 - self.min_y) * (self.max_z+1 - self.min_z)


class Volume:
    NEIGHBOUR_DELTAS = [Point(1, 0, 0), Point(0, 1, 0), Point(0, 0, 1),
                        Point(-1, 0, 0), Point(0, -1, 0), Point(0, 0, -1)]

    def __init__(self, range3d: Range3d, lava_cubes):
        self.range3d = range3d
        self.lava_cubes = lava_cubes
        self.nb_lava_cubes = len(self.lava_cubes)

    def bfs_find_ext_air_cube(self, start_node):
        nb_total_sides_in_lava_contact = 0
        visited = set()
        fifo = []
        visited.add(start_node)
        fifo.append(start_node)
        while fifo:
            current = fifo.pop(0)
            neighbours, nb_sides_in_lava_contact = self.build_air_cube_neighbours(current)
            nb_total_sides_in_lava_contact = nb_total_sides_in_lava_contact + nb_sides_in_lava_contact
            for neighbour in neighbours:
                if neighbour not in visited:
                    visited.add(neighbour)
                    fifo.append(neighbour)
        return visited, nb_total_sides_in_lava_contact

    @staticmethod
    def build_all_neighbours(p: Point):
        neighbours = []
        for delta in Volume.NEIGHBOUR_DELTAS:
            neighbour = p + delta
            neighbours.append(neighbour)

        return neighbours

    def build_air_cube_neighbours(self, point: Point):
        neighbours = self.build_all_neighbours(point)
        inside_cubes = list(filter(lambda p: self.range3d.is_inside(p), neighbours))
        air_cubes = list(filter(lambda p:  p not in self.lava_cubes, inside_cubes))
        nb_sides_in_lava_contact = len(inside_cubes) - len(air_cubes)
        return air_cubes, nb_sides_in_lava_contact

    def get_nb_total_cubes(self):
        return self.range3d.get_volume()

    def get_nb_lava_cubes(self):
        return self.nb_lava_cubes

    def find_exterior_air_cubes(self):
        return self.bfs_find_ext_air_cube(self.range3d.get_min_point())


class Puzzle:

    @staticmethod
    def to_lava_cubes(file):
        lava_cubes = set()
        range3d = Range3d()
        with open(file) as f:
            for line in f:
                x, y, z = tuple(map(lambda a: int(a), line.strip().split(',')))
                point = Point(x, y, z)
                lava_cubes.add(point)
                range3d.update(point)

        return lava_cubes, range3d

    def __init__(self, file):
        self.lava_cubes, self.range3d = self.to_lava_cubes(file)

    def compute_total_surface_area(self):
        nb_connected = 0
        for point in self.lava_cubes:
            for delta in Volume.NEIGHBOUR_DELTAS:
                neighbour = point + delta
                if neighbour in self.lava_cubes:
                    nb_connected = nb_connected + 1

        nb_surface_area = len(self.lava_cubes) * 6 - nb_connected
        return nb_surface_area

    @staticmethod
    def log_info(volume, exterior_air_cubes):
        nb_total_cubes = volume.get_nb_total_cubes()
        nb_exterior_air_cubes = len(exterior_air_cubes)
        nb_lava_cubes = volume.get_nb_lava_cubes()
        nb_inside_air_cubes = nb_total_cubes - nb_exterior_air_cubes - nb_lava_cubes
        logger.info("nb total cubes         : %s", nb_total_cubes)
        logger.info("nb exterior air cubes  : %s", nb_exterior_air_cubes)
        logger.info("nb lava cubes          : %s", nb_lava_cubes)
        logger.info("nb inside air cubes    : %s", nb_inside_air_cubes)

    def compute_total_exterior_surface_area(self):
        volume = Volume(self.range3d, self.lava_cubes)
        exterior_air_cubes, nb_total_sides_in_lava_contact = volume.find_exterior_air_cubes()
        self.log_info(volume, exterior_air_cubes)
        return nb_total_sides_in_lava_contact


class TestUtils:

    @staticmethod
    def check_result(test_name: str, expected_result: int, method_to_check):
        current_result = method_to_check()
        assert current_result == expected_result, test_name + ': ' + '(current_result:' + str(
            current_result) + ') != (expected_result:' + str(expected_result) + ')'
        return current_result


if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING)

    INPUT_FILE_EXAMPLE = os.path.join(TEST_DATA_DIR, 'day18', 'example.txt')
    INPUT_FILE = os.path.join(TEST_DATA_DIR, 'day18', 'input.txt')

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 1: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    nb_total_surface_area = TestUtils.check_result("part1", 64, puzzle.compute_total_surface_area)
    print("part 1: execution time is ", time.time() - start, " s")
    print("part 1: the total surface area is ", nb_total_surface_area)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 1: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    nb_total_surface_area = TestUtils.check_result("part1", 3650, puzzle.compute_total_surface_area)
    print("part 1: execution time is ", time.time() - start, " s")
    print("part 1: the total surface area is ", nb_total_surface_area)

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 2: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    nb_total_surface_area = TestUtils.check_result("part2", 58, puzzle.compute_total_exterior_surface_area)
    print("part 2: execution time is ", time.time() - start, " s")
    print("part 2: the total exterior surface area is ", nb_total_surface_area)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 2: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    nb_total_surface_area = TestUtils.check_result("part2", 2118, puzzle.compute_total_exterior_surface_area)
    print("part 2: execution time is ", time.time() - start, " s")
    print("part 2: the total exterior surface area is ", nb_total_surface_area)
