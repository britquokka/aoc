import logging
import os
import time
from enum import Enum

TEST_DATA_DIR = os.path.join(os.getcwd(), 'data')

logger = logging.getLogger(__name__)


class Shape(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


class RoundOutcome(Enum):
    LOST = 1
    DRAW = 2
    WIN = 3


class Game:
    rules = {(Shape.ROCK, Shape.ROCK): RoundOutcome.DRAW,
             (Shape.ROCK, Shape.PAPER): RoundOutcome.WIN,
             (Shape.ROCK, Shape.SCISSORS): RoundOutcome.LOST,
             (Shape.PAPER, Shape.ROCK): RoundOutcome.LOST,
             (Shape.PAPER, Shape.PAPER): RoundOutcome.DRAW,
             (Shape.PAPER, Shape.SCISSORS): RoundOutcome.WIN,
             (Shape.SCISSORS, Shape.ROCK): RoundOutcome.WIN,
             (Shape.SCISSORS, Shape.PAPER): RoundOutcome.LOST,
             (Shape.SCISSORS, Shape.SCISSORS): RoundOutcome.DRAW}
    gain_by_shape = {Shape.ROCK: 1, Shape.PAPER: 2, Shape.SCISSORS: 3}
    gain_by_round_outcome = {RoundOutcome.LOST: 0, RoundOutcome.DRAW: 3, RoundOutcome.WIN: 6}

    def __init__(self):
        # retrieve my shape by round result
        self.my_shape_by_round_outcome = {}
        for key, value in self.rules.items():
            shapes = key
            round_outcome = value
            self.my_shape_by_round_outcome[(shapes[0], round_outcome)] = shapes[1]


class Puzzle:
    @staticmethod
    def to_strategy_guide(file):
        strategy_guide = []
        with open(file) as f:
            for line in f:
                column1, column2 = line.strip().split()
                strategy_guide.append((column1, column2))
        return strategy_guide

    def __init__(self, file):
        self.strategy_guide = self.to_strategy_guide(file)
        self.game = Game()

        logger.debug(self.strategy_guide)

    def compute_round_score(self, opponent_shape, my_shape):
        round_outcome = self.game.rules[(opponent_shape, my_shape)]
        score = self.game.gain_by_round_outcome[round_outcome]
        shape_bonus = self.game.gain_by_shape[my_shape]
        return score + shape_bonus

    def compute_round_score_with_round_outcome(self, opponent_shape, round_outcome):
        my_shape = self.game.my_shape_by_round_outcome[(opponent_shape, round_outcome)]
        score = self.game.gain_by_round_outcome[round_outcome]
        shape_bonus = self.game.gain_by_shape[my_shape]
        return score + shape_bonus

    def compute_total_score(self):
        code_column1 = {'A': Shape.ROCK, 'B': Shape.PAPER, 'C': Shape.SCISSORS}
        code_column2 = {'X': Shape.ROCK, 'Y': Shape.PAPER, 'Z': Shape.SCISSORS}

        points = map(lambda columns: self.compute_round_score(code_column1[columns[0]], code_column2[columns[1]]),
                     self.strategy_guide)
        return sum(points)

    def compute_total_score_with_other_guide_meaning(self):
        code_column1 = {'A': Shape.ROCK, 'B': Shape.PAPER, 'C': Shape.SCISSORS}
        code_column2 = {'X': RoundOutcome.LOST, 'Y': RoundOutcome.DRAW, 'Z': RoundOutcome.WIN}
        points = map(
            lambda columns: self.compute_round_score_with_round_outcome(code_column1[columns[0]],
                                                                        code_column2[columns[1]]),
            self.strategy_guide)
        return sum(points)


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

    INPUT_FILE_EXAMPLE = os.path.join(TEST_DATA_DIR, 'day2', 'example.txt')
    INPUT_FILE = os.path.join(TEST_DATA_DIR, 'day2', 'input.txt')

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 1: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    total_score = TestUtils.check_result_no_arg("part1", 15, puzzle.compute_total_score)
    print("part 1: execution time is ", time.time() - start, " s")
    print("part 1: the total score is", total_score)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 1: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    total_score = TestUtils.check_result_no_arg("part1", 13484, puzzle.compute_total_score)
    print("part 1: execution time is ", time.time() - start, " s")
    print("part 1: the total score is", total_score)

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 2: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    total_score = TestUtils.check_result_no_arg("part1", 12, puzzle.compute_total_score_with_other_guide_meaning)
    print("part 2: execution time is ", time.time() - start, " s")
    print("part 2: the total score is", total_score)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 2: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    total_score = TestUtils.check_result_no_arg("part1", 13433, puzzle.compute_total_score_with_other_guide_meaning)
    print("part 2: execution time is ", time.time() - start, " s")
    print("part 2: the total score is", total_score)
