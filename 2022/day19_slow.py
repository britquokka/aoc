import logging
import os

import time
from dataclasses import dataclass, field

import collections


TEST_DATA_DIR = os.path.join(os.getcwd(), 'data')

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Resource:
    ore: int = 0
    clay: int = 0
    obsidian: int = 0
    geode: int = 0

    def __add__(self, other):
        ore = self.ore + other.ore
        clay = self.clay + other.clay
        obsidian = self.obsidian + other.obsidian
        geodes = self.geode + other.geode
        return Resource(ore, clay, obsidian, geodes)

    def __sub__(self, other):
        ore = self.ore - other.ore
        clay = self.clay - other.clay
        obsidian = self.obsidian - other.obsidian
        geodes = self.geode - other.geode
        return Resource(ore, clay, obsidian, geodes)

    @staticmethod
    def max(a, b):
        ore = max(a.ore, b.ore)
        clay = max(a.clay, b.clay)
        obsidian = max(a.obsidian, b.obsidian)
        geodes = max(a.geode, b.geode)
        return Resource(ore, clay, obsidian, geodes)


class RobotType:
    ORE = "ORE"
    CLAY = "CLAY"
    OBSIDIAN = "OBSIDIAN"
    GEODE = "GEODE"


@dataclass
class Robot:
    type: str
    cost: Resource


@dataclass
class Blueprint:
    id: int
    robot_by_type: field(default_factory=lambda: {})


class QualityLevelCalculator:
    @staticmethod
    def to_blueprints(file):
        blueprints = []
        with open(file) as f:
            for line in f:
                int_list = [int(i) for i in line.replace(':', ' ').split() if i.isdigit()]
                blueprint_id = int_list[0]
                cost = Resource(ore=int_list[1])
                ore_robot = Robot(RobotType.ORE, cost)
                cost = Resource(ore=int_list[2])
                clay_robot = Robot(RobotType.CLAY, cost)
                cost = Resource(ore=int_list[3], clay=int_list[4])
                obsidian_robot = Robot(RobotType.OBSIDIAN, cost)
                cost = Resource(ore=int_list[5], obsidian=int_list[6])
                geode_robot = Robot(RobotType.GEODE, cost)
                blueprint = Blueprint(blueprint_id, {RobotType.ORE: ore_robot,
                                                     RobotType.CLAY: clay_robot,
                                                     RobotType.OBSIDIAN: obsidian_robot,
                                                     RobotType.GEODE: geode_robot})
                blueprints.append(blueprint)

        return blueprints

    def __init__(self, file):
        self.blueprints = self.to_blueprints(file)

    @staticmethod
    def first_integer_sum(n):
        return n * (n+1) // 2

    @staticmethod
    def depth_first_search(initial_time_left: int,
                           blueprint: Blueprint):
        initial_ready_robots = Resource(ore=1)
        initial_resources = Resource()
        next_resources = Resource()
        max_open_geodes = nb_search_paths = 0
        max_robots_per_mn = Resource()
        cost_robot_ore = blueprint.robot_by_type[RobotType.ORE].cost
        cost_robot_clay = blueprint.robot_by_type[RobotType.CLAY].cost
        cost_robot_obs = blueprint.robot_by_type[RobotType.OBSIDIAN].cost
        cost_robot_geode = blueprint.robot_by_type[RobotType.GEODE].cost
        for robot in blueprint.robot_by_type.values():
            max_robots_per_mn = Resource.max(max_robots_per_mn, robot.cost)

        # init dfs
        visited = set()
        lifo = collections.deque()
        lifo.append((initial_time_left, initial_resources, initial_ready_robots))

        while lifo:
            node = lifo.pop()

            if node not in visited:
                visited.add(node)
                time_left, resources, robots = node
                logger.debug("time:%s, resource:%s, ready robots:%s", time_left, resources, robots)

                # compute max expected geode for this path if we manage to build one more geode robot per mn
                max_expected_geode = resources.geode + robots.geode * time_left \
                                     + QualityLevelCalculator.first_integer_sum(time_left-1)

                if max_expected_geode >= max_open_geodes:
                    # the running time
                    next_time_left = time_left - 1

                    if next_time_left >= 0:
                        #  new resources
                        next_resources = resources + robots

                    if next_time_left >= 1:

                        # way 1. No robot is build. Collect only resources
                        wait_ore = (resources.ore < cost_robot_ore.ore)
                        wait_clay = (robots.clay > 0 and resources.clay < cost_robot_obs.clay)
                        wait_obsidian = (robots.obsidian > 0
                                         and resources.obsidian < cost_robot_geode.obsidian) and next_time_left >= 4
                        allow_time_wait = wait_ore or wait_clay or wait_obsidian
                        if allow_time_wait:
                            lifo.append((next_time_left, next_resources, robots))

                        # way 2. Build ore robot
                        if robots.ore <= max_robots_per_mn.ore:
                            if resources.ore >= cost_robot_ore.ore:
                                lifo.append((next_time_left,
                                             next_resources - cost_robot_ore,
                                             robots + Resource(ore=1)))

                        # way 3. Build clay robot
                        if robots.clay <= max_robots_per_mn.clay and next_time_left >= 5:
                            if resources.ore >= cost_robot_clay.ore:
                                lifo.append((next_time_left,
                                             next_resources - cost_robot_clay,
                                             robots + Resource(clay=1)))

                        # way 4. Build obsidian robot
                        if robots.obsidian <= max_robots_per_mn.obsidian and next_time_left >= 3:
                            if resources.clay >= cost_robot_obs.clay and resources.ore >= cost_robot_obs.ore:
                                lifo.append((next_time_left,
                                             next_resources - cost_robot_obs,
                                             robots + Resource(obsidian=1)))

                        # way 5. Build geode robot
                        if resources.obsidian >= cost_robot_geode.obsidian and resources.ore >= cost_robot_geode.ore:
                            lifo.append((next_time_left,
                                         next_resources - cost_robot_geode,
                                         robots + Resource(geode=1)))

                    if next_time_left == 0:
                        nb_search_paths += 1
                        max_open_geodes = max(next_resources.geode, max_open_geodes)

        return blueprint.id, max_open_geodes, nb_search_paths

    def compute_quality_level(self, time_left: int):
        sum_quality_level = 0

        # put ore robot in ready robots list
        for blueprint in self.blueprints:
            logger.info("blueprint id:%s start", blueprint.id)
            bp_id, max_open_geodes, nb_search_paths = self.depth_first_search(time_left, blueprint)
            sum_quality_level = sum_quality_level + (max_open_geodes * bp_id)
            print("     blueprint id:", bp_id, ", nb geodes:", max_open_geodes, ", nb search path:", nb_search_paths)

        return sum_quality_level

    def multiply_result_for_first_3_solutions(self, time_left: int):
        product = 1

        # put ore robot in ready robots list
        for blueprint in self.blueprints[0:3]:
            logger.info("blueprint id:%s start", blueprint.id)
            bp_id, max_open_geodes, nb_search_paths = self.depth_first_search(time_left, blueprint)
            product = product * max_open_geodes
            print("     blueprint id:", bp_id, ", nb geodes:", max_open_geodes, ", nb search path:", nb_search_paths)

        return product


