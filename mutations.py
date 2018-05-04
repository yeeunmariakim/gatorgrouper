import sys
import random
from typing import List
from genetic_algorithm import Student


def replace_random(grouping: List[List[Student]]):
    """Replace student at random index in each group with student at same index in previous group."""

    # find size of smallest group for random maximum
    minimum_group_size = sys.maxsize
    for group in grouping:
        if len(group) < minimum_group_size:
            minimum_group_size = len(group)

    print("min group size: " + str(minimum_group_size))

    replace_index = random.randint(0, minimum_group_size - 1)

    print("REPLACE INDEX: " + str(replace_index))
    last_replaced_student = None
    for index, current_group in enumerate(grouping):
        print(current_group[replace_index])
        temp = current_group[replace_index]
        current_group[replace_index] = last_replaced_student
        next_group = grouping[(index + 1) % (len(grouping) - 1)]
        last_replaced_student = next_group[replace_index]
        next_group[replace_index] = temp

def swap(grouping):
    # print("MUTATION")
    group_count = len(grouping)
    # print("TOTAL GROUPS: {}".format(group_count))
    # print("BEFORE: {}".format(grouping))
    first, second = random.sample(range(len(grouping)), 2)
    first_index = random.randrange(len(grouping[first]))
    second_index = random.randrange(len(grouping[second]))
    # print("swapping student {} in group {} with student {} in group {}".format(first_index, first, second_index, second))
    temp = grouping[second][second_index]
    grouping[second][second_index] = grouping[first][first_index]
    grouping[second][second_index] = temp
    # grouping[first][first_index], grouping[second][second_index] = grouping[second][second_index], grouping[first][first_index]
    # print("AFTER: {}".format(grouping))

    return grouping

def multi_swap(grouping):
    num_swaps = random.randrange(1, 6)
    for _ in range(num_swaps):
        grouping = swap(grouping)
    return grouping

def get():
    return [swap, multi_swap]
