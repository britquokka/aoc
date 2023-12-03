import logging
import os
import time
from enum import Enum

logger = logging.getLogger(__name__)


class Color(Enum):
    BLUE = 0
    GREEN = 1
    RED = 2


class Puzzle:
    @staticmethod
    def to_games(file):
        subsets_by_game_id = {}
        with open(file) as f:
            for line in f:
                raw = line.strip().split(':')
                game, game_id = raw[0].split()
                game_id = int(game_id)
                raw_subsets = raw[1].split(';')
                subsets_in_game = []
                for subset_raw in raw_subsets:
                    raw_cubes = subset_raw.strip().split(',')
                    cubes = [0, 0, 0]
                    for raw_cube in raw_cubes:
                        cube_cnt, color = raw_cube.strip().split()
                        idx = Color[color.upper()].value
                        cubes[idx] = int(cube_cnt)
                    # create a game
                    subsets_in_game.append(cubes)
                    subsets_by_game_id[game_id] = subsets_in_game

        return subsets_by_game_id

    def __init__(self, file):
        self.subsets_by_game = {}
        self.subsets_by_game = self.to_games(file)
        logger.info(self.subsets_by_game)

    @staticmethod
    def is_game_impossible(subset: list, elf_proposal: list):
        flags = [1 for i, j in zip(subset, elf_proposal) if i <= j]
        return sum(flags) != len(subset)

    def sum_possible_game_ids(self):
        # The Elf would first like to know which games would have been possible
        # if the bag contained only 12 red cubes, 13 green cubes, and 14 blue cubes
        elf_proposal = [14, 13, 12]
        possible_game_ids_sum = 0
        for game_id, subsets in self.subsets_by_game.items():
            is_impossible = False
            for subset in subsets:
                is_impossible = is_impossible or Puzzle.is_game_impossible(subset, elf_proposal)
            if not is_impossible:
                possible_game_ids_sum += game_id

        return possible_game_ids_sum

    def power_and_sum_minimum_set(self):
        minimum_set_sum = 0
        for game_id, subsets in self.subsets_by_game.items():
            blue, green, red = subsets[0]
            # find the fewest number of cubes of each color that could have been in the bag to make the game possible
            for subset in subsets[1:]:
                blue, green, red = max(blue, subset[0]), max(green, subset[1]), max(red, subset[2])
            power = blue * green * red
            minimum_set_sum = minimum_set_sum + power

        return minimum_set_sum


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
    TEST_DATA_DIR = os.path.join(os.getcwd(), 'data')
    INPUT_FILE_EXAMPLE = os.path.join(TEST_DATA_DIR, 'day02', 'example.txt')
    INPUT_FILE = os.path.join(TEST_DATA_DIR, 'day02', 'input.txt')

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 1: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    game_ids_sum = TestUtils.check_result_no_arg("part1", 8, puzzle.sum_possible_game_ids)
    print("part 1: execution time is ", time.time() - start, " s")
    print("part 1: the sum of IDs of possible games is ", game_ids_sum)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 1: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    game_ids_sum = TestUtils.check_result_no_arg("part1", 2913, puzzle.sum_possible_game_ids)
    print("part 1: execution time is ", time.time() - start, " s")
    print("part 1: the sum of IDs of possible games is ", game_ids_sum)

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 2: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    minimum_set_of_cubes_power_sum = TestUtils.check_result_no_arg("part2", 2286, puzzle.power_and_sum_minimum_set)
    print("part 2: execution time is ", time.time() - start, " s")
    print("part 2: the sum of the power of the minimum set of cubes is ", minimum_set_of_cubes_power_sum)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 2: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    minimum_set_of_cubes_power_sum = TestUtils.check_result_no_arg("part2", 55593, puzzle.power_and_sum_minimum_set)
    print("part 2: execution time is ", time.time() - start, " s")
    print("part 2: the sum of the power of the minimum set of cubes is ", minimum_set_of_cubes_power_sum)
