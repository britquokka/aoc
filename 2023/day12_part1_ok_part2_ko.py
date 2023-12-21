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
                rows.append(list(raw_springs))
                groups = list(map(lambda x: int(x), raw_criterias.split(',')))
                groups_list.append(groups)
        return rows, groups_list

    def __init__(self, file):
        self.rows, self.groups_list = self.to_rows(file)

    @staticmethod
    def depth_first_search(row, groups):
        nb_arrangements = 0
        counter = Counter(row)
        cq, cd = counter['?'], counter['#']
        sg = sum(groups)
        lr, lg = len(row), len(groups)
        idx_r, idx_g = 0, 0
        cg = 0
        spring = row[0]
        candidate = []
        lifo = collections.deque()
        lifo.append((spring, idx_r, lr, cq, cd, idx_g, sg, cg, candidate))

        while lifo:
            (spring, idx_r, lr, cq, cd, idx_g, sg, cg, candidate) = lifo.pop()
            # new = candidate.copy()
            new = None
            if spring == '?':
                lifo.append(('#', idx_r, lr, cq - 1,  cd + 1, idx_g, sg, cg, new))
                lifo.append(('.', idx_r, lr, cq - 1, cd, idx_g, sg, cg, new))
            elif spring == '#':
                # new.append(spring)
                # logger.debug("criteria %s , #  candidate %s ", groups, new)
                cd -= 1
                lr -= 1
                sg -= 1
                cg += 1
                idx_r += 1
                is_group_valid = True if idx_g < lg and cg <= groups[idx_g] else False
                if lr > 0 and is_group_valid and (cd + cq >= sg) and sg > 0:
                    lifo.append((row[idx_r], idx_r, lr, cq, cd, idx_g, sg, cg, new))
                elif cd == 0 and (idx_g == lg - 1) and cg == groups[idx_g]:
                    # logger.debug("criteria %s , WIN candidate %s ", groups, new)
                    nb_arrangements += 1
            elif spring == '.':
                # new.append(spring)
                # logger.debug("criteria %s , #  candidate %s ", groups, new)
                lr -= 1
                idx_r += 1
                is_group_valid = True
                if cg != 0:
                    is_group_valid = True if idx_g < lg and cg == groups[idx_g] else False
                    idx_g += 1
                    cg = 0
                if lr > 0 and is_group_valid and (cd + cq >= sg):
                    lifo.append((row[idx_r], idx_r, lr, cq, cd, idx_g, sg, cg, new))

        # logger.debug("AR %s", nb_arrangements)
        return nb_arrangements

    def sum_arrangement_counts(self):
        sum_arrangements = 0
        for row, groups in zip(self.rows, self.groups_list):
            sum_arrangements += self.depth_first_search(row, groups)
        return sum_arrangements

    def unfold_and_sum_arrangement_counts(self):
        sum_arrangements, nb_row = 0, 0
        t0 = time.time()
        for row, groups in zip(self.rows, self.groups_list):
            unfolded_row = row.copy()
            unfolded_groups = groups.copy()
            for i in range(4):
                unfolded_row.append('?')
                unfolded_row.extend(row)
                unfolded_groups.extend(groups)
            nb_row += 1
            sum_arrangements += self.depth_first_search(unfolded_row, unfolded_groups)
            if nb_row % 1 == 0:
                logger.warning("nb row: %s, time: %s s", nb_row, time.time() - t0 )
        return sum_arrangements


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG)
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
    sum_arrangement_counts = TestUtils.check_result_no_arg("part2", 525152, puzzle.unfold_and_sum_arrangement_counts)
    print("part 2: execution time is ", time.time() - start, " s")
    print("part 2: The sum of the count of the different arrangements of springs is  ", sum_arrangement_counts)
