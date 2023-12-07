from dataclasses import dataclass

import logging
import os
import time

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Range:
    src_start: int
    dst_start: int
    length: int

    def can_process(self, item: int):
        return self.src_start <= item < (self.src_start + self.length)

    def process(self, item: int):
        return (item - self.src_start) + self.dst_start


@dataclass(frozen=True)
class Map:
    name: str
    ranges: list

    def convert_one(self, item: int):
        new_item = item
        for r in self.ranges:
            if r.can_process(item):
                new_item = r.process(item)
                break
        return new_item

    def _convert(self, items: list):
        next_items = list(map(lambda x: self.convert_one(x), items))
        return next_items

    def convert(self, data: list):
        data = self._convert(data)
        return data


@dataclass(frozen=True)
class Almanac:
    seed_numbers: list
    maps: list

    def find_locations(self, data: list):
        for a_map in self.maps:
            data = a_map.convert(data)
        return data


class Puzzle:
    @staticmethod
    def to_ranges(f):
        ranges = []
        for line in f:
            if line == '\n':
                break
            dst, src, length = list(map(lambda x: int(x), line.strip().split()))
            r = Range(src_start=src, dst_start=dst, length=length)
            ranges.append(r)
        return ranges

    @staticmethod
    def to_maps(f):
        maps = []
        for line in f:
            name, _ = line.strip().split()
            ranges = Puzzle.to_ranges(f)
            maps.append(Map(name=name, ranges=ranges))
        return maps

    @staticmethod
    def to_almanac(file):
        with open(file) as f:
            _, raw_seeds = f.readline().strip().split(':')
            seed_numbers = list(map(lambda x: int(x), raw_seeds.strip().split()))
            f.readline()
            maps = Puzzle.to_maps(f)
        return Almanac(seed_numbers=seed_numbers, maps=maps)

    def __init__(self, file):
        self.almanac = self.to_almanac(file)
        logger.info(self.almanac)

    def find_lowest_location(self):
        locations = self.almanac.find_locations(self.almanac.seed_numbers)
        return min(locations)


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
    INPUT_FILE_EXAMPLE = os.path.join(TEST_DATA_DIR, 'day05', 'example.txt')
    INPUT_FILE = os.path.join(TEST_DATA_DIR, 'day05', 'input.txt')

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 1: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    lowest_location = TestUtils.check_result_no_arg("part1", 35, puzzle.find_lowest_location)
    print("part 1: execution time is ", time.time() - start, " s")
    print("part 1: the lowest location number is ", lowest_location)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 1: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    lowest_location = TestUtils.check_result_no_arg("part1", 331445006, puzzle.find_lowest_location)
    print("part 1: execution time is ", time.time() - start, " s")
    print("part 1: the lowest location number is ", lowest_location)
