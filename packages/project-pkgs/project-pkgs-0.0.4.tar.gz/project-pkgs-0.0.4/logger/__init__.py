'''
Date: 2020-12-22 10:43:43
LastEditors: Rustle Karl
LastEditTime: 2021-01-09 09:59:32
'''

import logging
import os
from logging import Formatter, Logger
from logging.handlers import RotatingFileHandler
from logger.formatter import CustomFormatter

from color import sbluef

default_config = {
    'level': logging.INFO,
    'mode': 'w',
    'encoding': 'utf-8',
    'maxBytes': (1 << 20) * 50,  # MB
    'backupCount': 30,
}

default_logfile_format = "%(asctime)s %(levelname)s " \
                         "%(pathname)s:%(lineno)s %(message)s"

default_stdout_format = "> {}\n> %(asctime)s %(color)s"\
    "[%(levelname)s] %(message)s\n".format(sbluef("%(pathname)s:%(lineno)s"))


def get_logger(ns: str, logfile: str = '', ext='.log',
               logdir='logs', stdout=True, **kwargs) -> Logger:

    logger = logging.getLogger(ns)
    logger.setLevel(logging.DEBUG)

    # 日志文件
    if logfile:
        if not os.path.exists(logdir):
            os.makedirs(logdir)

        if not logfile.endswith(ext):
            logfile += ext

        logfile = os.path.join(logdir, logfile)

        file_handler = RotatingFileHandler(
            logfile,
            mode=kwargs.get('mode', default_config['mode']),
            encoding=kwargs.get('encoding', default_config['encoding']),
            maxBytes=kwargs.get('maxBytes', default_config['maxBytes']),
            backupCount=kwargs.get(
                'backupCount', default_config['backupCount']),
        )

        file_handler.setLevel(kwargs.get('level', default_config['level']))

        # 为文件输出设定格式
        file_handler.setFormatter(Formatter(default_logfile_format))

        logger.addHandler(file_handler)

    # 控制台
    if stdout or not logfile:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)

        # 控制台输出设定格式
        console_handler.setFormatter(CustomFormatter(default_stdout_format))

        logger.addHandler(console_handler)

    return logger


if __name__ == "__main__":
    logger = get_logger('debug', 'debug')

    logger.debug("I don't know")
    logger.info("I don't know")
    logger.warning("I don't know")
    logger.error("I don't know")
