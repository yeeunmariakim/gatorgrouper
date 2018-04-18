""" GatorGrouper randomly assigns a list of students to groups """

import sys
import logging
import workbook
import arguments


if __name__ == '__main__':

    workbook.get()
    ARGUMENTS = arguments.parse(sys.argv[1:])

    GROUP_SIZE = ARGUMENTS.group_size
