import logging
import os
import time
from dataclasses import dataclass, field

from TestUtils import TestUtils
from enum import IntEnum
import re
import operator

logger = logging.getLogger(__name__)


class ERuleResult(IntEnum):
    accepted = 1
    rejected = 0


class ERatingCategory(IntEnum):
    x = 0
    m = 1
    a = 2
    s = 3


@dataclass
class RatingRange:
    category: ERatingCategory
    r_min: int
    r_max: int

    def intersection(self, other):
        if (self.r_min > other.r_max) or (other.r_min > self.r_max):
            res = None
        else:
            i_max = min(other.r_max, self.r_max)
            i_min = max(other.r_min, self.r_min)
            res = RatingRange(self.category, i_min, i_max)
        return res


@dataclass
class Part:
    rating_by_name = {'x': ERatingCategory.x, 'm': ERatingCategory.m, 'a': ERatingCategory.a, 's': ERatingCategory.s}
    ratings = list


class IRule:
    def apply(self, ratings: list):
        return ERuleResult.rejected

    def apply_ranges(self, ratings: list):
        return None


@dataclass
class RuleResult(IRule):
    result_by_name = {'A': ERuleResult.accepted, 'R': ERuleResult.rejected}
    result: ERuleResult
    results: list = field(default_factory=lambda: [])

    def apply(self, ratings: list):
        return self.result

    def apply_ranges(self, ranges: list):
        if self.result == ERuleResult.accepted:
            self.results.append(ranges)
            logging.debug(ranges)
        return None

    @staticmethod
    def compute_ranges_combinations(ranges):
        result = 1
        for r in ranges:
            result *= r.r_max - r.r_min + 1
        return result

    def compute_total_combinations(self):
        totals = [self.compute_ranges_combinations(ranges) for ranges in self.results]
        return sum(totals)


@dataclass
class Rule(IRule):
    instructions: str
    op: operator
    op1: ERatingCategory
    op2: int
    dst: IRule

    def apply(self, ratings: list):
        result = None
        if self.op(ratings[self.op1], self.op2):
            result = self.dst.apply(ratings)
        return result

    def apply_ranges(self, ranges: list):
        logging.debug(self.instructions)
        else_ranges = None
        rating_range = ranges[self.op1]
        if self.op == operator.gt:
            if_result = rating_range.intersection(RatingRange(self.op1, self.op2+1, 4000))
            else_result = rating_range.intersection(RatingRange(self.op1, 1, self.op2))
        else:
            if_result = rating_range.intersection(RatingRange(self.op1, 1, self.op2 - 1))
            else_result = rating_range.intersection(RatingRange(self.op1, self.op2, 4000))

        if if_result:
            if_ranges = ranges.copy()
            if_ranges[self.op1] = if_result
            self.dst.apply_ranges(if_ranges)

        if else_result:
            else_ranges = ranges.copy()
            else_ranges[self.op1] = else_result

        return else_ranges


@dataclass
class RuleWf(IRule):
    name: str
    workflow_by_name: dict

    def apply(self, ratings: list):
        return self.workflow_by_name[self.name].apply(ratings)

    def apply_ranges(self, ranges: list):
        return self.workflow_by_name[self.name].apply_ranges(ranges)


@dataclass
class Workflow:
    name: str
    rules: list

    def add_rule(self, rule: IRule):
        self.rules.append(rule)

    def apply(self, ratings: list):
        result = ERuleResult.rejected
        flag_exit_loop = False
        i = 0
        while not flag_exit_loop:
            rule = self.rules[i]
            result = rule.apply(ratings)
            # go to next rule if no result
            if result is None:
                i += 1
            else:
                flag_exit_loop = True
        return result

    def apply_ranges(self, ranges: list):
        flag_exit_loop = False
        i = 0
        logging.debug(self.name)
        while not flag_exit_loop:
            rule = self.rules[i]
            else_ranges = rule.apply_ranges(ranges)
            ranges = else_ranges
            i += 1
            if else_ranges is None:
                flag_exit_loop = True
            if i == len(self.rules):
                flag_exit_loop = True
        return None


