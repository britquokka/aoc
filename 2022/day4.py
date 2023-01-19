import re
import logging
import os


TEST_DATA_DIR = os.path.join(os.getcwd(), 'data')


logger = logging.getLogger(__name__)


class Puzzle:

    @staticmethod
    def tolist2d(file):
        result = []
        with open(file) as f:
            for line in f:
                row = re.split(r",|-", line.strip())
                row = list(map(lambda x: int(x), row))
                result.append(row)
        return result

    def __init__(self, file):
        self.sections = self.tolist2d(file)
        logger.debug(self.sections)

    def compute_nb_pairs(self):
        pair_counter = 0
        for pair in self.sections:
            s1, e1, s2, e2 = pair
            cond_inside = s2 >= s1 and e2 <= e1 or s1 >= s2 and e1 <= e2
            if cond_inside:
                pair_counter = pair_counter + 1
        return pair_counter

    def compute_nb_overlapping_pairs(self):
        pair_counter = 0
        for pair in self.sections:
            s1, e1, s2, e2 = pair
            cond_not_overlap = e1 < s2 or e2 < s1
            if not cond_not_overlap:
                pair_counter = pair_counter + 1
        return pair_counter


class TestUtils:

    @staticmethod
    def check_result(test_name: str, expected_result: int, method_to_check):
        current_result = method_to_check()
        assert current_result == expected_result, test_name + ': ' + '(current_result:' + str(
            current_result) + ') != (expected_result:' + str(expected_result) + ')'
        return current_result


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    INPUT_FILE_EXAMPLE = os.path.join(TEST_DATA_DIR, 'day4', 'example.txt')
    INPUT_FILE = os.path.join(TEST_DATA_DIR, 'day4', 'input.txt')

    # part 1
    puzzle_test = Puzzle(INPUT_FILE_EXAMPLE)
    TestUtils.check_result("part1", 2, puzzle_test.compute_nb_pairs)

    puzzle = Puzzle(INPUT_FILE)
    nb_pairs = puzzle.compute_nb_pairs()
    print("part 1: nb pairs does one range fully contain the other is ", nb_pairs)

    # part 2
    TestUtils.check_result("part2", 4, puzzle_test.compute_nb_overlapping_pairs)

    nb_overlapping_pairs = puzzle.compute_nb_overlapping_pairs()
    print("part 2: nb assignment pairs do the ranges overlap is ", nb_overlapping_pairs)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
