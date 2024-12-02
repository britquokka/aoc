import logging
import os
import time
from TestUtils import TestUtils


logger = logging.getLogger(__name__)


class Puzzle:

    @staticmethod
    def to_reports(file):
        reports = []
        with open(file) as f:
            for line in f:
                row = [int(c) for c in line.strip().split()]
                reports.append(row)
        return reports

    def __init__(self, file):
        self.reports = Puzzle.to_reports(file)

    @staticmethod
    def is_safe_increase(report):
        return all([1 <= (level_b - level_a) <= 3 for level_a, level_b in zip(report, report[1::])])

    @staticmethod
    def is_safe_decrease(report):
        return all([1 <= level_a - level_b <= 3 for level_a, level_b in zip(report, report[1::])])

    @staticmethod
    def is_safe(report):
        return Puzzle.is_safe_decrease(report) or Puzzle.is_safe_increase(report)

    def find_safe_reports(self):
        safe_counter = sum([Puzzle.is_safe(report) for report in self.reports])
        return safe_counter

    def find_safe_reports_with_tolerance(self):
        safe_counter = sum([Puzzle.is_safe_with_tolerance(report) for report in self.reports])
        return safe_counter

    @staticmethod
    def is_safe_with_tolerance(report):
        is_safe = Puzzle.is_safe(report)

        # try to remove level one by one and check report is safe
        if not is_safe:
            is_safe = any(Puzzle.is_safe(report[:idx] + report[idx + 1:]) for idx in range(len(report)))

        return is_safe


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING)
    TEST_DATA_DIR = os.path.join(os.getcwd(), 'data')
    INPUT_FILE_EXAMPLE = os.path.join(TEST_DATA_DIR, 'day02', 'example.txt')
    INPUT_FILE = os.path.join(TEST_DATA_DIR, 'day02', 'input.txt')

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 1: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result_no_arg("part1", 2,
                                           puzzle.find_safe_reports)
    print("part 1: execution time is ", time.time() - t0, " s")
    print("part 1: The number of safe reports is", result)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 1: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result_no_arg("part1", 269,
                                           puzzle.find_safe_reports)
    print("part 1: execution time is ", time.time() - t0, " s")
    print("part 1: The number of safe reports is", result)

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 2: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result_no_arg("part2", 4,
                                           puzzle.find_safe_reports_with_tolerance)
    print("part 2: execution time is ", time.time() - t0, " s")
    print("part 2: The number of safe reports is", result)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 2: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result_no_arg("part2", 337,
                                           puzzle.find_safe_reports_with_tolerance)
    print("part 2: execution time is ", time.time() - t0, " s")
    print("part 2: The number of safe reports is", result)
