# coding=gbk
import pickle

from memory_cache.api import BaseCacheAPI

"""
Redis的API操作
"""


class RedisAPI(BaseCacheAPI):
    def __init__(self, storage, max_size=1024, limit_size=True):
        self._storage = storage
        self.max_size = max_size
        self.limit_size = limit_size

    def set(self, key, value, expire=-1):
        pick_value = pickle.dumps(value)
        if self.limit_size:
            if len(pick_value) > self.max_size:
                assert ValueError('超出内存限制')
        return self._storage.set(key, pick_value, expire=expire)

    def get(self, key):
        res = self._storage.get(key)
        if not res:
            return None
        return pickle.loads(res)

    def delete(self, key):
        return self._storage.delete(key)

    def exists(self, key):
        return self._storage.exists(key)

    def clear(self):
        return self._storage.clear()

    def nset(self, name, key, value, expire=-1):
        key_prefix = name
        return self.set(key_prefix + key, value, expire)

    def nget(self, name, key):
        key_prefix = name
        return self.get(key_prefix+key)

    def ndelete(self, name, key):
        key_prefix = name
        return self.delete(key_prefix + key)

    def nexists(self, name, key):
        key_prefix = name
        return self.exists(key_prefix + key)
