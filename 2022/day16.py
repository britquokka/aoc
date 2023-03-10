import logging
import os
import queue
import threading
import operator

import time
from itertools import combinations
from operator import itemgetter


TEST_DATA_DIR = os.path.join(os.getcwd(), 'data')

logger = logging.getLogger(__name__)


class Action:
    def __init__(self, valve_name: str, time_left: int):
        self.valve_name = valve_name
        self.time_left = time_left


class Valve:
    def __init__(self,  name: str, neighbours: list, rate: int):
        self.name = name
        self.neighbours = neighbours
        self.rate = rate

    @staticmethod
    def to_string(valves: list):
        return list(map(lambda valve: valve.name, valves))


class Volcano:
    def __init__(self, valves: list):
        self.neighbours_by_valve_name = {}
        self.graph = {}
        for valve in valves:
            self.neighbours_by_valve_name[valve.name] = valve.neighbours
            self.graph[valve.name] = valve

    def get_valve_by_name(self, name: str):
        return self.graph.get(name)


class DistanceMatrix:

    def __init__(self, graph: dict):
        self.distances = DistanceMatrix.build_distance_matrix(graph)

    @staticmethod
    def build_distance_matrix(graph: dict):
        distances = {}
        nodes = list(graph.keys())
        for current_node in nodes:
            distance_others = {}
            DistanceMatrix.bfs_distances(graph, current_node, distance_others)
            distances[current_node] = distance_others
        return distances

    @staticmethod
    def bfs_distances(graph, start_node, distance_others):
        visited = []
        fifo = []
        depth = []
        visited.append(start_node)
        depth.append(0)
        fifo.append(start_node)
        while fifo:
            current = fifo.pop(0)
            current_depth = depth.pop(0)
            for neighbour in graph[current]:
                if neighbour not in visited:
                    next_depth = current_depth + 1
                    distance_others[neighbour] = next_depth
                    visited.append(neighbour)
                    fifo.append(neighbour)
                    depth.append(next_depth)


class PressureCalculator:

    @staticmethod
    def to_valves(file):
        valves = []
        with open(file) as f:
            for line in f:
                row = list(line.strip().split(' '))
                name = row[1]
                rate = int(row[4].strip('rate=;'))
                neighbours = []
                for i in range(9, len(row)):
                    neighbours.append(row[i].strip(','))
                valves.append(Valve(name, neighbours, rate))

        return valves

    def __init__(self, file):
        valves = self.to_valves(file)
        self.volcano = Volcano(valves)
        self.distance_matrix = DistanceMatrix(self.volcano.neighbours_by_valve_name)
        self.filtered_valves = list(filter(lambda valve: valve.rate != 0, valves))
        self.valves_with_pressure = list(map(lambda valve: valve.name, self.filtered_valves))
        self.q = queue.Queue(100)
        self.max_pressure = 0
        logger.debug("distance_matrix: %s", self.distance_matrix)
        logger.debug("valves_with_pressure %s", self.valves_with_pressure)

    def depth_first_search(self,
                           current_valve: str,
                           prev_actions: list,
                           prev_time_left: int,
                           valves_to_visit: list):
        actions = []
        next_search_flag = False

        # logger.debug("current valve: %s , next valves: %s",
        #              current_valve.name, list(map(lambda a: a.name, valves_to_visit)))

        if prev_time_left < 2 or len(valves_to_visit) == 0:
            next_search_flag = False
        else:
            for valve in valves_to_visit:
                distance = self.distance_matrix.distances[current_valve][valve]
                time_left = prev_time_left - distance - 1
                if time_left >= 1:
                    actions = prev_actions.copy()
                    action = Action(valve, time_left)
                    actions.append(action)
                    next_valves_to_visit = valves_to_visit.copy()
                    next_valves_to_visit.remove(valve)
                    self.depth_first_search(valve, actions, time_left, next_valves_to_visit)
                    next_search_flag = True

        if next_search_flag is False:
            actions = actions if len(actions) > 0 else prev_actions.copy()
            result = (False, actions)
            # logger.debug("path %s", list(map(lambda a: a.valve_name, actions)))
            self.q.put(result)

    @staticmethod
    def compute_pressure(actions: list, graph):
        pressure = 0
        for action in actions:
            valve = graph.get_valve_by_name(action.valve_name)
            pressure = pressure + action.time_left * valve.rate
        return pressure

    def compute_most_pressure(self, time_left: int):
        # Turn-on the worker thread.
        task = threading.Thread(target=self.pressure_calculator_worker, daemon=True)
        task.start()

        origin = 'AA'
        self.depth_first_search(origin, [], time_left, self.valves_with_pressure)

        # last msg
        result = (True, [])
        self.q.put(result)

        # wait end task
        task.join()
        logger.info("most pressure: %s", self.max_pressure)
        return self.max_pressure

    def pressure_calculator_worker(self):
        nb_path = 0
        flag_exit_loop = False
        while not flag_exit_loop:
            is_last, actions = self.q.get()
            nb_path = nb_path + 1
            # logger.debug("compute max pressure for %s %s", is_last, list(map(lambda a: a.valve_name, actions)))
            if not is_last:
                pressure = self.compute_pressure(actions, self.volcano)
                self.max_pressure = max(self.max_pressure, pressure)
            self.q.task_done()
            flag_exit_loop = is_last
        print("part 1: nb paths to inspect is ", nb_path - 1)
        return


