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
    def is_safe(report):
        is_safe , _ = Puzzle.check_report(report)
        return is_safe

    def find_safe_reports(self):
        safe_counter = sum([Puzzle.is_safe(report) for report in self.reports])
        return safe_counter

    def find_safe_reports_with_tolerance(self):
        safe_counter = sum([Puzzle.is_safe_with_tolerance(report) for report in self.reports])
        return safe_counter

    @staticmethod
    def check_report(report):
        prev_level = None
        is_increase = is_decrease = None
        flag_error = None
        idx = 0
        flag_exit_loop = False
        while not flag_exit_loop:
            cur_level = report[idx]
            if prev_level:
                if 1 <= (cur_level - prev_level) <= 3:
                    is_increase = True
                    flag_error = is_decrease
                elif 1 <= (prev_level - cur_level) <= 3:
                    is_decrease = True
                    flag_error = is_increase
                else:
                    flag_error = True
            if flag_error or idx + 1 >= len(report):
                flag_exit_loop = True
            else:
                idx += 1
                prev_level = cur_level
        return not flag_error, idx

    @staticmethod
    def is_safe_with_tolerance(report):
        is_safe, idx_error = Puzzle.check_report(report)

        if not is_safe:
            # retry by removing current and prev level where error was detected
            is_safe = any(Puzzle.is_safe(report[:idx] + report[idx + 1:]) for idx in range(idx_error-1, idx_error+1, 1))

            # special case when first level is bad
            if not is_safe and idx_error == 2:
                candidate_report = report[1:]
                is_safe = Puzzle.is_safe(candidate_report)

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