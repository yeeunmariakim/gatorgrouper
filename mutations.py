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

    replace_index = random.randint(0, minimum_group_size)

    last_replaced_student = None
    for index, current_group in grouping:
        temp = current_group[replace_index]
        current_group[replace_index] = last_replaced_student
        next_group = grouping[(index + 1) % (len(grouping) - 1)]
        last_replaced_student = next_group[replace_index]
        next_group[replace_index] = temp


def get():
    return [replace_random]
