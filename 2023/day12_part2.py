import collections
import logging
import os
import time
from TestUtils import TestUtils
from collections import Counter

logger = logging.getLogger(__name__)


class Puzzle:

    @staticmethod
    def to_rows(file):
        rows, groups_list = [], []
        with open(file) as f:
            for line in f:
                raw_springs, raw_criterias = list(line.strip().split())
                rows.append(raw_springs)
                groups = tuple(map(lambda x: int(x), raw_criterias.split(',')))
                groups_list.append(groups)
        return rows, groups_list

    def __init__(self, file):
        self.cache_dfs_results = {}
        self.rows, self.groups_list = self.to_rows(file)

    @staticmethod
    def debug(candidate: list, spring, groups):
        new = candidate.copy()
        new.append('#')
        logger.debug("criteria %s , #  candidate %s ", groups, new)
        return new

    def dfs_recursive(self, row: str, groups, count_in_group, candidate) -> int:
        nb = 0

        key = (row, groups, count_in_group)
        if key in self.cache_dfs_results:
            # search already done and result was cached
            return self.cache_dfs_results[key]

        if len(row) > 0:
            spring = row[0]
            nb = 0

            if spring == '#' or spring == '?':
                new = puzzle.debug(candidate, '#', groups)
                count = count_in_group + 1
                is_group_valid = True if len(groups) and count <= groups[0] else False
                if is_group_valid:
                    nb += self.dfs_recursive(row[1:], groups, count, new)

            if spring == '.' or spring == '?':
                new = puzzle.debug(candidate, '.', groups)
                count = count_in_group
                new_groups = groups
                is_group_valid = True
                if count != 0:
                    is_group_valid = True if len(groups) and count == groups[0] else False
                    new_groups = groups[1:]
                    count = 0
                if is_group_valid:
                    nb += self.dfs_recursive(row[1:], new_groups, count, new)
        else:
            # en with '#"
            if len(groups) == 1 and count_in_group == groups[0]:
                nb = 1
            # end with '.'
            if len(groups) == 0 and count_in_group == 0:
                nb = 1
            if nb == 1:
                logger.debug("criteria %s , WIN candidate %s ", groups, candidate)

        # put result in cache. key are input parameters of the recursive DFS
        self.cache_dfs_results[key] = nb

        return nb

    def depth_first_search(self, row, groups):
        # reset cache
        self.cache_dfs_results = {}
        return self.dfs_recursive(row, groups, 0, [])

    def sum_arrangement_counts(self):
        sum_arrangements, nb_row = 0, 0
        t0 = time.time()
        for row, groups in zip(self.rows, self.groups_list):
            nb_row += 1
            nb_ar = self.depth_first_search(row, groups)
            logger.debug("nb row: %s, nb_ar: %s, date: %s s", nb_row, nb_ar, time.time() - t0)
            sum_arrangements += nb_ar
        return sum_arrangements

    def unfold_and_sum_arrangement_counts(self):
        sum_arrangements, nb_row = 0, 0
        t0 = time.time()
        for row, groups in zip(self.rows, self.groups_list):
            unfolded_row = '?'.join([row] * 5)
            unfolded_groups = groups * 5
            nb_row += 1
            nb_ar = self.depth_first_search(unfolded_row, unfolded_groups)
            if nb_row % 1 == 0:
                logger.debug("nb row: %s, nb_ar: %s, date: %s s", nb_row, nb_ar, time.time() - t0 )
            sum_arrangements += nb_ar
        return sum_arrangements


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    logging.basicConfig(level=logging.WARNING)
    TEST_DATA_DIR = os.path.join(os.getcwd(), 'data')
    INPUT_FILE_EXAMPLE = os.path.join(TEST_DATA_DIR, 'day12', 'example.txt')
    INPUT_FILE = os.path.join(TEST_DATA_DIR, 'day12', 'input.txt')

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 1: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    sum_arrangement_counts = TestUtils.check_result_no_arg("part1", 21, puzzle.sum_arrangement_counts)
    print("part 1: execution time is ", time.time() - start, " s")
    print("part 1: The sum of the count of the different arrangements of springs is  ", sum_arrangement_counts)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 1: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    sum_arrangement_counts = TestUtils.check_result_no_arg("part1", 7407, puzzle.sum_arrangement_counts)
    print("part 1: execution time is ", time.time() - start, " s")
    print("part 1: The sum of the count of the different arrangements of springs is  ", sum_arrangement_counts)

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 2: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    sum_arrangement_counts = TestUtils.check_result_no_arg("part2", 525152, puzzle.unfold_and_sum_arrangement_counts)
    print("part 2: execution time is ", time.time() - start, " s")
    print("part 2: The sum of the count of the different arrangements of springs is  ", sum_arrangement_counts)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 2: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    sum_arrangement_counts = TestUtils.check_result_no_arg("part2", 30568243604962, puzzle.unfold_and_sum_arrangement_counts)
    print("part 2: execution time is ", time.time() - start, " s")
    print("part 2: The sum of the count of the different arrangements of springs is  ", sum_arrangement_counts)
