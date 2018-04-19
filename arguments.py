"""Parse command-line arguments."""

import argparse
import logging
import config


def parse(args):
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument(
        "-d",
        "--debug",
        help="Display diagnostic information",
        action="store_const",
        dest="logging_level",
        const=logging.DEBUG,
        default=logging.ERROR)

    parser.add_argument(
        "-v", "--verbose",
        help="Display monitoring information",
        action="store_const", dest="logging_level", const=logging.INFO
    )

    parser.add_argument(
        "--group-size",
        help="Number of students per group",
        type=int,
        default=config.DEFAULT_GROUP_SIZE,
        required=False)

    arguments = parser.parse_args(args)

    logging.basicConfig(format="%(levelname)s:%(pathname)s: %(message)s",
                        level=arguments.logging_level)

    return arguments
