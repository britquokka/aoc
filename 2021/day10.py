import collections
import logging
import os
import time
from TestUtils import TestUtils


logger = logging.getLogger(__name__)


class Puzzle:
    points_by_illegal_character = {')': 3, ']': 57, '}': 1197, '>': 25137}
    open_brackets = {'(', '{', '<', '['}
    inv_closing_bracket = {')': '(', ']': '[', '}': '{', '>': '<'}
    points_by_character = {'(': 1, '[': 2, '{': 3, '<': 4}

    @staticmethod
    def to_navigation_subsystem(file):
        with open(file) as f:
            navigation_subsystem = [line.strip() for line in f]
        return navigation_subsystem

    def __init__(self, file):
        self.navigation_subsystem = Puzzle.to_navigation_subsystem(file)

    def compute_total_syntax_error_score(self):
        lifo = collections.deque()
        illegal_characters = []

        for line in self.navigation_subsystem:
            for c in line:
                if c in Puzzle.open_brackets:
                    lifo.append(c)
                else:
                    prev = lifo.pop()
                    if prev != Puzzle.inv_closing_bracket[c]:
                        illegal_characters.append(c)
                        break

        # compute score
        scores = map(lambda char: Puzzle.points_by_illegal_character[char], illegal_characters)
        total = sum(scores)

        return total

    @staticmethod
    def compute_score(remaining_chars):
        score = 0
        brackets = list(remaining_chars)
        brackets.reverse()
        for c in brackets:
            score = score * 5 + Puzzle.points_by_character[c]
        return score

    @staticmethod
    def process_line(line):
        illegal_characters = []
        fifo = collections.deque(line)
        lifo = collections.deque()
        while fifo:
            c = fifo.popleft()
            if c in Puzzle.open_brackets:
                lifo.append(c)
            else:
                # complete chunk by checking stored characters
                prev = lifo.pop()
                if prev != Puzzle.inv_closing_bracket[c]:
                    illegal_characters.append(c)
                    # end so raz to exit
                    fifo.clear()
                    lifo.clear()
        # lifo stores all remaining brackets not completed
        return lifo

    @staticmethod
    def compute_line_score(line: str):
        remaining_chars = Puzzle.process_line(line)
        return Puzzle.compute_score(remaining_chars)

    def compute_middle_score(self):
        scores = [self.compute_line_score(line) for line in self.navigation_subsystem]
        scores = list(filter(lambda score: score > 0, scores))
        scores.sort()
        index = len(scores)//2
        return scores[index]


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING)
    TEST_DATA_DIR = os.path.join(os.getcwd(), 'data')
    INPUT_FILE_EXAMPLE = os.path.join(TEST_DATA_DIR, 'day10', 'example.txt')
    INPUT_FILE = os.path.join(TEST_DATA_DIR, 'day10', 'input.txt')

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 1: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result_no_arg("part1", 26397,
                                           puzzle.compute_total_syntax_error_score)
    print("part 1: execution time is ", time.time() - t0, " s")
    print("part 1: The total syntax error score is", result)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 1: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result_no_arg("part1", 341823,
                                           puzzle.compute_total_syntax_error_score)
    print("part 1: execution time is ", time.time() - t0, " s")
    print("part 1: The total syntax error score is", result)

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 2: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result_no_arg("part2", 288957,
                                           puzzle.compute_middle_score)
    print("part 2: execution time is ", time.time() - t0, " s")
    print("part 2: The middle score is", result)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 2: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result_no_arg("part2", 2801302861,
                                           puzzle.compute_middle_score)
    print("part 2: execution time is ", time.time() - t0, " s")
    print("part 2: The middle score is", result)
