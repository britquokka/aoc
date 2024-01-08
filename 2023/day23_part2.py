import collections
import logging
import os
import time
from TestUtils import TestUtils
from collections import defaultdict

logger = logging.getLogger(__name__)


class Graph:
    # Constructor
    def __init__(self, directed=True):
        # Graph representation - Adjacency list
        # We use a dictionary to implement an adjacency list
        self.adj_list = defaultdict(set)

    # Add edge to the graph
    def add_edge(self, node1, node2, weight=1, directed=False):
        self.adj_list[node1].add((node2, weight))

        if not directed:
            self.adj_list[node2].add((node1, weight))

    def log_graph(self):
        logger.info("nb node:%d", len(self.adj_list.keys()))
        logger.debug("adj_list:%s", self.adj_list)


class Puzzle:

    @staticmethod
    def to_grid(file):
        with open(file) as f:
            grid = f.read().splitlines()
        return grid

    def __init__(self, file, allow_climbing=False):
        self.grid = self.to_grid(file)
        self.start = (0, 1)
        self.target = (len(self.grid) - 1, len(self.grid[0]) - 2)
        self.allow_climbing = allow_climbing
        self.graph = self.build_graph_with_dfs()

    def build_neighbours(self, p):
        (y, x) = p
        neighbours = []
        all_neighbours = [(y - 1, x), (y, x + 1), (y + 1, x), (y, x - 1)]
        for r, c in all_neighbours:
            tile = self.grid[r][c]
            if tile != '#':
                neighbours.append((r, c))
        return neighbours

    def build_graph_with_dfs(self):
        graph = Graph()
        visited = set()
        lifo = collections.deque()
        # go to the south once to avoid to build outside neighbours
        visited.add(self.start)
        y, x = self.start
        first_p = (y + 1, x)
        visited.add(first_p)
        lifo.append((first_p, 0, first_p))
        graph.add_edge(self.start, first_p, weight=1)
        while lifo:
            p, depth, prev_node = lifo.pop()
            if p == self.target:
                graph.add_edge(prev_node, p, depth)
            else:
                neighbours = self.build_neighbours(p)
                depth += 1
                # path without intersection
                if len(neighbours) == 2:
                    visited.add(p)
                    for neighbour in neighbours:
                        if neighbour not in visited:
                            lifo.append((neighbour, depth, prev_node))
                # intersection found because we have more than 2 neighbours
                elif len(neighbours) > 2 and p != prev_node:
                    graph.add_edge(prev_node, p, depth)
                    depth = 0
                    prev_node = p
                    for neighbour in neighbours:
                        if neighbour not in visited:
                            lifo.append((neighbour, depth, prev_node))
        return graph

    def find_max_steps(self):
        self.graph.log_graph()
        return self.dfs(self.start, self.target)

    def dfs(self, start, target):
        max_path_len = 0
        visited = set()
        lifo = collections.deque()
        path_len = 0
        lifo.append((start, visited, path_len))
        while lifo:
            node, visited, path_len = lifo.pop()
            visited.add(node)
            if node == target:
                max_path_len = max(max_path_len, path_len)
            else:
                for (neighbour, weight) in self.graph.adj_list[node]:
                    if neighbour not in visited:
                        lifo.append((neighbour, visited.copy(), path_len+weight))
        return max_path_len


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    logging.basicConfig(level=logging.WARNING)
    TEST_DATA_DIR = os.path.join(os.getcwd(), 'data')
    INPUT_FILE_EXAMPLE = os.path.join(TEST_DATA_DIR, 'day23', 'example.txt')
    INPUT_FILE_EXAMPLE_PART2 = os.path.join(TEST_DATA_DIR, 'day23', 'example_part2.txt')
    INPUT_FILE = os.path.join(TEST_DATA_DIR, 'day23', 'input.txt')

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 2: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    max_steps = TestUtils.check_result_no_arg("part2", 154, puzzle.find_max_steps)
    print("part 2: execution time is ", time.time() - t0, " s")
    print("part 2: The number of the steps of the longest hike is ", max_steps)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 2: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    max_steps = TestUtils.check_result_no_arg("part2", 6230, puzzle.find_max_steps)
    print("part 2: execution time is ", time.time() - t0, " s")
    print("part 2: The number of the steps of the longest hike is ", max_steps)
