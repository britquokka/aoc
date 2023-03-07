import collections
import logging
import os
import time

TEST_DATA_DIR = os.path.join(os.getcwd(), 'data')

logger = logging.getLogger(__name__)


class Puzzle:
    @staticmethod
    def to_crates(file):
        input_rows = []
        stacks = []
        movements = []
        with open(file) as f:
            for line in f:
                # empty line between stacks and movements
                if line == '\n':
                    break
                else:
                    input_rows.append(line)

            # last input_row give nb stacks
            nb_stacks = len(input_rows.pop().split())

            # create list of stack
            for i in range(0, nb_stacks):
                stacks.append(collections.deque())

            # put crates in stacks
            for input_row in input_rows:
                row = list(input_row)
                range_row = range(1, len(row), 4)
                range_stack = range(0, nb_stacks)
                for i, idx_stack in zip(range_row, range_stack):
                    crate = row[i]
                    if crate != ' ':
                        stacks[idx_stack].appendleft(crate)

            # resume file read and retrieve stack movement
            for line in f:
                row = line.split()
                movements.append([int(row[1]), int(row[3]) - 1, int(row[5]) - 1])

        return stacks, movements

    def __init__(self, file):
        self.stacks, self.movements = self.to_crates(file)
        logger.debug(self.stacks)

    def rearrange_crates(self):
        result = ''
        for nb_crates, from_stack_idx, to_stack_idx in self.movements:
            for i in range(0, nb_crates):
                crate_to_move = self.stacks[from_stack_idx].pop()
                self.stacks[to_stack_idx].append(crate_to_move)
        for stack in self.stacks:
            result += stack.pop()
        return result

    def rearrange_crates_with_crate_mover_9001(self):
        result = ''
        for nb_crates, from_stack_idx, to_stack_idx in self.movements:
            crates_to_move = collections.deque()
            for i in range(0, nb_crates):
                crates_to_move.appendleft(self.stacks[from_stack_idx].pop())
            self.stacks[to_stack_idx].extend(crates_to_move)
        for stack in self.stacks:
            result += stack.pop()
        return result


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

    INPUT_FILE_EXAMPLE = os.path.join(TEST_DATA_DIR, 'day5', 'example.txt')
    INPUT_FILE = os.path.join(TEST_DATA_DIR, 'day5', 'input.txt')

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 1: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    top_crates = TestUtils.check_result_no_arg("part1", 'CMZ', puzzle.rearrange_crates)
    print("part 1: execution time is ", time.time() - start, " s")
    print("part 1: the crate ends up on top of each stack are", top_crates)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 1: input file is ", input_file)
    start = time.time()
    for k in range(1, 500):
        puzzle = Puzzle(input_file)
        top_crates = TestUtils.check_result_no_arg("part1", 'QNNTGTPFN', puzzle.rearrange_crates)
    print("part 1: execution time is ", time.time() - start, " s")
    print("part 1: the crate ends up on top of each stack are", top_crates)

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 2: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    top_crates = TestUtils.check_result_no_arg("part2", 'MCD', puzzle.rearrange_crates_with_crate_mover_9001)
    print("part 2: execution time is ", time.time() - start, " s")
    print("part 2: the crate ends up on top of each stack are", top_crates)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 2: input file is ", input_file)
    start = time.time()
    for k in range(1, 500):
        puzzle = Puzzle(input_file)
        top_crates = TestUtils.check_result_no_arg("part2", 'GGNPJBTTR', puzzle.rearrange_crates_with_crate_mover_9001)
    print("part 2: execution time is ", time.time() - start, " s")
    print("part 2: the crate ends up on top of each stack are", top_crates)
