import logging
from pympler import tracker


if __name__ == '__main__':
    tr = tracker.SummaryTracker()
    # logging.basicConfig(level=logging.INFO, format='%(asctime)6s *%(levelname).1s* %(message)s', datefmt='%H%M%S')
    # tr.print_diff()
    logger = logging.getLogger('test logger')
    logger.setLevel(logging.DEBUG)

    logger_handler = logging.StreamHandler()
    logger.addHandler(logger_handler)

    logger_formater = logging.Formatter('%(asctime)6s *%(levelname).1s* %(message)s', datefmt='%H%M%S')
    logger_handler.setFormatter(logger_formater)

    logger.info('before exception')
    try:
        1/0
    except ZeroDivisionError as e:
        logger.exception('arbitrarily causing ZeroDivisionError for logging.exception trial.')

    logger.info('after exception')
    tr.print_diff()
