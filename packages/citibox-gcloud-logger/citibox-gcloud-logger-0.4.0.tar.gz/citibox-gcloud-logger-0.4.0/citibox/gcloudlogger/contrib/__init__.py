import abc
import time
import logging


class Middleware(abc.ABC):
    def __init__(self):
        self.logger = logging.getLogger('http_middleware')

    @staticmethod
    def _get_current_timestamp():
        return int(round(time.time() * 1000))

    def _get_url_fingerprint(self, req_url: str, params_values: dict):
        fingerprint = req_url
        for key, value in params_values.items():
            fingerprint = fingerprint.replace(value, f'{{{key}}}')

        return fingerprint
