import logging
import os
import time

TEST_DATA_DIR = os.path.join(os.getcwd(), 'data')

logger = logging.getLogger(__name__)


class Puzzle:
    @staticmethod
    def to_rucksacks(file):
        rucksacks = []
        with open(file) as f:
            for line in f:
                rucksacks.append(line.strip())
        return rucksacks

    def __init__(self, file):
        self.rucksacks = self.to_rucksacks(file)
        logger.debug(self.rucksacks)

    @staticmethod
    def item_to_prio(item):
        prio_offset = (27 - ord('A')) if item.isupper() else (1 - ord('a'))
        return ord(item) + prio_offset

    @staticmethod
    def get_prio(rucksack):
        size = int(len(rucksack) / 2)
        intersect = set(rucksack[0:size]) & set(rucksack[size:])
        return Puzzle.item_to_prio(intersect.pop())

    def compute_priorities_sum(self):
        priorities = map(lambda r: self.get_prio(r), self.rucksacks)
        return sum(priorities)

    @staticmethod
    def get_prio_group(rucksacks):
        intersect = set(rucksacks[0])
        for rucksack in rucksacks[1:]:
            intersect &= set(rucksack)
        return Puzzle.item_to_prio(intersect.pop())

    def compute_priorities_sum_for_three_elf_group(self):
        prio_sum = 0
        for i in range(0, len(self.rucksacks), 3):
            prio_sum += self.get_prio_group(self.rucksacks[i:i+3])
        return prio_sum


class TestUtils:

    @staticmethod
    def check_result(test_name: str, expected_result: int, method_to_check, argv):
        current_result = method_to_check(argv)
        assert current_result == expected_result, test_name + ': ' + '(current_result:' + str(
            current_result) + ') != (expected_result:' + str(expected_result) + ')'
        return current_result

    @staticmethod
    def check_result_no_arg(test_name: str, expected_result: int, method_to_check):
        current_result = method_to_check()
        assert current_result == expected_result, test_name + ': ' + '(current_result:' + str(
            current_result) + ') != (expected_result:' + str(expected_result) + ')'
        return current_result


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING)

    INPUT_FILE_EXAMPLE = os.path.join(TEST_DATA_DIR, 'day3', 'example.txt')
    INPUT_FILE = os.path.join(TEST_DATA_DIR, 'day3', 'input.txt')

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 1: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    priorities_sum = TestUtils.check_result_no_arg("part1", 157, puzzle.compute_priorities_sum)
    print("part 1: execution time is ", time.time() - start, " s")
    print("part 1: the sum of the priorities of those item types is ", priorities_sum)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 1: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    priorities_sum = TestUtils.check_result_no_arg("part1", 7824, puzzle.compute_priorities_sum)
    print("part 1: execution time is ", time.time() - start, " s")
    print("part 1: the sum of the priorities of those item types is ", priorities_sum)

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 2: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    priorities_sum = TestUtils.check_result_no_arg("part2", 70, puzzle.compute_priorities_sum_for_three_elf_group)
    print("part 2: execution time is ", time.time() - start, " s")
    print("part 2: the sum of the priorities for three-Elf group is ", priorities_sum)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 2: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    priorities_sum = TestUtils.check_result_no_arg("part2", 2798, puzzle.compute_priorities_sum_for_three_elf_group)
    print("part 2: execution time is ", time.time() - start, " s")
    print("part 2: the sum of the priorities for three-Elf group is ", priorities_sum)
