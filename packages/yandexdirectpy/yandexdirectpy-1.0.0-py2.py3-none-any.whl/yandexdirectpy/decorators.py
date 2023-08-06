import functools
from yandexdirect.loggers import logger


def log_func(fn):
    @functools.wraps(fn)
    def inner(**kwargs):
        logger.info(msg='')
        return fn(**kwargs)
    return inner
