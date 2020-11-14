
import logging

logging.basicConfig(level=logging.DEBUG,
                    format=' %(asctime)6s *%(levelname).1s* %(message)',
                    datefmt='%H%M%S')

if __name__ == '__main__':
    logging.DEBUG('config read')