import logging
import os
import time

logger = logging.getLogger(__name__)


class Puzzle:
    @staticmethod
    def to_cards(file):
        numbers_by_card_id = {}
        with open(file) as f:
            for line in f:
                raw = line.strip().split(':')
                card, card_id = raw[0].split()
                card_id = int(card_id)
                raw_lists = raw[1].split('|')
                numbers_lists = []
                for raw_list in raw_lists:
                    numbers = set(raw_list.strip().split())
                    # create a card
                    numbers_lists.append(numbers)
                    numbers_by_card_id[card_id] = numbers_lists

        return numbers_by_card_id

    def __init__(self, file):
        self.numbers_by_card = self.to_cards(file)
        logger.info(self.numbers_by_card)

    def compute_points(self):
        nb_points = 0
        for winning_numbers, numbers_you_have in self.numbers_by_card.values():
            # your_winning_numbers = numbers_you_have.intersection(winning_numbers)
            # or intersection with &
            nb_winning_numbers = len(numbers_you_have & winning_numbers)
            new_points = pow(2, nb_winning_numbers-1) if nb_winning_numbers else 0
            nb_points += new_points

        return nb_points

    def compute_nb_cards(self):
        counters = [1] * len(self.numbers_by_card.keys())
        for card_id, (winning_numbers, numbers_you_have) in self.numbers_by_card.items():
            nb_winning_numbers = len(numbers_you_have & winning_numbers)
            idx_cnt = card_id - 1
            if nb_winning_numbers > 0:
                for i in range(idx_cnt+1, idx_cnt+1+nb_winning_numbers):
                    counters[i] = counters[i] + counters[idx_cnt]

        return sum(counters)


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
    INPUT_FILE_EXAMPLE = os.path.join(TEST_DATA_DIR, 'day04', 'example.txt')
    INPUT_FILE = os.path.join(TEST_DATA_DIR, 'day04', 'input.txt')

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 1: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    points = TestUtils.check_result_no_arg("part1", 13, puzzle.compute_points)
    print("part 1: execution time is ", time.time() - start, " s")
    print("part 1: Cards are worth ", points, " points.")

    print("-----------------")
    input_file = INPUT_FILE
    print("part 1: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    points = TestUtils.check_result_no_arg("part1", 17782, puzzle.compute_points)
    print("part 1: execution time is ", time.time() - start, " s")
    print("part 1: Cards are worth ", points, " points.")

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 2: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    nb_cards = TestUtils.check_result_no_arg("part1", 30, puzzle.compute_nb_cards)
    print("part 2: execution time is ", time.time() - start, " s")
    print("part 2: The total number of scratchcards is ", nb_cards)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 2: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    nb_cards = TestUtils.check_result_no_arg("part1", 8477787, puzzle.compute_nb_cards)
    print("part 2: execution time is ", time.time() - start, " s")
    print("part 2: The total number of scratchcards is ", nb_cards)
