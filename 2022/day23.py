import logging
import os
import time


TEST_DATA_DIR = os.path.join(os.getcwd(), 'data')

logger = logging.getLogger(__name__)


class Direction:
    NORTH: int = 0
    SOUTH: int = 1
    WEST: int = 2
    EAST: int = 3


class Puzzle:
    @staticmethod
    def to_elves(file):
        elves = {}
        x = 3
        y = 9
        elf_id = 0
        with open(file) as f:
            for line in f:
                tiles = line.strip()
                for tile in tiles:
                    if tile == '#':
                        elves[elf_id] = (x, y)
                        elf_id += 1
                    x += 1
                y -= 1
                x = 3
        return elves

    def __init__(self, file):
        self.elves = self.to_elves(file)
        logger.debug(self.elves)

    @staticmethod
    def get_neighbours(coord, direction):
        x, y = coord
        if direction == Direction.NORTH:
            neighbours = [(x - 1, y + 1), (x, y + 1), (x + 1, y + 1)]
        elif direction == Direction.SOUTH:
            neighbours = [(x - 1, y - 1), (x, y - 1), (x + 1, y - 1)]
        elif direction == Direction.WEST:
            neighbours = [(x - 1, y - 1), (x - 1, y), (x - 1, y + 1)]
        else:
            neighbours = [(x + 1, y + 1), (x + 1, y), (x + 1, y - 1)]

        return set(neighbours)

    @staticmethod
    def move(coord, direction):
        x, y = coord
        if direction == Direction.NORTH:
            next_p = (x, y + 1)
        elif direction == Direction.SOUTH:
            next_p = (x, y - 1)
        elif direction == Direction.WEST:
            next_p = (x - 1, y)
        else:
            next_p = (x + 1, y)

        return next_p

    @staticmethod
    def get_next_destination(coord, first_direction, elves_set):
        dst = coord
        has_neighbour = False
        proposition = None
        # try to move N, S , W, E then modulo S, W, E, N ... modulo 4
        for i in range(0, 4):
            direction = (first_direction + i) % 4
            neighbours = Puzzle.get_neighbours(coord, direction)
            occupied_tiles = neighbours.intersection(elves_set)
            if len(occupied_tiles) == 0:
                if proposition is None:
                    proposition = Puzzle.move(coord, direction)
            else:
                has_neighbour = True

        if has_neighbour and proposition is not None:
            dst = proposition

        return dst

    @staticmethod
    def get_min(p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        res = (min(x1, x2), min(y1, y2))
        return res

    @staticmethod
    def get_max(p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        res = (max(x1, x2), max(y1, y2))
        return res

    @staticmethod
    def get_limits(c, min_c, max_c):
        max_c = Puzzle.get_max(c, max_c)
        min_c = Puzzle.get_min(c, min_c)
        return min_c, max_c

    @staticmethod
    def move_all_elves(direction, elves, elves_set):

        elves_dst = {}
        elves_to_restore = []
        elf_by_dst = {}
        min_coord, max_coord = elves[0], elves[0]
        for elf_id, coord in elves.items():
            dst = Puzzle.get_next_destination(coord, direction, elves_set)
            # other elf want to go to the same dst
            elf_id_with_same_dst = elf_by_dst.get(dst)
            if elf_id_with_same_dst is None:
                min_coord, max_coord = Puzzle.get_limits(dst, min_coord, max_coord)
                elves_dst[elf_id] = dst
                elf_by_dst[dst] = elf_id
            else:
                elves_to_restore.append(elf_id)
                elves_to_restore.append(elf_id_with_same_dst)

        # restore position of elves if needed
        for elf_id in elves_to_restore:
            elves_dst[elf_id] = elves[elf_id]

        return elves_dst, min_coord, max_coord

    def compute_nb_empty_ground_tiles(self, nb_round: int):
        direction = Direction.NORTH

        for round_cnt in range(0, nb_round):
            elves_set = set(self.elves.values())
            self.elves, min_coord, max_coord = Puzzle.move_all_elves(direction, self.elves, elves_set)
            direction = (direction+1) % 4

        x_min, y_min = min_coord
        x_max, y_max = max_coord
        nb_tiles = (x_max + 1 - x_min) * (y_max + 1 - y_min)
        nb_empty_tiles = nb_tiles - len(self.elves.values())
        return nb_empty_tiles

    def compute_first_round_with_no_move(self):
        direction = Direction.NORTH
        rnd_count = 0
        move_flag = True
        elves_set = set(self.elves.values())
        while move_flag:
            rnd_count += 1
            self.elves, min_coord, max_coord = Puzzle.move_all_elves(direction, self.elves, elves_set)
            direction = (direction+1) % 4
            next_elves_set = set(self.elves.values())
            if next_elves_set == elves_set:
                move_flag = False
            elves_set = next_elves_set

        return rnd_count


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

    INPUT_FILE_EXAMPLE = os.path.join(TEST_DATA_DIR, 'day23', 'example.txt')
    INPUT_FILE = os.path.join(TEST_DATA_DIR, 'day23', 'input.txt')

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 1: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    nb_empty_ground_tiles = TestUtils.check_result("part1", 110, puzzle.compute_nb_empty_ground_tiles, 10)
    print("part 1: execution time is ", time.time() - start, " s")
    print("part 1: the number empty ground tiles, does that rectangle contain, is", nb_empty_ground_tiles)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 1: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    nb_empty_ground_tiles = TestUtils.check_result("part1", 3940, puzzle.compute_nb_empty_ground_tiles, 10)
    print("part 1: execution time is ", time.time() - start, " s")
    print("part 1: the number empty ground tiles, does that rectangle contain, is", nb_empty_ground_tiles)

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 2: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    nb_round_with_no_move = TestUtils.check_result_no_arg("part2", 20, puzzle.compute_first_round_with_no_move)
    print("part 2: execution time is ", time.time() - start, " s")
    print("part 2: the number of the first round where no Elf moves is", nb_round_with_no_move)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 2: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    nb_round_with_no_move = TestUtils.check_result_no_arg("part2", 990, puzzle.compute_first_round_with_no_move)
    print("part 2: execution time is ", time.time() - start, " s")
    print("part 2: the number of the first round where no Elf moves is", nb_round_with_no_move)
