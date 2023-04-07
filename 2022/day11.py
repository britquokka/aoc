import collections
import logging
import os
import time
import math
import re
import operator

TEST_DATA_DIR = os.path.join(os.getcwd(), 'data')

logger = logging.getLogger(__name__)


class Monkey:

    def __init__(self, identifier, items, op, operand, test_divisor, followers):
        self.identifier = identifier
        self.items = items
        self.operation = operator.add if op == '+' else operator.mul
        self.operand = operand
        self.test_divisor = test_divisor
        self.followers = followers
        self.nb_inspected_items = 0

    def add_follower(self, other_monkey):
        self.followers.append(other_monkey)

    def inspect_items(self, before_test_operation):
        self.nb_inspected_items += len(self.items)
        while self.items:
            item = self.items.popleft()
            self.inspect_item(item, before_test_operation)

    def inspect_item(self, old_worry_level, before_test_operation):
        if self.operand is None:
            new_worry_level = self.operation(old_worry_level, old_worry_level)
        else:
            new_worry_level = self.operation(old_worry_level, self.operand)

        new_worry_level = before_test_operation(new_worry_level)

        if new_worry_level % self.test_divisor == 0:
            self.followers[0].add_item(new_worry_level)
        else:
            self.followers[1].add_item(new_worry_level)

    def add_item(self, item):
        self.items.append(item)


class Puzzle:
    @staticmethod
    def to_monkeys(file, part2_flag):
        monkeys = {}
        followers_by_monkey_id = {}
        # Monkey 0:
        #  Starting items: 79, 98
        #  Operation: new = old * 19
        #  Test: divisible by 23
        #    If true: throw to monkey 2
        #    If false: throw to monkey 3
        with open(file) as f:
            for line in f:
                row = re.split(r",|:| ", line.strip())
                if row[0] == 'Monkey':
                    monkey_id = int(row[1])
                elif row[0] == 'Starting':
                    items = filter(lambda x: True if x != '' else False, row[3:])
                    items = list(map(lambda x: int(x), items))
                elif row[0] == 'Operation':
                    op = row[5]
                    operand_left = int(row[6]) if row[6] != 'old' else None
                elif row[0] == 'Test':
                    test_divisor = int(row[4])
                elif row[0] == '':
                    pass
                elif row[1] == 'true':
                    true_follower = int(row[6])
                elif row[1] == 'false':
                    false_follower = int(row[6])
                    monkey = Monkey(identifier=monkey_id, items=collections.deque(items),
                                    op=op, operand=operand_left, test_divisor=test_divisor,
                                    followers=[])
                    followers_by_monkey_id[monkey_id] = [true_follower, false_follower]
                    monkeys[monkey_id] = monkey

        # second pass
        for monkey_id in monkeys.keys():
            for follower_id in followers_by_monkey_id[monkey_id]:
                monkeys[monkey_id].add_follower(monkeys[follower_id])

        return monkeys

    @staticmethod
    def before_test_part1(worry_level):
        # // is a floored quotient also referred to as integer division
        return worry_level // 3

    def __init__(self, file, part2_flag: bool = False):
        self.monkeys = self.to_monkeys(file, part2_flag)

    def compute_monkey_business_level_part1(self):
        return self.compute_monkey_business_level(20, lambda x: x // 3)

    def compute_monkey_business_level_part2(self):
        test_divisors = []
        for monkey in self.monkeys.values():
            test_divisors.append(monkey.test_divisor)
        # worry level will become very big so find a way to minimize it.
        # test_operation will continue to work by using the least_common_multiple modulo of the test_divisors
        # lcm function is used even if it is not needed because test_divisors are always prime numbers in input.txt
        least_common_multiple = math.lcm(*test_divisors)
        return self.compute_monkey_business_level(10000, lambda x: x % least_common_multiple)

    def compute_monkey_business_level(self, nb_rounds, before_test_operation):
        for nb_round in range(0, nb_rounds):
            for monkey in self.monkeys.values():
                monkey.inspect_items(before_test_operation)

        results = []
        for monkey in self.monkeys.values():
            results.append(monkey.nb_inspected_items)
        results.sort(reverse=True)
        business_level = results[0] * results[1]

        return business_level


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
    logging.basicConfig(level=logging.DEBUG)

    INPUT_FILE_EXAMPLE = os.path.join(TEST_DATA_DIR, 'day11', 'example.txt')
    INPUT_FILE = os.path.join(TEST_DATA_DIR, 'day11', 'input.txt')

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 1: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    monkey_business_level = TestUtils.check_result_no_arg("part1", 10605, puzzle.compute_monkey_business_level_part1)
    print("part 1: execution time is ", time.time() - start, " s")
    print("part 1: The level of monkey business after 20 rounds is ", monkey_business_level)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 1: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file)
    monkey_business_level = TestUtils.check_result_no_arg("part1", 102399, puzzle.compute_monkey_business_level_part1)
    print("part 1: execution time is ", time.time() - start, " s")
    print("part 1: The level of monkey business after 20 rounds is ", monkey_business_level)

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 2: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file, True)
    monkey_business_level = TestUtils.check_result_no_arg("part2", 2713310158,
                                                          puzzle.compute_monkey_business_level_part2)
    print("part 2: execution time is ", time.time() - start, " s")
    print("part 2: The level of monkey business after 10000 rounds is ", monkey_business_level)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 2: input file is ", input_file)
    start = time.time()
    puzzle = Puzzle(input_file, True)
    monkey_business_level = TestUtils.check_result_no_arg("part2", 23641658401,
                                                          puzzle.compute_monkey_business_level_part2)
    print("part 2: execution time is ", time.time() - start, " s")
    print("part 2: The level of monkey business after 10000 rounds is ", monkey_business_level)
