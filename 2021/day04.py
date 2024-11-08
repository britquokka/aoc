import logging
import os
import time
from TestUtils import TestUtils

logger = logging.getLogger(__name__)


class Board:

    def __init__(self, a_raw_board: list):
        self.raw_board = a_raw_board
        self.max_y = len(self.raw_board)
        self.max_x = len(self.raw_board[0])
        self.counters_by_y = [0] * self.max_y
        self.counters_by_x = [0] * self.max_x
        self.pos_by_value = Board.build(self.raw_board)
        self.values = set(self.pos_by_value.keys())
        self.win_value = None

    def mark_and_check(self, bingo_value: int):
        is_winner = False
        pos = self.pos_by_value.get(bingo_value)
        if pos is not None:
            y, x = pos
            self.values.remove(bingo_value)
            self.counters_by_y[y] += 1
            self.counters_by_x[x] += 1
            is_winner = (self.max_x == self.counters_by_y[y]) | (self.max_y == self.counters_by_x[x])
            self.win_value = bingo_value if is_winner else None
        return is_winner

    @staticmethod
    def build(a_raw_bord: list):
        pos_by_value = {}
        for y in range(len(a_raw_bord)):
            row = a_raw_bord[y]
            for x in range(len(row)):
                pos_by_value[row[x]] = (y, x)
        return pos_by_value

    def sum_left(self):
        return sum(self.values)

    def compute_final_score(self):
        return None if self.win_value is None else self.sum_left()*self.win_value


class Puzzle:

    @staticmethod
    def to_bingo_input(file):
        boards = []
        with open(file) as f:
            draw_numbers = list(map(lambda x: int(x), f.readline().strip().split(",")))
            for line in f:
                row = line.strip().split()
                if len(row) == 0:
                    board = []
                    boards.append(board)
                else:
                    board.append(list(map(lambda x: int(x), row)))
        return draw_numbers, boards

    def __init__(self, file):
        self.draw_numbers, raw_boards = self.to_bingo_input(file)
        self.boards = [Board(b) for b in raw_boards]
        logger.debug(self.draw_numbers)
        logger.debug(self.boards)

    def find_final_score(self):
        for draw_number in self.draw_numbers:
            for board in self.boards:
                is_winning = board.mark_and_check(draw_number)
                if is_winning:
                    return board.compute_final_score()
        return 0

    @staticmethod
    def find_win_boards(number: int, boards: list):
        win_boards = list(filter(lambda b: b.mark_and_check(number), boards))
        return win_boards

    def find_final_score_for_last_winning_board(self):
        boards = self.boards.copy()
        last_win_board = None
        for draw_number in self.draw_numbers:
            last_win_boards = Puzzle.find_win_boards(draw_number, boards)
            boards = [b for b in boards if b not in last_win_boards]
            if len(last_win_boards) > 0:
                last_win_board = last_win_boards[-1]
        return last_win_board.compute_final_score()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    TEST_DATA_DIR = os.path.join(os.getcwd(), 'data')
    INPUT_FILE_EXAMPLE = os.path.join(TEST_DATA_DIR, 'day04', 'example.txt')
    INPUT_FILE = os.path.join(TEST_DATA_DIR, 'day04', 'input.txt')

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 1: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result_no_arg("part1", 4512, puzzle.find_final_score)
    print("part 1: execution time is ", time.time() - t0, " s")
    print("part 1: The final score for the selected board is ", result)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 1: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result_no_arg("part1", 16674, puzzle.find_final_score)
    print("part 1: execution time is ", time.time() - t0, " s")
    print("part 1: The final score for the selected board is ", result)

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 2: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result_no_arg("part2", 1924,
                                           puzzle.find_final_score_for_last_winning_board)
    print("part 2: execution time is ", time.time() - t0, " s")
    print("part 2: The final score for the last winning board is ", result)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 2: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result_no_arg("part2", 7075,
                                           puzzle.find_final_score_for_last_winning_board)
    print("part 2: execution time is ", time.time() - t0, " s")
    print("part 2: The final score for the last winning board is ", result)
