import logging
import os
import time
from collections import defaultdict

TEST_DATA_DIR = os.path.join(os.getcwd(), 'data')

logger = logging.getLogger(__name__)


class Cave:

    def __init__(self):
        self.occupied_map = defaultdict(lambda: defaultdict(int))
        self.highest_point = (0, 0)

    def set_rock_line(self, begin, end):
        x1, y1 = begin
        x2, y2 = end
        y1, y2 = sorted([y1, y2])
        x1, x2 = sorted([x1, x2])
        for j in range(y1, y2 + 1):
            for i in range(x1, x2 + 1):
                self.occupied_map[i][j] = 1

    def is_free_point(self, point):
        x2, y2 = self.highest_point
        x1, y1 = point
        # part 2 set an infinite floor at two plus the highest y coordinate of any point
        if y1 == y2 + 2:
            self.occupied_map[x1][y1] = 1
        return True if self.occupied_map[x1][y1] == 0 else False

    def set_point_occupied(self, point):
        x, y = point
        self.occupied_map[x][y] = 1

    def set_highest_point_if_needed(self, point):
        x1, y1 = self.highest_point
        x2, y2 = point
        self.highest_point = point if y1 < y2 else self.highest_point

    def is_falling_in_abyss(self, point):
        x1, y1 = self.highest_point
        x2, y2 = point
        return True if y1 < y2 else False


class Puzzle:

    @staticmethod
    def to_2d_cave(file):
        cave = Cave()
        with open(file) as f:
            for line in f:
                rock_nodes = list(line.strip().split(' -> '))
                logger.info(rock_nodes)
                prev_point = None
                for rock_node in rock_nodes:
                    cur_point = tuple(map(lambda a: int(a), rock_node.split(',')))
                    cave.set_highest_point_if_needed(cur_point)
                    if prev_point is not None:
                        cave.set_rock_line(prev_point, cur_point)
                    prev_point = cur_point
        return cave

    def __init__(self, file):
        self.cave = self.to_2d_cave(file)
        logger.info("cave: %s", self.cave)
        logger.info("highest point:%s", self.cave.highest_point)

    def get_next_destination(self, point):
        result = None
        x, y = point
        down = x, y+1
        left = x-1, y+1
        right = x+1, y+1
        destinations = [down, left, right]
        for destination in destinations:
            if self.cave.is_free_point(destination):
                result = destination
                break
        return result

    def compute_nb_units_of_sand(self, with_floor=False):
        entry_point = (500, 0)
        flag_exit_loop = False
        sand_counter = 0
        path = [entry_point]
        while not flag_exit_loop:
            cur_point = path.pop()
            logger.debug("move:%s", cur_point)
            destination = self.get_next_destination(cur_point)
            if not destination:
                self.cave.set_point_occupied(cur_point)
                sand_counter = sand_counter + 1
                if cur_point == entry_point:
                    flag_exit_loop = True
            elif self.cave.is_falling_in_abyss(destination) and not with_floor:
                flag_exit_loop = True
            else:
                path.append(cur_point)
                path.append(destination)
        return sand_counter


class TestUtils:

    @staticmethod
    def check_result(test_name: str, expected_result: int, method_to_check, with_floor=False):
        current_result = method_to_check(with_floor)
        assert current_result == expected_result, test_name + ': ' + '(current_result:' + str(
            current_result) + ') != (expected_result:' + str(expected_result) + ')'
        return current_result


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING)

    INPUT_FILE_EXAMPLE = os.path.join(TEST_DATA_DIR, 'day14', 'example.txt')
    INPUT_FILE = os.path.join(TEST_DATA_DIR, 'day14', 'input.txt')

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 1: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    nb_unit_of_sands = TestUtils.check_result("part1", 24, puzzle.compute_nb_units_of_sand)
    print("part 1: execution time is ", time.time() - start, " s")
    print("part 1: the nb units of sand come to rest before abyss is ", nb_unit_of_sands)

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 2: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    nb_unit_of_sands = TestUtils.check_result("part1", 93, puzzle.compute_nb_units_of_sand, True)
    print("part 2: execution time is ", time.time() - start, " s")
    print("part 2: the nb units of sand come to rest is ", nb_unit_of_sands)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 1: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    nb_unit_of_sands = TestUtils.check_result("part1", 873, puzzle.compute_nb_units_of_sand)
    print("part 1: execution time is ", time.time() - start, " s")
    print("part 1: the nb units of sand come to rest before abyss is ", nb_unit_of_sands)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 2: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    nb_unit_of_sands = TestUtils.check_result("part1", 24813, puzzle.compute_nb_units_of_sand, True)
    print("part 2: execution time is ", time.time() - start, " s")
    print("part 2: the nb units of sand come to rest is", nb_unit_of_sands)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