class PressureCalculatorWithElephant(PressureCalculator):

    def pressure_calculator_worker(self):
        max_pressure_per_combination = {}
        flag_exit_loop = False
        nb_path = 0
        while not flag_exit_loop:
            is_last, actions = self.q.get()
            nb_path = nb_path + 1
            # logger.debug("compute max pressure for %s %s", is_last, list(map(lambda a: a.valve_name, actions)))
            if not is_last:
                self.compute_pressure_step_by_step(actions, max_pressure_per_combination)
            self.q.task_done()
            flag_exit_loop = is_last
        print("part 2: nb paths to inspect is ", nb_path - 1)
        # we want 2 path with no common valves, one set for me and one set for the elephant
        # we search in the best path first and we will stop search when we can't increase pressure
        best_paths_first = sorted(max_pressure_per_combination.items(), key=itemgetter(1), reverse=True)

        for my_path, my_pressure in best_paths_first:
            for elephant_path, elephant_pressure in best_paths_first:
                if my_path != elephant_path:
                    intersect = my_path & elephant_path
                    if len(intersect) == 0:
                        pressure = my_pressure + elephant_pressure
                        if pressure > self.max_pressure:
                            self.max_pressure = pressure
                        else:
                            # elephant can't do better
                            break

        return

    def compute_pressure_step_by_step(self, actions, max_pressure_per_combination):
        # if  actions path is [JJ,HH,EE,DD] then we compute pressure for
        # [JJ]
        # [JJ,HH]
        # [JJ,HH,EE]
        # [JJ,HH,EE,DD]
        # and we put result in a map .
        pressure = 0
        step_by_step = []
        for action in actions:
            step_by_step.append(action)
            valve = self.volcano.get_valve_by_name(action.valve_name)
            pressure = pressure + action.time_left * valve.rate
            valves_combination_key = frozenset(map(lambda v: v.valve_name, step_by_step))
            prev_max_pressure = max_pressure_per_combination.get(valves_combination_key, 0)
            max_pressure_per_combination[valves_combination_key] = max(prev_max_pressure, pressure)
        return pressure


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

    INPUT_FILE_EXAMPLE = os.path.join(TEST_DATA_DIR, 'day16', 'example.txt')
    INPUT_FILE = os.path.join(TEST_DATA_DIR, 'day16', 'input.txt')

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 1: input file is ", input_file)
    start = time.time()
    puzzle = PressureCalculator(input_file)
    most_pressure = TestUtils.check_result("part1", 1651, puzzle.compute_most_pressure, 30)
    print("part 1: execution time is ", time.time() - start, " s")
    print("part 1: the most pressure, I can release, is ", most_pressure)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 1: input file is ", input_file)
    start = time.time()
    puzzle = PressureCalculator(input_file)
    most_pressure = TestUtils.check_result("part1", 1584, puzzle.compute_most_pressure, 30)
    print("part 1: execution time is ", time.time() - start, " s")
    print("part 1: the most pressure, I can release, is ", most_pressure)

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 2: input file is ", input_file)
    start = time.time()
    puzzle = PressureCalculatorWithElephant(input_file)
    most_pressure = TestUtils.check_result("part2", 1707, puzzle.compute_most_pressure, 26)
    print("part 2: execution time is ", time.time() - start, " s")
    print("part 2: the most pressure, I can release with elephant, is ", most_pressure)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 2: input file is ", input_file)
    start = time.time()
    puzzle = PressureCalculatorWithElephant(input_file)
    most_pressure = TestUtils.check_result("part2", 2052, puzzle.compute_most_pressure, 26)
    print("part 2: execution time is ", time.time() - start, " s")
    print("part 2: the most pressure, I can release with elephant in 26 mn , is ", most_pressure)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 2: input file is ", input_file)
    start = time.time()
    puzzle = PressureCalculatorWithElephant(input_file)
    most_pressure = TestUtils.check_result("part2", 2761, puzzle.compute_most_pressure, 30)
    print("part 2: execution time is ", time.time() - start, " s")
    print("part 2: the most pressure, I can release with elephant in 30 mn , is ", most_pressure)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
