import logging
import os
import time
from TestUtils import TestUtils
from collections import namedtuple

logger = logging.getLogger(__name__)

Position = namedtuple('Position', ['h', 'd'])
Movement = namedtuple('Movement', ['direction', 'range'])


class Submarine:
    delta_by_dir = {
        "forward": (1, 0),
        "up": (0, -1),
        "down": (0, 1)
    }

    def __init__(self):
        self.position = Position(0, 0)

    def move(self, course: list) -> Position:
        for movement in course:
            self.position = self.move_one(movement)
        return self.position

    def move_one(self, movement: Movement):
        delta_h, delta_d = Submarine.delta_by_dir[movement.direction]
        return Position(h=self.position.h + delta_h * movement.range,
                        d=self.position.d + delta_d * movement.range)


class SubmarineWithAim(Submarine):

    def __init__(self):
        super().__init__()
        self.aim = 0

    def move_one(self, movement: Movement):
        delta_f, delta_v = Submarine.delta_by_dir[movement.direction]
        if delta_v != 0:
            # compute aim on up/down order
            self.aim = delta_v * movement.range + self.aim
        else:
            delta_h = delta_f * movement.range
            delta_d = delta_h * self.aim
            self.position = Position(h=self.position.h + delta_h,
                                     d=self.position.d + delta_d)
        return self.position


class Puzzle:

    @staticmethod
    def to_planned_course(file):
        course = []
        with open(file) as f:
            for line in f:
                raw = line.strip().split()
                course.append(Movement(direction=raw[0], range=int(raw[1])))
        return course

    def __init__(self, file):
        self.planned_course = self.to_planned_course(file)
        logger.debug(self.planned_course)

    def get_move_results(self):
        submarine = Submarine()
        final_position = submarine.move(self.planned_course)
        return final_position.h * final_position.d

    def get_move_with_aim_results(self):
        submarine = SubmarineWithAim()
        final_position = submarine.move(self.planned_course)
        return final_position.h * final_position.d


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    TEST_DATA_DIR = os.path.join(os.getcwd(), 'data')
    INPUT_FILE_EXAMPLE = os.path.join(TEST_DATA_DIR, 'day02', 'example.txt')
    INPUT_FILE = os.path.join(TEST_DATA_DIR, 'day02', 'input.txt')

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 1: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result_no_arg("part1", 150, puzzle.get_move_results)
    print("part 1: execution time is ", time.time() - t0, " s")
    print("part 1: The result if you multiply final h position by final depth  is ", result)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 1: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result_no_arg("part1", 1815044, puzzle.get_move_results)
    print("part 1: execution time is ", time.time() - t0, " s")
    print("part 1: The result if you multiply final h position by final depth  is ", result)

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 2: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result_no_arg("part2", 900, puzzle.get_move_with_aim_results)
    print("part 2: execution time is ", time.time() - t0, " s")
    print("part 2: The result if you multiply final h position by final depth  is ", result)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 2: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result_no_arg("part2", 1739283308, puzzle.get_move_with_aim_results)
    print("part 2: execution time is ", time.time() - t0, " s")
    print("part 2: The result if you multiply final h position by final depth  is ", result)
