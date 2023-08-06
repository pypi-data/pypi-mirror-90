# coding=gbk
from redis import StrictRedis

from memory_cache.storage import BaseStorage


class RedisStorage(BaseStorage):
    def __init__(self, host, port, db, password=None):
        self._storage = StrictRedis(host=host, port=port, db=db, password=password)

    def set(self, key, value, **kwargs):
        expire = None
        if 'expire' in kwargs:
            tmp = kwargs['expire']
            if int(tmp) > 0:
                expire = tmp
        return self._storage.set(key, value, ex=expire)

    def get(self, key):
        return self._storage.get(key)

    def delete(self, key):
        return self._storage.delete(key)

    def exists(self, key):
        return self._storage.exists(key)

    def clear(self):
        return self._storage.flushdb()
