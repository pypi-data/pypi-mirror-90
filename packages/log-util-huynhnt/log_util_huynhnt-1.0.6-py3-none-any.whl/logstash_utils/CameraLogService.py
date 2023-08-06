import logging
import logstash
import sys
import os


class CameraLogService:
    def __init__(self, camera_id):
        self.logger = logging.getLogger(os.getenv('LOGSTASH_NAME'))

        use_logtash = os.getenv('USE_LOGSTASH')

        if use_logtash == 'True':
            if self.logger.hasHandlers():
                self.logger.handlers.clear()

            self.logger.setLevel(logging.INFO)
            self.logger.addHandler(logstash.TCPLogstashHandler(os.getenv('LOGSTASH_HOST'), os.getenv('LOGSTASH_PORT'), version=1))
            self.camera_id = camera_id
        self.extra = {
            'camera_id': self.camera_id,
        }

    def i(self, msg, *args):
        self.logger.info(msg, extra=self.extra)

    def w(self, msg, *args):
        self.logger.warning(msg, extra=self.extra)

    def e(self, msg, *args):
        self.logger.error(msg, extra=self.extra)

    def d(self, msg, *args):
        self.logger.debug(msg, extra=self.extra)


class CameraLogServiceManager:
    __instance = None

    @staticmethod 
    def getInstance(camera_id = 'None') -> CameraLogService:
        if CameraLogServiceManager.__instance == None:
            CameraLogServiceManager.__instance = CameraLogService(camera_id)
        return CameraLogServiceManager.__instance