import sys
from utils import string_to_operator
import logging
from common import configure_logging

# Настройка логирования
configure_logging()
logger = logging.getLogger(__name__)

def calc(args):
    logger.info("Arguments: %s", args)

    num_1 = args[0]
    operator = args[1]
    num_2 = args[2]

    try:
        num_1 = float(num_1)
    except ValueError as e:
        logger.error("Error while converting number 1: %s", e)

    try:
        num_2 = float(num_2)
    except ValueError as e:
        logger.error("Error while converting number 2: %s", e)

    operator_func = string_to_operator(operator)

    result = operator_func(num_1, num_2)

    logger.info("Result: %s", result)
    logger.info("%s %s %s = %s", num_1, operator, num_2, result)


if __name__ == '__main__':
    # calc(sys.argv[1:])
    calc(['2', '+', '3'])