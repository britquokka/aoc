from dataclasses import dataclass
from TestUtils import TestUtils
import logging
import os
import time

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class EngineSchematic:
    part_by_coord: dict
    digit_coords: set
    symbol_coords: set
    asterisk_coords: set

    def find_gears(self):
        gears = []
        # find digit around * symbol
        for asterisk_coord in self.asterisk_coords:
            neighbours = EngineSchematic.get_neighbours(asterisk_coord)
            adjacent_digit_coords = neighbours & self.digit_coords
            gear_part_candidates = set()
            for adjacent_digit_coord in adjacent_digit_coords:
                gear_part_candidates.add(self.part_by_coord[adjacent_digit_coord])
            # A gear is any * symbol that is adjacent to exactly two part numbers
            if len(gear_part_candidates) == 2:
                gears.append(gear_part_candidates)

        return gears

    @staticmethod
    def get_neighbours(coord: tuple):
        (y, x) = coord
        neighbours = [(y - 1, x - 1), (y - 1, x), (y - 1, x + 1), (y, x - 1), (y, x + 1), (y + 1, x - 1), (y + 1, x),
                      (y + 1, x + 1)]
        return set(neighbours)

    def find_part_numbers(self):
        # find digit around symbols
        adjacent_digit_coords = []
        for symbol_coord in self.symbol_coords:
            neighbours = EngineSchematic.get_neighbours(symbol_coord)
            adjacent_digit_coords.extend(neighbours & self.digit_coords)

        # retrieve adjacent engine part number with its coordinate in the schematic
        # part numbers are stored in a dict at several position so use a "set" to count it only once
        part_numbers = set()
        for adjacent_digit_coord in adjacent_digit_coords:
            part_numbers.add(self.part_by_coord[adjacent_digit_coord])
        return part_numbers


@dataclass(frozen=True)
class PartNumber:
    id: int
    part_number: int
    id_counter = 0

    def __radd__(self, other):
        return self.part_number + other

    @staticmethod
    def build(digits: list):
        a_part_number = int(str().join(digits))
        PartNumber.id_counter += 1
        return PartNumber(id=PartNumber.id_counter, part_number=a_part_number)


class Puzzle:
    @staticmethod
    def to_engine_schematic(file):
        part_by_coord = {}
        digit_coords, symbol_coords, asterisk_coords = [], [], []
        with open(file) as f:
            y = 0
            for line in f:
                chars = list(line.strip())
                last_digits_read, last_digits_coords = [], []
                max_x = len(chars)
                for x in range(0, max_x):
                    char, coord = chars[x], (y, x)
                    if char.isdigit():
                        digit_coords.append(coord)
                        last_digits_read.append(char)
                        last_digits_coords.append(coord)
                    elif char != '.':
                        symbol_coords.append(coord)
                        if char == '*':
                            asterisk_coords.append(coord)
                    # build part number with previous digits when current char is no more a digit or before end of line
                    if (not char.isdigit() or (x == max_x - 1)) and len(last_digits_read):
                        part_number = PartNumber.build(last_digits_read)
                        for a_coord in last_digits_coords:
                            part_by_coord[a_coord] = part_number
                        last_digits_read.clear()
                        last_digits_coords.clear()
                y += 1

        return EngineSchematic(part_by_coord=part_by_coord, digit_coords=set(digit_coords),
                               symbol_coords=set(symbol_coords), asterisk_coords=set(asterisk_coords))

    def __init__(self, file):
        self.schematic = self.to_engine_schematic(file)
        logger.info(self.schematic)

    def find_and_sum_part_numbers(self):
        return sum(self.schematic.find_part_numbers())

    def find_and_sum_gear_ratios(self):
        gears = self.schematic.find_gears()
        return sum([(part1.part_number * part2.part_number) for part1, part2 in gears])


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING)
    TEST_DATA_DIR = os.path.join(os.getcwd(), 'data')
    INPUT_FILE_EXAMPLE = os.path.join(TEST_DATA_DIR, 'day03', 'example.txt')
    INPUT_FILE = os.path.join(TEST_DATA_DIR, 'day03', 'input.txt')

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 1: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    part_numbers_sum = TestUtils.check_result_no_arg("part1", 4361, puzzle.find_and_sum_part_numbers)
    print("part 1: execution time is ", time.time() - start, " s")
    print("part 1: the sum of all the part numbers is ", part_numbers_sum)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 1: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    part_numbers_sum = TestUtils.check_result_no_arg("part1", 527364, puzzle.find_and_sum_part_numbers)
    print("part 1: execution time is ", time.time() - start, " s")
    print("part 1: the sum of all the part numbers is ", part_numbers_sum)

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 2: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    gear_ratios_sum = TestUtils.check_result_no_arg("part2", 467835, puzzle.find_and_sum_gear_ratios)
    print("part 2: execution time is ", time.time() - start, " s")
    print("part 2: the sum of all of the gear ratios is ", gear_ratios_sum)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 2: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    gear_ratios_sum = TestUtils.check_result_no_arg("part2", 79026871, puzzle.find_and_sum_gear_ratios)
    print("part 2: execution time is ", time.time() - start, " s")
    print("part 2: the sum of all of the gear ratios is ", gear_ratios_sum)
