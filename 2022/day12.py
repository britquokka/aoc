import logging
import os

TEST_DATA_DIR = os.path.join(os.getcwd(), 'data')

logger = logging.getLogger(__name__)


class HillGraph:

    def build_id(self, i, j):
        return i * self.id_column_factor + j

    @staticmethod
    def conv(elevation):
        result = 'a' if elevation == 'S' else elevation
        result = 'z' if result == 'E' else result
        return result

    def is_inside_map(self, coord):
        i, j = coord
        flag_row = (0 <= i < self.nb_rows)
        flag_column = (0 <= j < self.nb_columns)
        return flag_column and flag_row

    def build_neighbours(self, i, j):
        neighbours = []
        neighbours_coord = [[i - 1, j], [i, j - 1], [i, j + 1], [i + 1, j]]
        neighbours_coord_filtered = filter(lambda pos: self.is_inside_map(pos), neighbours_coord)
        elevation = HillGraph.conv(self.squares[i][j])
        for coord in neighbours_coord_filtered:
            x, y = coord
            neighbour_elevation = HillGraph.conv(self.squares[x][y])
            if self.is_neighbour_predicate(neighbour_elevation, elevation):
                key = self.build_id(x, y)
                neighbours.append(key)
        return neighbours

    def __init__(self, squares, is_neighbour_predicate):
        self.graph = {}
        self.start_node = None
        self.end_node = None
        self.elevation_a_nodes = []
        self.nb_rows = len(squares)
        self.nb_columns = len(squares[0])
        self.id_column_factor = pow(10, len(str(self.nb_columns)))
        self.squares = squares
        self.is_neighbour_predicate = is_neighbour_predicate
        for i in range(0, self.nb_rows):
            for j in range(0, self.nb_columns):
                key = self.build_id(i, j)
                self.graph[key] = self.build_neighbours(i, j)
                if squares[i][j] == 'S':
                    self.start_node = key
                elif squares[i][j] == 'E':
                    self.end_node = key
                elif squares[i][j] == 'a':
                    self.elevation_a_nodes.append(key)


class Puzzle:

    @staticmethod
    def tolist(file):
        result = []
        with open(file) as f:
            for line in f:
                row = list(line.strip())
                result.append(row)
        return result

    def __init__(self, file):
        self.squares = self.tolist(file)

    @staticmethod
    def bfs(graph, parent_by_node, start_node, end_nodes: list):
        visited = []
        queue = []
        visited.append(start_node)
        queue.append(start_node)
        while queue:
            current = queue.pop(0)
            logger.debug("current %s", current)
            logger.debug("neighbour %s", graph[current])
            if current in end_nodes:
                return current
            for neighbour in graph[current]:
                if neighbour not in visited:
                    parent_by_node[neighbour] = current
                    visited.append(neighbour)
                    queue.append(neighbour)

    @staticmethod
    def find_steps( graph, start_node, end_nodes):
        parent_by_node = {}
        end_node = Puzzle.bfs(graph, parent_by_node, start_node, end_nodes)
        steps = []
        flag_exit_loop = False
        current_node = end_node
        steps.append(current_node)
        while not flag_exit_loop:
            parent = parent_by_node.get(current_node)
            if parent is not None:
                steps.append(parent)
                current_node = parent
            else:
                flag_exit_loop = True
        return steps

    @staticmethod
    def is_neighbour_asc(neighbour_elevation, current_elevation):
        return ord(neighbour_elevation) - ord(current_elevation) <= 1

    @staticmethod
    def is_neighbour_dsc(neighbour_elevation, current_elevation):
        return ord(neighbour_elevation) - ord(current_elevation) >= -1

    def compute_nb_steps(self):
        hill_graph = HillGraph(self.squares, Puzzle.is_neighbour_asc)
        logger.info("start_node: %s", hill_graph.start_node)
        logger.info("end_node: %s", hill_graph.end_node)
        logger.debug("graph %s", hill_graph.graph)
        end_nodes = [hill_graph.end_node]
        steps = self.find_steps(hill_graph.graph, hill_graph.start_node, end_nodes)
        logger.info(steps)
        return len(steps) - 1

    def compute_nb_fewest_steps_from_any_a_elevation(self):
        hill_graph = HillGraph(self.squares, Puzzle.is_neighbour_dsc)
        logger.info("start_node: %s", hill_graph.start_node)
        logger.info("end_node: %s", hill_graph.end_node)
        logger.debug("graph %s", hill_graph.graph)

        end_nodes = [hill_graph.start_node]
        end_nodes.extend(hill_graph.elevation_a_nodes)
        steps = self.find_steps(hill_graph.graph, hill_graph.end_node, end_nodes)
        logger.info(steps)
        return len(steps) - 1


class TestUtils:

    @staticmethod
    def check_result(test_name: str, expected_result: int, method_to_check):
        current_result = method_to_check()
        assert current_result == expected_result, test_name + ': ' + '(current_result:' + str(
            current_result) + ') != (expected_result:' + str(expected_result) + ')'
        return current_result


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING)

    INPUT_FILE_EXAMPLE = os.path.join(TEST_DATA_DIR, 'day12', 'example.txt')
    INPUT_FILE = os.path.join(TEST_DATA_DIR, 'day12', 'input.txt')

    # part 1
    puzzle_test = Puzzle(INPUT_FILE_EXAMPLE)
    TestUtils.check_result("part1", 31, puzzle_test.compute_nb_steps)

    puzzle = Puzzle(INPUT_FILE)
    nb_steps = puzzle.compute_nb_steps()
    print("part 1: nb fewest steps from 'S' to 'E' is ", nb_steps)

    # part 2
    TestUtils.check_result("part2", 29, puzzle_test.compute_nb_fewest_steps_from_any_a_elevation)

    nb_fewest_steps_from_any_a_elevation = puzzle.compute_nb_fewest_steps_from_any_a_elevation()
    print("part 2: nb fewest steps from any 'a' elevation to 'E' is ", nb_fewest_steps_from_any_a_elevation)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
