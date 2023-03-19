import logging
import os
import time
import math

TEST_DATA_DIR = os.path.join(os.getcwd(), 'data')

logger = logging.getLogger(__name__)


class Direction:
    move_by_dir = {'U': (0, 1), 'R': (1, 0), 'D': (0, -1), 'L': (-1, 0)}


class Puzzle:
    @staticmethod
    def to_movements(file):
        movements = []
        with open(file) as f:
            for line in f:
                direction, steps = line.strip().split()
                movements.append((direction, int(steps)))
        return movements

    def __init__(self, file):
        self.movements = self.to_movements(file)

    @staticmethod
    def move(point, delta):
        x, y = point
        delta_x, delta_y = delta
        return x+delta_x, y+delta_y

    @staticmethod
    def to_3_state(value):
        state = 0
        if value > 0:
            state = 1
        elif value < 0:
            state = -1
        return state

    @staticmethod
    def compute_knot_movement(knot, prev_knot):
        shall_move = False
        move_x = move_y = 0
        x2, y2 = knot
        x1, y1 = prev_knot
        delta_x = x1 - x2
        delta_y = y1 - y2
        if (math.fabs(delta_x) > 1) or (math.fabs(delta_y) > 1):
            shall_move = True
            move_x = Puzzle.to_3_state(delta_x)
            move_y = Puzzle.to_3_state(delta_y)
        knot_movement = (move_x, move_y)
        return knot_movement, shall_move

    def compute_nb_tail_positions(self, nb_knots):
        idx_tail = nb_knots-1
        tail_positions = set()
        knots = [(0, 0)] * nb_knots
        tail_positions.add(knots[idx_tail])

        for direction, steps in self.movements:
            for step in range(0, steps):
                knots[0] = self.move(knots[0], Direction.move_by_dir[direction])
                for idx in range(1, nb_knots):
                    movement, shall_move = self.compute_knot_movement(knots[idx], knots[idx-1])
                    if shall_move:
                        knots[idx] = self.move(knots[idx], movement)
                    else:
                        break
                tail_positions.add(knots[idx_tail])
        return len(tail_positions)


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

    INPUT_FILE_EXAMPLE = os.path.join(TEST_DATA_DIR, 'day9', 'example.txt')
    INPUT_FILE_EXAMPLE_PART2 = os.path.join(TEST_DATA_DIR, 'day9', 'example_part2.txt')
    INPUT_FILE = os.path.join(TEST_DATA_DIR, 'day9', 'input.txt')

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 1: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    nb_tail_positions = TestUtils.check_result("part1", 13, puzzle.compute_nb_tail_positions, 2)
    print("part 1: execution time is ", time.time() - start, " s")
    print("part 1: The number of positions does the tail of the rope visit at least once is", nb_tail_positions)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 1: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    nb_tail_positions = TestUtils.check_result("part1", 5874, puzzle.compute_nb_tail_positions, 2)
    print("part 1: execution time is ", time.time() - start, " s")
    print("part 1: The number of positions does the tail of the rope visit at least once is", nb_tail_positions)

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE_PART2
    print("part 2: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    nb_tail_positions = TestUtils.check_result("part2", 36, puzzle.compute_nb_tail_positions, 10)
    print("part 2: execution time is ", time.time() - start, " s")
    print("part 2: The number of positions does the tail of the rope visit at least once is", nb_tail_positions)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 2: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    nb_tail_positions = TestUtils.check_result("part2", 2467, puzzle.compute_nb_tail_positions, 10)
    print("part 2: execution time is ", time.time() - start, " s")
    print("part 2: The number of positions does the tail of the rope visit at least once is", nb_tail_positions)