class TestUtils:

    @staticmethod
    def check_result(test_name: str, expected_result: int, method_to_check, argv):
        current_result = method_to_check(argv)
        assert current_result == expected_result, test_name + ': ' + '(current_result:' + str(
            current_result) + ') != (expected_result:' + str(expected_result) + ')'
        return current_result


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING)

    INPUT_FILE_EXAMPLE = os.path.join(TEST_DATA_DIR, 'day19', 'example.txt')
    INPUT_FILE = os.path.join(TEST_DATA_DIR, 'day19', 'input.txt')

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 1: input file is ", input_file)
    start = time.time()
    puzzle = QualityLevelCalculator(input_file)
    quality_level_sum = TestUtils.check_result("part1", 33, puzzle.compute_quality_level, 24)
    print("part 1: execution time is ", time.time() - start, " s")
    print("part 1: the sum of quality level of all of the blueprints is ", quality_level_sum)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 1: input file is ", input_file)
    start = time.time()
    puzzle = QualityLevelCalculator(input_file)
    quality_level_sum = TestUtils.check_result("part1", 1144, puzzle.compute_quality_level, 24)
    print("part 1: execution time is ", time.time() - start, " s")
    print("part 1: the sum of quality level of all of the blueprints is ", quality_level_sum)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 2: input file is ", input_file)
    start = time.time()
    puzzle = QualityLevelCalculator(input_file)
    result = TestUtils.check_result("part1", 19980, puzzle.multiply_result_for_first_3_solutions, 32)
    print("part 2: execution time is ", time.time() - start, " s")
    print("part 2: if i multiply the result for first 3 solutions, i get ", result)
