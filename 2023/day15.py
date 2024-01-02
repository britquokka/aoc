import logging
import os
import time
from collections import defaultdict
from TestUtils import TestUtils

logger = logging.getLogger(__name__)


class HashUtils:
    @staticmethod
    def hash(a_string: str):
        value = 0
        for c in a_string:
            value = ((value + ord(c)) * 17) % 256
        return value


class Boxes:

    def __init__(self):
        self.boxes = defaultdict(list)
        self.focal_by_label = {}

    def apply_steps(self, op_steps: list):
        for operation, (label, focal) in op_steps:
            box_number = HashUtils.hash(label)
            slots = self.boxes[box_number]
            if operation == '=':
                self.focal_by_label[label] = int(focal)
                if label not in slots:
                    slots.append(label)
            else:
                if label in slots:
                    slots.remove(label)

    def compute_focusing_power(self):
        power = 0
        for box_number, slots in self.boxes.items():
            for slot_idx, label in enumerate(slots):
                power += (box_number + 1) * (slot_idx + 1) * self.focal_by_label[label]
        return power


class Puzzle:
    @staticmethod
    def to_op_steps(steps: list):
        op_steps = []
        for step in steps:
            idx = step.find('=')
            if idx > 0:
                lens = (step[0:idx], step[idx + 1::])
                operation = '='
            else:
                lens = (step[0:len(step) - 1], '')
                operation = '-'
            op_steps.append((operation, lens))
        return op_steps

    @staticmethod
    def to_steps(file):
        steps = []
        with open(file) as f:
            for line in f:
                row = line.strip().split(',')
                steps.extend(row)
        op_steps = Puzzle.to_op_steps(steps)
        return steps, op_steps

    def __init__(self, file):
        self.steps, self.op_steps = self.to_steps(file)

    def sum_results(self):
        return sum([HashUtils.hash(step) for step in self.steps])

    def compute_focusing_power(self):
        boxes = Boxes()
        boxes.apply_steps(self.op_steps)
        return boxes.compute_focusing_power()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING)
    TEST_DATA_DIR = os.path.join(os.getcwd(), 'data')
    INPUT_FILE_EXAMPLE = os.path.join(TEST_DATA_DIR, 'day15', 'example.txt')
    INPUT_FILE = os.path.join(TEST_DATA_DIR, 'day15', 'input.txt')

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 1: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    results_sum = TestUtils.check_result_no_arg("part1", 1320, puzzle.sum_results)
    print("part 1: execution time is ", time.time() - start, " s")
    print("part 1: The sum of the results is  ", results_sum)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 1: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    results_sum = TestUtils.check_result_no_arg("part1", 504449, puzzle.sum_results)
    print("part 1: execution time is ", time.time() - start, " s")
    print("part 1: The sum of the results is  ", results_sum)

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 2: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    focusing_power = TestUtils.check_result_no_arg("part2", 145, puzzle.compute_focusing_power)
    print("part 2: execution time is ", time.time() - start, " s")
    print("part 2: The focusing power of the resulting lens configuration is  ",  focusing_power)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 2: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    focusing_power = TestUtils.check_result_no_arg("part2", 262044, puzzle.compute_focusing_power)
    print("part 2: execution time is ", time.time() - start, " s")
    print("part 2: The focusing power of the resulting lens configuration is  ",  focusing_power)
