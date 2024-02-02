import heapq
import logging
import os
import time
from TestUtils import TestUtils
from enum import IntEnum
from dataclasses import dataclass
from collections import defaultdict

logger = logging.getLogger(__name__)


class Orientation(IntEnum):
    H = 0
    V = 1


@dataclass(frozen=True)
class NodeState:
    coord: tuple
    orientation: Orientation

    def __eq__(self, other):
        return (self.coord == other.coord) and (self.orientation == other.orientation)

    def __ne__(self, other):
        return not (self == other)

    def __lt__(self, other):
        return (self.coord < other.coord) and (self.orientation < other.orientation)

    def __gt__(self, other):
        return (self.coord > other.coord) and (self.orientation > other.orientation)

    def __le__(self, other):
        return (self < other) or (self == other)

    def __ge__(self, other):
        return (self > other) or (self == other)


class Puzzle:
    @staticmethod
    def to_city_blocks(file):
        with open(file) as f:
            cities = f.read().splitlines()
        city_blocks = []
        for row in cities:
            city_blocks.append([int(c) for c in row])
        return city_blocks

    def __init__(self, file, min_move=1, max_move=3):
        self.city_blocks = self.to_city_blocks(file)
        self.cache_dfs_results = {}
        self.start = (0, 0)
        self.target = (len(self.city_blocks) - 1, len(self.city_blocks[0]) - 1)
        self.r_max = len(self.city_blocks) - 1
        self.c_max = len(self.city_blocks[0]) - 1
        self.min_move = min_move
        self.max_move = max_move

    def dijkstra(self, start_coord: tuple):
        distances = defaultdict(lambda: float('inf'))
        parents = dict()
        visited = set()
        queue = []

        # 2 start nodes
        for orientation in Orientation:
            start = NodeState(start_coord, orientation)
            distances[start] = 0
            parents[start] = None
            queue.append((0, start))  # priority queue

        while queue:
            d, node = heapq.heappop(queue)
            visited.add(node)
            neighbours = self.build_neighbours(node)
            for neighbor, neigh_d in neighbours:
                if neighbor not in visited:
                    new_d = d + neigh_d
                    if new_d < distances[neighbor]:
                        distances[neighbor] = new_d
                        parents[neighbor] = node
                        heapq.heappush(queue, (new_d, neighbor))
        return distances, parents

    @staticmethod
    def build_path(parent_by_child, target):
        path = [target]
        flag_exit_loop = False
        child = target
        while not flag_exit_loop:
            parent = parent_by_child[child]
            if parent:
                path.append(parent)
                child = parent
            else:
                flag_exit_loop = True
        return path

    def find_least_heat_loss(self):
        heat_loss_by_dst, parents = self.dijkstra(self.start)

        # 2 result by cities
        d_h = heat_loss_by_dst[NodeState(self.target, Orientation.H)]
        d_v = heat_loss_by_dst[NodeState(self.target, Orientation.V)]
        min_heat_loss = min(d_h, d_v)

        logging.debug(self.build_path(parents, NodeState(self.target, Orientation.H)))
        logging.debug(self.build_path(parents, NodeState(self.target, Orientation.H)))
        logging.debug(heat_loss_by_dst)

        return min_heat_loss

    def in_cities(self, point):
        r, c = point
        return (r >= 0) and (r <= self.r_max) and (c >= 0) and (c <= self.c_max)

    def build_v_edges(self, coord, x_range: range, min_move):
        all_neighbours = []
        r, c = coord
        d_from_node = 0
        for x in x_range:
            new_coord = next_r, next_c = (r, c + x)
            if self.in_cities(new_coord):
                neighbor = NodeState(new_coord, Orientation.V)
                d_from_node += self.city_blocks[next_r][next_c]
                if abs(x) >= min_move:
                    all_neighbours.append((neighbor, d_from_node))
        return all_neighbours

    def build_h_edges(self, coord, y_range: range, min_move):
        all_neighbours = []
        r, c = coord
        d_from_node = 0
        for y in y_range:
            new_coord = next_r, next_c = (r+y, c)
            if self.in_cities(new_coord):
                neighbor = NodeState(new_coord, Orientation.H)
                d_from_node += self.city_blocks[next_r][next_c]
                if abs(y) >= min_move:
                    all_neighbours.append((neighbor, d_from_node))
        return all_neighbours

    def build_neighbours(self, node: NodeState):
        range_up = range(1, self.max_move + 1)
        range_down = range(-1, -(self.max_move+1), -1)
        if node.orientation == Orientation.H:
            all_neighbours = self.build_v_edges(node.coord, range_up, self.min_move)
            all_neighbours.extend(self.build_v_edges(node.coord, range_down, self.min_move))
        else:
            all_neighbours = self.build_h_edges(node.coord, range_up, self.min_move)
            all_neighbours.extend(self.build_h_edges(node.coord, range_down, self.min_move))

        return all_neighbours


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)
    TEST_DATA_DIR = os.path.join(os.getcwd(), 'data')
    INPUT_FILE_EXAMPLE = os.path.join(TEST_DATA_DIR, 'day17', 'example.txt')
    INPUT_FILE = os.path.join(TEST_DATA_DIR, 'day17', 'input.txt')

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 1: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    least_heat_loss = TestUtils.check_result_no_arg("part1", 102, puzzle.find_least_heat_loss)
    print("part 1: execution time is ", time.time() - t0, " s")
    print("part 1: The least heat loss is ", least_heat_loss)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 1: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file)
    least_heat_loss = TestUtils.check_result_no_arg("part1", 638, puzzle.find_least_heat_loss)
    print("part 1: execution time is ", time.time() - t0, " s")
    print("part 1: The least heat loss is ", least_heat_loss)

    print("-----------------")
    input_file = INPUT_FILE_EXAMPLE
    print("part 2: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file, min_move=4, max_move=10)
    least_heat_loss = TestUtils.check_result_no_arg("part2", 94, puzzle.find_least_heat_loss)
    print("part 2: execution time is ", time.time() - t0, " s")
    print("part 2: The least heat loss is ", least_heat_loss)

    print("-----------------")
    input_file = INPUT_FILE
    print("part 2: input file is ", input_file)
    t0 = time.time()
    puzzle = Puzzle(input_file, min_move=4, max_move=10)
    least_heat_loss = TestUtils.check_result_no_arg("part2", 748, puzzle.find_least_heat_loss)
    print("part 2: execution time is ", time.time() - t0, " s")
    print("part 2: The least heat loss is ", least_heat_loss)
