import logging

class StationBookLogger():
    def __init__(self, logger_name):
        self.logger = logging.getLogger(logger_name)

    def log_info(self, text):
        self.logger.info(text)

    def log_warning(self, text):
        self.logger.warning(text)

    def log_exception(self, text):
        self.logger.exception(text)