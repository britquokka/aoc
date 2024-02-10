import logging
import os
import time
from dataclasses import dataclass

from TestUtils import TestUtils
from enum import IntEnum
import re
import operator

logger = logging.getLogger(__name__)


class ERuleResult(IntEnum):
    accepted = 1
    rejected = 0


class ERating(IntEnum):
    x = 0
    m = 1
    a = 2
    s = 3


@dataclass
class Part:
    rating_by_name = {'x': ERating.x, 'm': ERating.m, 'a': ERating.a, 's': ERating.s}
    ratings = list


class IRule:
    def apply(self, ratings: list):
        return ERuleResult.rejected


@dataclass
class RuleResult(IRule):
    result_by_name = {'A': ERuleResult.accepted, 'R': ERuleResult.rejected}
    result: ERuleResult

    def apply(self, ratings: list):
        return self.result


@dataclass
class Rule(IRule):
    op: operator
    op1: ERating
    op2: int
    dst: IRule

    def apply(self, ratings: list):
        result = None
        if self.op(ratings[self.op1], self.op2):
            result = self.dst.apply(ratings)
        return result


@dataclass
class RuleWf(IRule):
    name: str
    workflow_by_name: dict

    def apply(self, ratings: list):
        return self.workflow_by_name[self.name].apply(ratings)


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
            if result is None:
                i += 1
            else:
                flag_exit_loop = True
        return result


class WorkflowBuilder:

    def __init__(self, workflow_by_name: dict):
        self.workflow_by_name = workflow_by_name

    def build_dst_rule(self, dst: str):
        if dst == 'A':
            rule = RuleResult(ERuleResult.accepted)
        elif dst == 'R':
            rule = RuleResult(ERuleResult.rejected)
        else:
            rule = RuleWf(dst, self.workflow_by_name)
        return rule

    def build_rule(self, instructions: list):
        dst = self.build_dst_rule(instructions[1])
        operands = re.split('[<>]', instructions[0])
        op = operator.lt if '<' in instructions[0] else operator.gt
        op1 = Part.rating_by_name[operands[0]]
        op2 = int(operands[1])
        rule = Rule(op, op1, op2, dst)
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
        builder = WorkflowBuilder(workflow_by_name)
        flag_exit_loop = False
        while not flag_exit_loop:
            wf_line = f.readline()
            if wf_line != '\n':
                builder.add_workflow(wf_line)
            else:
                flag_exit_loop = True
        return builder.workflow_by_name

    @staticmethod
    def to_part(part_str: str):
        ratings = re.split('[=xmas,{}]', part_str)
        ratings = filter(lambda x: len(x) > 0, ratings)
        ratings = [int(r) for r in ratings]
        return ratings

    @staticmethod
    def to_puzzle_input(file):
        with open(file) as f:
            workflow_by_name = Puzzle.to_workflow(f)
            parts = [Puzzle.to_part(part_line.strip()) for part_line in f]
        return workflow_by_name, parts

    def __init__(self, file):
        self. workflow_by_name, self.parts = self.to_puzzle_input(file)

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
