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
from genetic_algorithm import create, calculate_fitness, evolve

if __name__ == '__main__':

    ARGUMENTS = arguments.parse(sys.argv[1:])
    GROUP_SIZE = ARGUMENTS.group_size

    workbook.get(GROUP_SIZE)

    evolve(60, 0.33, 0.16, 0.18, 0.66, mutations.get())