class WorkflowBuilder:

    def __init__(self, workflow_by_name: dict, result_collector: IRule):
        self.workflow_by_name = workflow_by_name
        self.accepted_rule = result_collector
        self.rejected_rule = RuleResult(ERuleResult.rejected)

    def build_dst_rule(self, dst: str):
        if dst == 'A':
            rule = self.accepted_rule
        elif dst == 'R':
            rule = self.rejected_rule
        else:
            rule = RuleWf(dst, self.workflow_by_name)
        return rule

    def build_rule(self, instructions: list):
        dst = self.build_dst_rule(instructions[1])
        operands = re.split('[<>]', instructions[0])
        op = operator.lt if '<' in instructions[0] else operator.gt
        op1 = Part.rating_by_name[operands[0]]
        op2 = int(operands[1])
        rule = Rule(instructions[0], op, op1, op2, dst)
        return rule

    def build_i_rule(self, rule_str: str):
        instructions = rule_str.split(':')
        if len(instructions) == 1:
            rule = self.build_dst_rule(instructions[0])
        else:
            rule = self.build_rule(instructions)
        return rule

    def build_rules(self, rules_str: str):
        rules_str = rules_str.split(',')
        rules = []
        for rule_str in rules_str:
            rule = self.build_i_rule(rule_str)
            rules.append(rule)
        return rules

    def add_workflow(self, wf_line: str):
        name, rules_str, _ = re.split('{|}|,}', wf_line.strip())
        rules = self.build_rules(rules_str)
        # build workflow if it not already created
        workflow = Workflow(name, rules)
        self.workflow_by_name[name] = workflow


class Puzzle:

    @staticmethod
    def to_workflow(f):
        workflow_by_name = {}
        result_collector = RuleResult(ERuleResult.accepted)
        builder = WorkflowBuilder(workflow_by_name, result_collector)
        flag_exit_loop = False
        while not flag_exit_loop:
            wf_line = f.readline()
            if wf_line != '\n':
                builder.add_workflow(wf_line)
            else:
                flag_exit_loop = True
        return builder.workflow_by_name, result_collector

    @staticmethod
    def to_part(part_str: str):
        ratings = re.split('[=xmas,{}]', part_str)
        ratings = filter(lambda x: len(x) > 0, ratings)
        ratings = [int(r) for r in ratings]
        return ratings

    @staticmethod
    def to_puzzle_input(file):
        with open(file) as f:
            workflow_by_name, result_collector = Puzzle.to_workflow(f)
            parts = [Puzzle.to_part(part_line.strip()) for part_line in f]
        return workflow_by_name, parts, result_collector

    def __init__(self, file):
        self.workflow_by_name, self.parts, self.result_collector = self.to_puzzle_input(file)

        logging.debug(self.workflow_by_name)
        logging.debug(self.parts)

    def compute_sum_of_accepted_ratings(self):
        # total = 0
        # for part in self.parts:
        #    result = self.workflow_by_name['in'].apply(part)
        #    if result == ERuleResult.accepted:
        #        total += sum(part)
        accepted_parts = filter(lambda part: self.workflow_by_name['in'].apply(part), self.parts)
        totals = [sum(part) for part in accepted_parts]
        return sum(totals)

    def compute_combinations_of_ratings(self):
        ranges = [RatingRange(category, 1, 4000) for category in ERatingCategory]
        self.workflow_by_name['in'].apply_ranges(ranges)
        nb_combinations = self.result_collector.compute_total_combinations()
        return nb_combinations


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    TEST_DATA_DIR = os.path.join(os.getcwd(), 'data')
    INPUT_FILE_EXAMPLE = os.path.join(TEST_DATA_DIR, 'day19', 'example.txt')
    INPUT_FILE = os.path.join(TEST_DATA_DIR, 'day19', 'input.txt')

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 1: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    total_ratings = TestUtils.check_result_no_arg("part1", 19114,
                                                  puzzle.compute_sum_of_accepted_ratings)
    print("part 1: execution time is ", time.time() - t0, " s")
    print("part 1: The numbers of cubic meters of lava is ", total_ratings)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 1: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    total_ratings = TestUtils.check_result_no_arg("part1", 368523,
                                                  puzzle.compute_sum_of_accepted_ratings)
    print("part 1: execution time is ", time.time() - t0, " s")
    print("part 1: The numbers of cubic meters of lava is ", total_ratings)

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 2: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    total_ratings_combinations = TestUtils.check_result_no_arg("part2", 167409079868000,
                                                               puzzle.compute_combinations_of_ratings)
    print("part 2: execution time is ", time.time() - t0, " s")
    print("part 2: The number of ratings combinations is ", total_ratings_combinations)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 2: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    total_ratings_combinations = TestUtils.check_result_no_arg("part2", 124167549767307,
                                                               puzzle.compute_combinations_of_ratings)
    print("part 2: execution time is ", time.time() - t0, " s")
    print("part 2: The number of ratings combinations is ", total_ratings_combinations)
