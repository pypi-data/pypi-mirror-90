'''
Date: 2020-12-22 10:41:08
LastEditors: Rustle Karl
LastEditTime: 2020-12-22 14:05:49
'''
from logging import Formatter, LogRecord

from color import Color, set_color, unset_color

default_color_config = {
    'DEBUG': Color.Cyan,
    'INFO': Color.Green,
    'WARNING': Color.Yellow,
    'ERROR': Color.Red,
}


class CustomFormatter(Formatter):

    def __init__(self, fmt, datefmt=None, config=default_color_config) -> None:
        super(CustomFormatter, self).__init__(fmt, datefmt)
        self.config = config

    def parse_color(self, level):
        return set_color(self.config.get(level, Color.Green))

    def format(self, record: LogRecord) -> str:
        record.color = self.parse_color(record.levelname)
        return unset_color(super(CustomFormatter, self).format(record))
