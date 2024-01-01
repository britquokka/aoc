from dataclasses import dataclass
import logging
import os
import time
from enum import IntEnum


from TestUtils import TestUtils

logger = logging.getLogger(__name__)


class ReflectionType(IntEnum):
    HORIZONTAL = 1
    VERTICAL = 2


@dataclass
class Reflection:
    type: ReflectionType
    idx: int

    def weight(self):
        number = self.idx + 1
        w = number if self.type == ReflectionType.VERTICAL else number * 100
        return w


@dataclass
class Pattern:
    rows: list

    @staticmethod
    def transpose(rows: list):
        return ["".join(col) for col in zip(*rows)]

    def check_proposal(self, lines, proposal):
        return all([lines[i] == lines[j] for i, j in zip(range(proposal + 1, len(lines)), range(proposal, -1, -1))])

    def find_reflection_number(self, lines: list):
        flag_exit_loop, found = False, False
        proposal = 0
        while not flag_exit_loop:
            found = self.check_proposal(lines, proposal)
            if not found:
                proposal += 1
                flag_exit_loop = False if proposal < len(lines)-1 else True
            else:
                flag_exit_loop = True
        return found, proposal

    def find_reflection(self):
        reflexion = None
        rtype = ReflectionType.HORIZONTAL
        found, number = self.find_reflection_number(self.rows)
        if not found:
            rtype = ReflectionType.VERTICAL
            columns = self.transpose(self.rows)
            found, number = self.find_reflection_number(columns)
        if found:
            reflexion = Reflection(rtype, number)
        return reflexion


@dataclass
class SmudgedPattern(Pattern):
    allow_fix_smudge: bool

    def fix_smudge_once(self, line1: str, line2: str):
        is_equal = (line1 == line2)
        if not is_equal and self.allow_fix_smudge:
            nb_common_char = sum([(c1 == c2) for c1, c2 in zip(line1, line2)])
            if (len(line1) - 1) == nb_common_char:
                is_equal = True
                self.allow_fix_smudge = False
        return is_equal

    def check_proposal(self, lines, proposal):
        self.allow_fix_smudge = True
        found = all([self.fix_smudge_once(lines[i], lines[j])
                    for i, j in zip(range(proposal + 1, len(lines)), range(proposal, -1, -1))])
        return found and not self.allow_fix_smudge


class Puzzle:
    @staticmethod
    def build_pattern(rows: list, fix_smudge: bool):
        if fix_smudge:
            pattern = SmudgedPattern(rows, fix_smudge)
        else:
            pattern = Pattern(rows)
        return pattern

    @staticmethod
    def to_patterns(file, fix_smudge):
        patterns = []
        rows = []
        with open(file) as f:
            for line in f:
                row = line.strip()
                if row == '':
                    pattern = Puzzle.build_pattern(rows, fix_smudge)
                    patterns.append(pattern)
                    rows = []
                else:
                    rows.append(row)
            # last
            pattern = Puzzle.build_pattern(rows, fix_smudge)
            patterns.append(pattern)
        return patterns

    def __init__(self, file, fix_smudge=False):
        self.patterns = self.to_patterns(file, fix_smudge)

    def summarize_notes(self):
        total = 0
        for pattern in self.patterns:
            reflexion = pattern.find_reflection()
            if reflexion:
                total += reflexion.weight()

        return total


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING)
    TEST_DATA_DIR = os.path.join(os.getcwd(), 'data')
    INPUT_FILE_EXAMPLE = os.path.join(TEST_DATA_DIR, 'day13', 'example.txt')
    INPUT_FILE = os.path.join(TEST_DATA_DIR, 'day13', 'input.txt')

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 1: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    pattern_notes_number = TestUtils.check_result_no_arg("part1", 405, puzzle.summarize_notes)
    print("part 1: execution time is ", time.time() - start, " s")
    print("part 1: The number after summarizing all of my notes is  ", pattern_notes_number)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 1: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    pattern_notes_number = TestUtils.check_result_no_arg("part1", 30518, puzzle.summarize_notes)
    print("part 1: execution time is ", time.time() - start, " s")
    print("part 1: The number after summarizing all of my notes is  ", pattern_notes_number)

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 2: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file, True)
    pattern_notes_number = TestUtils.check_result_no_arg("part2", 400, puzzle.summarize_notes)
    print("part 2: execution time is ", time.time() - start, " s")
    print("part 2: The number after summarizing all of my notes is  ", pattern_notes_number)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 2: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file, True)
    pattern_notes_number = TestUtils.check_result_no_arg("part2", 36735, puzzle.summarize_notes)
    print("part 2: execution time is ", time.time() - start, " s")
    print("part 2: The number after summarizing all of my notes is  ", pattern_notes_number)
