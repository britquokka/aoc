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

    def __init__(self, file):
        self.city_blocks = self.to_city_blocks(file)
        self.cache_dfs_results = {}
        self.start = (0, 0)
        self.target = (len(self.city_blocks) - 1, len(self.city_blocks[0]) - 1)
        self.r_max = len(self.city_blocks) - 1
        self.c_max = len(self.city_blocks[0]) - 1

    def dijkstra(self, start: tuple):
        distances = defaultdict(lambda: float('inf'))
        parents = dict()
        visited = set()
        start_h = NodeState(start, Orientation.H)
        start_v = NodeState(start, Orientation.V)
        distances[start_h] = 0
        distances[start_v] = 0
        parents[start_h] = None
        parents[start_v] = None
        queue = [(0, start_h), (0, start_v)]  # priority queue
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

    def build_v_edges(self, coord, x_range: range):
        all_neighbours = []
        r, c = coord
        d_from_node = 0
        for x in x_range:
            new_coord = next_r, next_c = (r, c + x)
            if self.in_cities(new_coord):
                neighbor = NodeState(new_coord, Orientation.V)
                d_from_node += self.city_blocks[next_r][next_c]
                all_neighbours.append((neighbor, d_from_node))
        return all_neighbours

    def build_h_edges(self, coord, y_range: range):
        all_neighbours = []
        r, c = coord
        d_from_node = 0
        for y in y_range:
            new_coord = next_r, next_c = (r+y, c)
            if self.in_cities(new_coord):
                neighbor = NodeState(new_coord, Orientation.H)
                d_from_node += self.city_blocks[next_r][next_c]
                all_neighbours.append((neighbor, d_from_node))
        return all_neighbours

    def build_neighbours(self, node: NodeState):

        if node.orientation == Orientation.H:
            all_neighbours = self.build_v_edges(node.coord, range(1, 4))
            all_neighbours.extend(self.build_v_edges(node.coord, range(-1, -4, -1)))
        else:
            all_neighbours = self.build_h_edges(node.coord, range(1, 4))
            all_neighbours.extend(self.build_h_edges(node.coord, range(-1, -4, -1)))

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
