import logging
import logstash
import sys
import os


class LogService:
    def __init__(self):
        self.logger = logging.getLogger(os.getenv('LOGSTASH_NAME'))
        self.logger.setLevel(int(os.getenv('LOGSTASH_LEVEL')))

        use_logtash = os.getenv('USE_LOGSTASH')

        if use_logtash == 'True':
            if (self.logger.hasHandlers()):
                self.logger.handlers.clear()
            
            self.logger.addHandler(logstash.TCPLogstashHandler(os.getenv('LOGSTASH_HOST'), os.getenv('LOGSTASH_PORT'), version=1))

    def i(self, msg, *args):
        self.logger.info(msg)

    def w(self, msg, *args):
        self.logger.warning(msg)

    def e(self, msg, *args):
        self.logger.error(msg)

    def d(self, msg, *args):
        self.logger.debug(msg)

log_service = LogService()