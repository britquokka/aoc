import bisect

from dataclasses import dataclass

import logging
import os
import time
from TestUtils import TestUtils

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class DataRange:
    start: int
    size: int


class Map:

    def __init__(self, name: str, ranges: list):
        self.name = name
        self.start_points = [r[0] for r in ranges]
        self.start_points.sort()
        self.end_points = [r[0] + r[2] for r in ranges]
        self.end_points.sort()
        self.delta_by_start_points = {}
        self.nb_ranges = len(self.end_points)
        for r in ranges:
            self.delta_by_start_points[r[0]] = r[1] - r[0]

    def convert(self, data: DataRange):
        prev_start, prev_size = data.start, data.size
        prev_stop = prev_start + prev_size
        delta = 0

        # find in which interval the first data is
        idx_start = bisect.bisect_right(self.start_points, prev_start)
        idx_stop = bisect.bisect_right(self.end_points, prev_start)

        # several case
        # find an interval
        if idx_start-1 == idx_stop:
            delta = self.delta_by_start_points[self.start_points[idx_start-1]]
            prev_stop = min(self.end_points[idx_stop], prev_start + prev_size)
        # don't find an interval
        elif idx_start == idx_stop:
            delta = 0
            if idx_stop != self.nb_ranges:
                prev_stop = min(self.start_points[idx_start], prev_start + prev_size)
            else:
                # after all interval
                prev_stop = prev_start + prev_size

        next_size = prev_stop - prev_start
        next_start = prev_start + delta

        return DataRange(next_start, next_size)


@dataclass(frozen=True)
class Almanac:
    maps: list
    seed_ranges: list

    def convert(self, data: DataRange):
        for a_map in self.maps:
            data = a_map.convert(data)
        return data

    def process_data(self, data: DataRange):
        flag_exit_loop = False
        min_loc = float('inf')
        while not flag_exit_loop:
            out_data = self.convert(data)
            min_loc = min(out_data.start, min_loc)
            next_size = data.size - out_data.size
            if next_size == 0:
                flag_exit_loop = True
            else:
                data = DataRange(data.start + out_data.size, next_size)
        return min_loc

    def find_lowest_locations(self):
        min_loc = float('inf')
        for data in self.seed_ranges:
            out_min_loc = self.process_data(data)
            min_loc = min(out_min_loc, min_loc)
        return min_loc


class Puzzle:
    @staticmethod
    def to_ranges(f):
        ranges = []
        for line in f:
            if line == '\n':
                break
            dst, src, size = list(map(lambda x: int(x), line.strip().split()))
            r = (src, dst, size)
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
    def to_seed_ranges(seed_numbers: list, part2: bool):
        seed_ranges = []
        if part2:
            seed_ranges, i = [], 0
            while i < len(seed_numbers):
                seed_ranges.append(DataRange(seed_numbers[i], seed_numbers[i + 1]))
                i = i + 2
        else:
            for seed_number in seed_numbers:
                seed_ranges.append(DataRange(seed_number, 1))
        return seed_ranges

    @staticmethod
    def to_almanac(file, part2):
        with open(file) as f:
            _, raw_seeds = f.readline().strip().split(':')
            seed_numbers = list(map(lambda x: int(x), raw_seeds.strip().split()))
            f.readline()
            maps = Puzzle.to_maps(f)
            seed_ranges = Puzzle.to_seed_ranges(seed_numbers, part2)
        return Almanac(seed_ranges=seed_ranges, maps=maps)

    def __init__(self, file, part2=False):
        self.almanac = self.to_almanac(file, part2)
        logger.info(self.almanac)

    def find_lowest_location(self):
        return self.almanac.find_lowest_locations()


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

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 2: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file, True)
    lowest_location = TestUtils.check_result_no_arg("part2", 46, puzzle.find_lowest_location)
    print("part 2: execution time is ", time.time() - start, " s")
    print("part 2: the lowest location number is ", lowest_location)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 2: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file, True)
    lowest_location = TestUtils.check_result_no_arg("part2", 6472060, puzzle.find_lowest_location)
    print("part 2: execution time is ", time.time() - start, " s")
    print("part 2: the lowest location number is ", lowest_location)
