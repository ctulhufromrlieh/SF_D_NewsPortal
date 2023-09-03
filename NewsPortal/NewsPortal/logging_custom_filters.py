import logging


class FilterLessWarning(logging.Filter):
    def filter(self, record):
        return record.levelno < logging.WARNING


class FilterLessError(logging.Filter):
    def filter(self, record):
        return record.levelno < logging.ERROR
