import logging
import os
import time
from collections import defaultdict
from TestUtils import TestUtils
import collections

logger = logging.getLogger(__name__)


class Puzzle:

    @staticmethod
    def to_graph(file):
        graph = defaultdict(set)
        with open(file) as f:
            for line in f:
                node, neighbours = line.strip().split(':')
                graph[node] = neighbours.strip().split()
        return graph

    def __init__(self, file):
        self.graph = Puzzle.to_graph(file)
        self.cache_dfs_results = {}

    def find_nb_paths(self):
        logger.debug(self.graph)
        return self.dfs("you", "out")

    def dfs(self, start, target):
        nb_paths = 0
        visited = set()
        lifo = collections.deque()
        path_len = 0
        lifo.append((start, visited, path_len))
        while lifo:
            node, visited, path_len = lifo.pop()
            visited.add(node)
            if node == target:
                nb_paths += 1
            else:
                for neighbour in self.graph[node]:
                    if neighbour not in visited:
                        lifo.append((neighbour, visited.copy(), path_len+1))
        return nb_paths

    def dfs_p2(self, start, target):
        nb_paths = nb_paths_dac_fft = 0
        visited = set()
        lifo = collections.deque()
        path_len = 0
        lifo.append((start, visited, path_len))
        while lifo:
            node, visited, path_len = lifo.pop()
            visited.add(node)
            if node == target:
                nb_paths += 1
                if "dac" in visited:
                    if "fft" in visited:
                        nb_paths_dac_fft += 1
            else:
                for neighbour in self.graph[node]:
                    if neighbour not in visited:
                        lifo.append((neighbour, visited.copy(), path_len + 1))
        return nb_paths, nb_paths_dac_fft

    def dfs_recursive(self, node, target, visited):
        nb_paths = nb_paths_dac_fft = 0

        if node in self.cache_dfs_results.keys():
            logger.warning("cache_dfs_results[%s] = %s",  node,self.cache_dfs_results[node])
            return self.cache_dfs_results[node]

        visited.append(node)
        if node == target:
            logger.warning(visited)
            nb_paths += 1
            return nb_paths, 0

        for neighbour in self.graph[node]:
            nb_paths_tmp, nb_paths_dac_fft_tmp = self.dfs_recursive(neighbour, target, visited.copy())
            logger.warning(visited)
            nb_paths += nb_paths_tmp
            nb_paths_dac_fft += nb_paths_dac_fft_tmp

        if "dac" in visited:
            if "fft" in visited:
                nb_paths_dac_fft = nb_paths

        self.cache_dfs_results[node] = (nb_paths, nb_paths_dac_fft)
        logger.warning("set cache_dfs_results[%s] = %s", node, self.cache_dfs_results[node])
        return nb_paths, nb_paths_dac_fft

    def find_nb_paths_p2(self):
        logger.debug(self.graph)
        visited = []
        nb_paths, nb_paths_dac_fft = self.dfs_recursive("svr", "out",visited)
        logger.warning("nb_paths = %d, nb_paths with fft and dac = %d", nb_paths, nb_paths_dac_fft)
        return nb_paths_dac_fft


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    TEST_DATA_DIR = os.path.join(os.getcwd(), 'data')
    INPUT_FILE_EXAMPLE = os.path.join(TEST_DATA_DIR, 'day11', 'example.txt')
    INPUT_FILE = os.path.join(TEST_DATA_DIR, 'day11', 'input.txt')
    INPUT_FILE_EXAMPLE_P2 = os.path.join(TEST_DATA_DIR, 'day11', 'example_p2.txt')

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 1: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result_no_arg(test_name="part1", expected_result=5,
                                           method_to_check=puzzle.find_nb_paths)
    print("part 1: execution time is ", time.time() - t0, " s")
    print(f"part 1: There are {result} different path lead from you to out")

    print("-----------------")
    input_file = INPUT_FILE
    print("part 1: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result_no_arg(test_name="part1", expected_result=590,
                                           method_to_check=puzzle.find_nb_paths)
    print("part 1: execution time is ", time.time() - t0, " s")
    print(f"part 1: There are {result} different paths lead from you to out")

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE_P2
    print("part 2: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result_no_arg(test_name="part2", expected_result=2,
                                            method_to_check=puzzle.find_nb_paths_p2)
    print("part 2: execution time is ", time.time() - t0, " s")
    print(f"part 2: There are {result} different paths lead from svr to out and visit both dac and fft")

    exit(0)
    print("-----------------")
    input_file = INPUT_FILE
    print("part 2: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    result = TestUtils.check_result_no_arg(test_name="part2", expected_result=2,
                                           method_to_check=puzzle.find_nb_paths_p2)
    print("part 2: execution time is ", time.time() - t0, " s")
    print(f"part 2: There are {result} different paths lead from svr to out and visit both dac and fft")
