import logging
import os
import time
from TestUtils import TestUtils
from collections import deque

logger = logging.getLogger(__name__)


class Puzzle:
    move_by_dir = {'N': (-1, 0), 'S': (1, 0), 'W': (0, -1), 'E': (0, 1)}
    pipe_by_code = {'|': 'NS', '-': 'WE', 'L': 'NE', 'J': 'NW', '7': 'SW', 'F': 'SE'}
    from_by_dir = {'N': 'S', 'E': 'W', 'W': 'E', 'S': 'N'}

    @staticmethod
    def to_sketch(file):
        sketch = []
        start_pos = (0, 0)
        with open(file) as f:
            y = 0
            for line in f:
                raw_line = list(line.strip())
                sketch.append(raw_line)
                x = line.strip().find('S')
                if x >= 0:
                    start_pos = (y, x)
                y += 1
        return start_pos, sketch

    def __init__(self, file):
        self.start_pos, self.sketch = self.to_sketch(file)

    @staticmethod
    def get_next_dir(pipe_code, prev_dir):
        pipe = Puzzle.pipe_by_code[pipe_code]
        from_dir = Puzzle.from_by_dir[prev_dir]
        # ex pipe = 'NS' if we come from 'S' then we go to  ('NS' - 'S' = 'N')
        next_dir_set = set(pipe) - set(from_dir)
        next_dir = next_dir_set.pop() if len(next_dir_set) == 1 else None
        return next_dir

    @staticmethod
    def move(pos, next_dir):
        (y0, x0) = pos
        (delta_y, delta_x) = Puzzle.move_by_dir[next_dir]
        (y, x) = (y0 + delta_y, x0 + delta_x)
        return y, x

    def find_first_direction(self, initial_pos):
        flag_exit_loop = False
        dirs = list(Puzzle.move_by_dir.keys())
        (y, x) = initial_pos
        next_dir = str()
        i = 0
        while not flag_exit_loop:
            next_dir = dirs[i]
            i += 1
            (y, x) = Puzzle.move(initial_pos, next_dir)
            pipe_code = self.sketch[y][x]
            if pipe_code != '.':
                next_dir = Puzzle.get_next_dir(pipe_code, next_dir)
                if next_dir:
                    flag_exit_loop = True

        return (y, x), next_dir

    def find_loop_path(self):
        path = deque([self.start_pos])

        # search first direction
        (y, x), next_dir = self.find_first_direction(self.start_pos)
        path.appendleft((y, x))

        # go into the loop
        flag_exit_loop = False
        while not flag_exit_loop:
            (y, x) = Puzzle.move((y, x), next_dir)
            pipe_code = self.sketch[y][x]
            path.appendleft((y, x))
            if pipe_code != 'S':
                next_dir = Puzzle.get_next_dir(pipe_code, next_dir)
            else:
                flag_exit_loop = True
        logger.info(path)
        return path

    def find_num_steps(self):
        path = self.find_loop_path()
        return (len(path) - 1) / 2


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    logging.basicConfig(level=logging.WARNING)
    TEST_DATA_DIR = os.path.join(os.getcwd(), 'data')
    INPUT_FILE_EXAMPLE = os.path.join(TEST_DATA_DIR, 'day10', 'example.txt')
    INPUT_FILE = os.path.join(TEST_DATA_DIR, 'day10', 'input.txt')

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 1: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    num_steps = TestUtils.check_result_no_arg("part1", 8, puzzle.find_num_steps)
    print("part 1: execution time is ", time.time() - start, " s")
    print("part 1: The number of steps from S points to the farthest point is ", num_steps)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 1: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    num_steps = TestUtils.check_result_no_arg("part1", 6846, puzzle.find_num_steps)
    print("part 1: execution time is ", time.time() - start, " s")
    print("part 1: The number of steps from S points to the farthest point is ", num_steps)
