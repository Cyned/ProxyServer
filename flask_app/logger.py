import logging

from os.path import join as path_join

from logging.handlers import TimedRotatingFileHandler


def create_logger(app_dir):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('[%(asctime)s - %(levelname)s %(module)s %(funcName)s] - %(message)s')
    fh = TimedRotatingFileHandler(path_join(app_dir, 'logs/MAIN.log'), when='midnight', encoding='utf8')
    fh.suffix = '%Y_%m_%d.log'
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    return logger
