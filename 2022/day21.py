import logging
import os
import time
from dataclasses import dataclass

TEST_DATA_DIR = os.path.join(os.getcwd(), 'data')
logger = logging.getLogger(__name__)


@dataclass
class Job:
    name: str

    def compute(self):
        pass


@dataclass
class YellJob(Job):
    yelled_number: int

    def compute(self):
        return self.yelled_number


@dataclass
class OperationJob(Job):
    names: []
    operation: str
    needed_jobs: []

    def compute(self):
        res_job1 = self.needed_jobs[0].compute()
        res_job2 = self.needed_jobs[1].compute()
        if self.operation == '+':
            result = res_job1 + res_job2
        elif self.operation == '-':
            result = res_job1 - res_job2
        elif self.operation == '*':
            result = res_job1 * res_job2
        elif self.operation == '/':
            result = res_job1 / res_job2
        elif self.operation == '=':
            result = True if res_job1 == res_job2 else False

        return result


class Puzzle:

    @staticmethod
    def to_jobs(file):
        jobs = {}
        with open(file) as f:
            for line in f:
                inputs = line.strip().replace(':', '').split(' ')
                name = inputs[0]
                names = []
                if inputs[1].isdigit():
                    yelled_number = int(inputs[1])
                    jobs[name] = YellJob(name, yelled_number)
                else:
                    names.append(inputs[1])
                    operation = inputs[2]
                    names.append(inputs[3])
                    jobs[name] = OperationJob(name, names, operation, [])

        # second pass
        for job in jobs.values():
            if isinstance(job, OperationJob):
                for name in job.names:
                    job.needed_jobs.append(jobs[name])
        return jobs

    def __init__(self, file):
        self.jobs = self.to_jobs(file)

    def compute(self):
        root_job = self.jobs['root']
        return root_job.compute()

    @staticmethod
    def dichotomy(f, a, b, e):
        delta = 1
        while delta > e:
            m = int((a + b) / 2)
            delta = abs(b - a)
            if f(m) == 0:
                return m
            elif f(a) * f(m) > 0:
                a = m
            else:
                b = m
        return a, b

    def do_root_job(self, value_to_test):
        root_job = self.jobs['root']
        my_job = self.jobs['humn']
        my_job.yelled_number = value_to_test
        return root_job.compute()

    def find_number_to_yell(self):
        root_job = self.jobs['root']
        root_job.operation = '-'

        # find range for dichotomy
        flag_exit_loop = False
        below = 0
        above = 2**10
        while not flag_exit_loop:
            if self.do_root_job(below) * self.do_root_job(above) < 0:
                flag_exit_loop = True
            else:
                below = below
                above = above * 2

        # dichotomy
        my_number_to_yell = self.dichotomy(self.do_root_job, below, above, 0)
        return my_number_to_yell


class TestUtils:

    @staticmethod
    def check_result(test_name: str, expected_result: int, method_to_check):
        current_result = method_to_check()
        assert current_result == expected_result, test_name + ': ' + '(current_result:' + str(
            current_result) + ') != (expected_result:' + str(expected_result) + ')'
        return current_result


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING)

    INPUT_FILE_EXAMPLE = os.path.join(TEST_DATA_DIR, 'day21', 'example.txt')
    INPUT_FILE = os.path.join(TEST_DATA_DIR, 'day21', 'input.txt')

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 1: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    number = TestUtils.check_result("part1", 152, puzzle.compute)
    print("part 1: execution time is ", time.time() - start, " s")
    print("part 1: the monkey named root will yell the number ", number)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 1: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    number = TestUtils.check_result("part1", 276156919469632, puzzle.compute)
    print("part 1: execution time is ", time.time() - start, " s")
    print("part 1: the monkey named root will yell the number ", number)

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 2: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    number = TestUtils.check_result("part2", 301, puzzle.find_number_to_yell)
    print("part 2: execution time is ", time.time() - start, " s")
    print("part 2: the number to yell, to pass root's equality test, is ", number)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 2: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    number = TestUtils.check_result("part2", 3441198826073, puzzle.find_number_to_yell)
    print("part 2: execution time is ", time.time() - start, " s")
    print("part 2: the number to yell, to pass root's equality test, is ", number)



