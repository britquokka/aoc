import collections
import logging
import os
import time

TEST_DATA_DIR = os.path.join(os.getcwd(), 'data')

logger = logging.getLogger(__name__)


class Puzzle:
    @staticmethod
    def to_forest(file):
        forest = []

        with open(file) as f:
            for line in f:
                row = list(map(lambda x: int(x), list(line.strip())))
                forest.append(row)
        return forest

    def __init__(self, file):
        self.forest = self.to_forest(file)
        self.max_x = len(self.forest[0])
        self.max_y = len(self.forest)
        logger.debug(self.forest)

    def compute_scenic_score(self, x, y):
        scenic_score = 0
        tree_height = self.forest[y][x]
        up = down = left = right = 0

        # up
        if y != 0:
            for j in range(y-1, -1, -1):
                is_visible = True if self.forest[j][x] < tree_height else False
                up += 1
                if not is_visible:
                    break

        # down
        if y != (self.max_y - 1):
            for j in range(y+1, self.max_y, 1):
                is_visible = True if self.forest[j][x] < tree_height else False
                down += 1
                if not is_visible:
                    break

        # right
        if x != (self.max_x - 1):
            for i in range(x+1, self.max_x, 1):
                is_visible = True if self.forest[y][i] < tree_height else False
                right += 1
                if not is_visible:
                    break

        # left
        if x != 0:
            for i in range(x-1, -1, -1):
                is_visible = True if self.forest[y][i] < tree_height else False
                left += 1
                if not is_visible:
                    break

        return up * down * right * left

    def find_visible_trees_from_we(self, range_y, range_x):
        visible_trees = set()
        for y in range_y:
            max_height = -1
            for x in range_x:
                height = self.forest[y][x]
                if height > max_height:
                    visible_trees.add((x, y))
                    max_height = height
        return visible_trees

    def find_visible_trees_from_ns(self, range_y, range_x):
        visible_trees = set()
        for x in range_x:
            max_height = -1
            for y in range_y:
                height = self.forest[y][x]
                if height > max_height:
                    visible_trees.add((x, y))
                    max_height = height
        return visible_trees

    def count_nb_visible_trees(self):
        visible_trees_from_west = self.find_visible_trees_from_we(range(0, self.max_y), range(0, self.max_x))
        visible_trees_from_east = self.find_visible_trees_from_we(range(0, self.max_y), range(self.max_x-1, -1, -1))
        visible_trees_from_north = self.find_visible_trees_from_ns(range(0, self.max_y), range(0, self.max_x))
        visible_trees_from_south = self.find_visible_trees_from_ns(range(self.max_y-1, -1, -1), range(0, self.max_x))

        trees = visible_trees_from_west.union(visible_trees_from_east,
                                              visible_trees_from_north,
                                              visible_trees_from_south)
        return len(trees)

    def compute_highest_scenic_score(self):
        high_scenic_score = 0
        for y in range(0, self.max_y):
            for x in range(0, self.max_x):
                scenic_score = self.compute_scenic_score(x, y)
                high_scenic_score = max(scenic_score, high_scenic_score)
        return high_scenic_score


class TestUtils:

    @staticmethod
    def check_result(test_name: str, expected_result: str, method_to_check, argv):
        current_result = method_to_check(argv)
        assert current_result == expected_result, test_name + ': ' + '(current_result:' + str(
            current_result) + ') != (expected_result:' + str(expected_result) + ')'
        return current_result

    @staticmethod
    def check_result_no_arg(test_name: str, expected_result: str, method_to_check):
        current_result = method_to_check()
        assert current_result == expected_result, test_name + ': ' + '(current_result:' + str(
            current_result) + ') != (expected_result:' + str(expected_result) + ')'
        return current_result


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING)

    INPUT_FILE_EXAMPLE = os.path.join(TEST_DATA_DIR, 'day8', 'example.txt')
    INPUT_FILE = os.path.join(TEST_DATA_DIR, 'day8', 'input.txt')

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 1: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    nb_visible_trees = TestUtils.check_result_no_arg("part1", 21, puzzle.count_nb_visible_trees)
    print("part 1: execution time is ", time.time() - start, " s")
    print("part 1: The number of trees visible from outside the grid is", nb_visible_trees)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 1: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    nb_visible_trees = TestUtils.check_result_no_arg("part1", 1690, puzzle.count_nb_visible_trees)
    print("part 1: execution time is ", time.time() - start, " s")
    print("part 1: The number of trees visible from outside the grid is", nb_visible_trees)

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 2: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    highest_scenic_score = TestUtils.check_result_no_arg("part2", 8, puzzle.compute_highest_scenic_score)
    print("part 2: execution time is ", time.time() - start, " s")
    print("part 2: The highest scenic score possible for any tree is", highest_scenic_score)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 2: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    highest_scenic_score = TestUtils.check_result_no_arg("part2", 535680, puzzle.compute_highest_scenic_score)
    print("part 2: execution time is ", time.time() - start, " s")
    print("part 2: The highest scenic score possible for any tree is", highest_scenic_score)