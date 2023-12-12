import logging
import os
import time
from TestUtils import TestUtils
from enum import IntEnum

logger = logging.getLogger(__name__)


class HandType(IntEnum):
    FIVE_OF_A_KIND = 7
    FOUR_OF_A_KIND = 6
    FULL_HOUSE = 5
    THREE_OF_A_KIND = 4
    TWO_PAIR = 3
    ONE_PAIR = 2
    HIGH_CARD = 1


class Puzzle:

    strength_by_label = {'A': 'E', 'K': 'D', 'Q': 'C',  'J': 'B', 'T': 'A', '9': '9',
                         '8': '8', '7': '7', '6': '6', '5': '5', '4': '4', '3': '3', '2': '2'}

    strength_with_joker_by_label = {'A': 'E', 'K': 'D', 'Q': 'C', 'J': '1', 'T': 'A', '9': '9',
                                    '8': '8', '7': '7', '6': '6', '5': '5', '4': '4', '3': '3', '2': '2'}

    @staticmethod
    def to_hands(file):
        hands = []
        with open(file) as f:
            for line in f:
                hand, bid = line.strip().split()
                hands.append((hand, int(bid)))

        return hands

    def __init__(self, file):
        self.hands = self.to_hands(file)

    @staticmethod
    def get_hand_type_by_counters(counters):
        hand_type = HandType.HIGH_CARD
        if counters[0] == 5:
            hand_type = HandType.FIVE_OF_A_KIND
        elif counters[0] == 4:
            hand_type = HandType.FOUR_OF_A_KIND
        elif counters[0] == 3:
            if counters[1] == 2:
                hand_type = HandType.FULL_HOUSE
            else:
                hand_type = HandType.THREE_OF_A_KIND
        elif counters[0] == 2:
            if counters[1] == 2:
                hand_type = HandType.TWO_PAIR
            else:
                hand_type = HandType.ONE_PAIR
        elif counters[0] == 1:
            hand_type = HandType.HIGH_CARD

        return hand_type

    @staticmethod
    def find_hand_type(hand):
        counters = [hand.count(c) for c in set(hand)]
        counters.sort(reverse=True)
        hand_type = Puzzle.get_hand_type_by_counters(counters)
        return hand_type

    @staticmethod
    def find_hand_type_with_joker(hand):
        nb_jokers = hand.count('J')
        counters = [0]
        if nb_jokers == 0:
            counters = [hand.count(c) for c in set(hand)]
        elif nb_jokers < 5:
            hand = hand.replace('J', '')
            counters = [hand.count(c) for c in set(hand)]

        counters.sort(reverse=True)
        # increase max counter to have the strongest type
        counters[0] += nb_jokers
        hand_type = Puzzle.get_hand_type_by_counters(counters)

        return hand_type

    @staticmethod
    def sort_and_compute_total_winnings(typed_hands: list):
        # sort is done with HandType(IntEnum) and conv_hands
        typed_hands.sort(reverse=True)
        rank = len(typed_hands)
        total = 0
        for _, _, hand, bid in typed_hands:
            total += bid * rank
            rank -= 1
        return total

    def compute_total_winnings(self):
        typed_hands = []

        for hand, bid in self.hands:
            hand_type = Puzzle.find_hand_type(hand)
            conv_hand = [puzzle.strength_by_label[c] for c in hand]
            typed_hands.append((hand_type, conv_hand, hand, bid))

        total = Puzzle.sort_and_compute_total_winnings(typed_hands)

        return total

    def compute_total_winnings_with_joker(self):
        typed_hands = []

        for hand, bid in self.hands:
            hand_type = Puzzle.find_hand_type_with_joker(hand)
            conv_hand = [puzzle.strength_with_joker_by_label[c] for c in hand]
            typed_hands.append((hand_type, conv_hand, hand, bid))

        total = Puzzle.sort_and_compute_total_winnings(typed_hands)

        return total


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    logging.basicConfig(level=logging.WARNING)
    TEST_DATA_DIR = os.path.join(os.getcwd(), 'data')
    INPUT_FILE_EXAMPLE = os.path.join(TEST_DATA_DIR, 'day07', 'example.txt')
    INPUT_FILE = os.path.join(TEST_DATA_DIR, 'day07', 'input.txt')

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 1: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    total_winnings = TestUtils.check_result_no_arg("part1", 6440, puzzle.compute_total_winnings)
    print("part 1: execution time is ", time.time() - start, " s")
    print("part 1: The total winnings of this set of hands is ", total_winnings)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 1: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    total_winnings = TestUtils.check_result_no_arg("part1", 246409899, puzzle.compute_total_winnings)
    print("part 1: execution time is ", time.time() - start, " s")
    print("part 1: The total winnings of this set of hands is ", total_winnings)

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 2: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    total_winnings = TestUtils.check_result_no_arg("part2", 5905, puzzle.compute_total_winnings_with_joker)
    print("part 2: execution time is ", time.time() - start, " s")
    print("part 2: The total winnings with joker of this set of hands is ", total_winnings)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 2: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    total_winnings = TestUtils.check_result_no_arg("part2", 244848487, puzzle.compute_total_winnings_with_joker)
    print("part 2: execution time is ", time.time() - start, " s")
    print("part 2: The total winnings with joker of this set of hands is ", total_winnings)
