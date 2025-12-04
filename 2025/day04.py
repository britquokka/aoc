import logging
import os
import time
from TestUtils import TestUtils

logger = logging.getLogger(__name__)


class HelpfulDiagram:

    def __init__(self, grid):
        self.grid = grid
        self.nb_rows = len(self.grid)
        self.nb_columns = len(self.grid[0])

    def all_tiles(self):
        for r in range(self.nb_rows):
            for c in range(self.nb_columns):
                yield r, c

    def is_inside_grid(self, p):
        x, y = p
        return True if (0 <= x < self.nb_columns) and (0 <= y < self.nb_rows) else False

    def get_adjacent_rolls(self, p):
        (y0, x0) = p
        all_neighbours = [(y0 - 1, x0), (y0, x0 + 1), (y0 + 1, x0), (y0, x0 - 1)]
        all_neighbours += [(y0 - 1, x0 - 1), (y0 + 1, x0 + 1), (y0 + 1, x0 - 1), (y0 - 1, x0 + 1)]
        adjacent_rolls_of_paper = [(y, x) for y, x in all_neighbours if self.is_inside_grid((y, x))
                                   and self.grid[y][x] == '@']

        return adjacent_rolls_of_paper

    def is_roll_accessible(self, p):
        # there are fewer than 4 rolls in the 8 adjacent positions
        adj_rolls = self.get_adjacent_rolls(p)
        return len(adj_rolls) < 4

    def get_accessible_rolls(self):
        rolls = [(y, x) for y, x in self.all_tiles() if self.grid[y][x] == '@' and self.is_roll_accessible((y, x))]
        return rolls

    def remove(self, rolls):
        for (y, x) in rolls:
            self.grid[y][x] = 'x'


class Puzzle:

    @staticmethod
    def to_grid(file):
        with open(file) as f:
            grid = [list(line.strip()) for line in f]
        return grid

    def __init__(self, file):
        self.helpfulDiagram = HelpfulDiagram(Puzzle.to_grid(file))

    def find_nb_of_accessible_rolls(self):
        return len(self.helpfulDiagram.get_accessible_rolls())

    def find_nb_of_removable_rolls(self):
        flag_exit_loop = False
        nb_removed = 0
        while not flag_exit_loop:
            rolls_to_remove = self.helpfulDiagram.get_accessible_rolls()
            if len(rolls_to_remove) > 0:
                self.helpfulDiagram.remove(rolls_to_remove)
                nb_removed += len(rolls_to_remove)
            else:
                flag_exit_loop = True

        return nb_removed


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING)
    TEST_DATA_DIR = os.path.join(os.getcwd(), 'data')
    INPUT_FILE_EXAMPLE = os.path.join(TEST_DATA_DIR, 'day04', 'example.txt')
    INPUT_FILE = os.path.join(TEST_DATA_DIR, 'day04', 'input.txt')

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 1: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result_no_arg(test_name="part1", expected_result=13,
                                           method_to_check=puzzle.find_nb_of_accessible_rolls)
    print("part 1: execution time is ", time.time() - t0, " s")
    print(f"part 1: {result} rolls of paper can be accessed by a forklift")

    print("-----------------")
    input_file = INPUT_FILE
    print("part 1: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result_no_arg(test_name="part1", expected_result=1602,
                                           method_to_check=puzzle.find_nb_of_accessible_rolls)
    print("part 1: execution time is ", time.time() - t0, " s")
    print(f"part 1: {result} rolls of paper can be accessed by a forklift")

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 2: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result_no_arg(test_name="part2", expected_result=43,
                                           method_to_check=puzzle.find_nb_of_removable_rolls)
    print("part 2: execution time is ", time.time() - t0, " s")
    print(f"part 2: {result} rolls of paper can be removed by the Elves")

    print("-----------------")
    input_file = INPUT_FILE
    print("part 2: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result_no_arg(test_name="part2", expected_result=9518,
                                           method_to_check=puzzle.find_nb_of_removable_rolls)
    print("part 2: execution time is ", time.time() - t0, " s")
    print(f"part 2: {result} rolls of paper can be removed by the Elves")
