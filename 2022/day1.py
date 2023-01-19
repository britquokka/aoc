import os

TEST_DATA_DIR = os.path.join(os.getcwd(), 'data')


def tolist2d(file):
    result = []
    row = []
    with open(file) as f:
        for line in f:
            item = line.strip()
            if item == '':
                result.append(row)
                row = []
            else:
                row.append(int(item))
    return result


def compute_sum_calories_for_each_elf(list2d):
    result = []
    for items_per_elf in list2d:
        calories_per_elf = sum(items_per_elf)
        result.append(calories_per_elf)
    return result


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    INPUT_FILE_EXAMPLE = os.path.join(TEST_DATA_DIR, 'day1', 'example.txt')
    INPUT_FILE = os.path.join(TEST_DATA_DIR, 'day1', 'input.txt')
    list_cal_for_each_elf = tolist2d(INPUT_FILE)
    sum_calories_for_each_elf = compute_sum_calories_for_each_elf(list_cal_for_each_elf)
    sum_calories_for_each_elf.sort(reverse=True)
    max_calories_part1 = sum_calories_for_each_elf[0]
    nb_first_elves = 3
    calories_part2 = sum(sum_calories_for_each_elf[0:nb_first_elves])

    print("part 1 result is", max_calories_part1)
    print("part 2 result is", calories_part2)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
