""" GatorGrouper randomly assigns a list of students to groups """

import sys
import logging
import pandas as pd
from colors import bold
import math

import config
import workbook
import arguments
import mutations
from genetic_algorithm import create

if __name__ == '__main__':

    ARGUMENTS = arguments.parse(sys.argv[1:])
    GROUP_SIZE = ARGUMENTS.group_size

    workbook.get(GROUP_SIZE)

    GROUPING = create()

    for index, group in enumerate(GROUPING):
        print("Group " + str(index) + "\n")
        for student in group:
            print("\t" + student.email + "\n")

    # evolve(30, 0.05, 0.8, calculate_fitness, mutations.get(), create)
