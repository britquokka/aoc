import logging
import os

TEST_DATA_DIR = os.path.join(os.getcwd(), 'data')


logger = logging.getLogger(__name__)


class Node:

    def __init__(self, a_name: str, a_size: int, a_parent):
        self.name = a_name
        self.size = a_size
        self.parent = a_parent

    def get_size(self):
        return self.size

    def compute_size(self):
        return self.get_size()


class Dir(Node):

    def __init__(self, a_name: str, a_size: int, a_parent):
        Node.__init__(self, a_name, a_size, a_parent)
        self.nodes: list = []
        self.nodes_by_name: dict = {}

    def compute_size(self):
        self.size = 0
        for node in self.nodes:
            self.size = node.compute_size() + self.size
        return self.size

    def get_node_by_name(self, a_name: str):
        return self.nodes_by_name.get(a_name)

    def add_node(self, a_node: Node):
        self.nodes_by_name[a_node.name] = a_node
        self.nodes.append(a_node)

    def add_file(self, a_name: str, a_size: int):
        file = self.get_node_by_name(a_name)
        if file is None:
            file = File(a_name, a_size, self)
            logger.debug("add_file %s in %s", file.name, file.parent.name)
            self.add_node(file)

    def add_dir(self, a_name: str):
        directory = self.get_node_by_name(a_name)
        if directory is None:
            directory = Dir(a_name, 0, self)
            logger.debug("add_dir %s in %s", directory.name, directory.parent.name)
            self.add_node(directory)

    def find_dirs(self):
        dir_list = [self]
        for node in self.nodes:
            if isinstance(node, Dir):
                dir_list.extend(node.find_dirs())
        return dir_list


class File(Node):
    pass


class NodeBuilder:

    def __init__(self):
        self.root_dir = None
        self.current_dir = None

    def create(self, a_console_output_list):
        self.root_dir = Dir('/', 0, None)
        self.root_dir = self._create(self.root_dir, a_console_output_list)
        return self.root_dir

    def process_cmd(self, cmd):
        if cmd[1] == 'cd':
            next_dir_name = cmd[2]
            if cmd[2] == '/':
                next_current_dir = self.root_dir
            elif cmd[2] == '..':
                next_current_dir = self.current_dir.parent
            else:
                next_current_dir = self.current_dir.get_node_by_name(next_dir_name)
            self.current_dir = next_current_dir

    def process_result(self, result):
        if result[0] == 'dir':
            # create or update dir
            dir_name = result[1]
            self.current_dir.add_dir(dir_name)
        else:
            file_size = int(result[0])
            file_name = result[1]
            self.current_dir.add_file(file_name, file_size)

    def _create(self, a_current_dir, a_console_output_list):
        current_root_dir = a_current_dir
        self.current_dir = a_current_dir
        for console_output in a_console_output_list:
            logger.debug("current cmd : %s", console_output)
            if console_output[0] == '$':
                self.process_cmd(console_output)
            else:
                self.process_result(console_output)

        return current_root_dir


class Puzzle:

    @staticmethod
    def tolist2d(file):
        result = []
        with open(file) as f:
            for line in f:
                row = line.strip().split(' ')
                result.append(row)
        return result

    def __init__(self, file):
        self.console_output_lines = self.tolist2d(file)
        builder = NodeBuilder()
        self.root_node = builder.create(self.console_output_lines)
        self.root_node.compute_size()

    def sum_sizes_of_at_most_100000_directory(self):
        dirs = self.root_node.find_dirs()
        dir_sizes = list(map(lambda a_dir: a_dir.size, dirs))
        result_list = list(filter(lambda a_size: a_size < 100000, dir_sizes))
        logger.debug(result_list)
        return sum(result_list)

    def get_size_of_directory_to_delete(self):
        dirs = self.root_node.find_dirs()
        dir_sizes = list(map(lambda a_dir: a_dir.size, dirs))
        used_space = self.root_node.size
        unused_space = 70000000 - used_space
        needed_space = 30000000
        # candidates_list = [size for size in dir_sizes if unused_space + size >= needed_space]
        candidates_list = list(filter(lambda size: unused_space + size >= needed_space, dir_sizes))
        return min(candidates_list)


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

    INPUT_FILE_EXAMPLE = os.path.join(TEST_DATA_DIR, 'day7', 'example.txt')
    INPUT_FILE = os.path.join(TEST_DATA_DIR, 'day7', 'input.txt')

    # part 1
    puzzle_test = Puzzle(INPUT_FILE_EXAMPLE)
    TestUtils.check_result("part1", 95437, puzzle_test.sum_sizes_of_at_most_100000_directory)

    puzzle = Puzzle(INPUT_FILE)
    sum_sizes = puzzle.sum_sizes_of_at_most_100000_directory()
    print("part 1: sum of the total sizes of the (at most 100000) directories is ", sum_sizes)

    # part 2
    TestUtils.check_result("part2", 24933642, puzzle_test.get_size_of_directory_to_delete)

    size_of_dir_to_delete = puzzle.get_size_of_directory_to_delete()
    print("part 2: size of directory to delete is ", size_of_dir_to_delete)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
