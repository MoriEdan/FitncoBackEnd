# -*- coding: utf-8 -*-


class ConfigUtil:

    def __init__(self, config=None):
        super().__init__()
        self._config = config

        if self._config is not None:
            self.init_app(config)

    def init_app(self, config=None):
        self._config = config

    def get(self, key):
        result = self._config[key]
        return result


config = ConfigUtil()
