# -*- coding: utf-8 -*-
from flask_caching import Cache
from src.helpers.base_helper import BaseHelper

global_cache = Cache()


class CacheHelper(BaseHelper):
    
    def __init__(self):
        super().__init__()
        self.__cache = global_cache

    def set(self, key: str, value, timeout: float = None):
        result = self.__cache.set(key=key, value=value, timeout=timeout)
        return result

    def get(self, key: str):
        result = self.__cache.get(key=key)
        return result

    def delete(self, key: str):
        result = self.__cache.delete(key=key)
        return result

    def delete_many(self, keys):
        result = self.__cache.delete_many(*keys)
        return result

    def get_many(self, keys):
        result = self.__cache.get_many(*keys)
        return result


cache = CacheHelper()
