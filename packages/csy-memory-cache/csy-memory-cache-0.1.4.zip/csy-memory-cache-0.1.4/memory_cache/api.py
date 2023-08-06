# coding=gbk
import sys
from abc import ABCMeta, abstractmethod

from memory_cache.algorithms import LRU
from memory_cache.storage import SimpleStorage

"""
操作的API
"""


class BaseCacheAPI(metaclass=ABCMeta):
    @abstractmethod
    def set(self, key, value, expire=-1):
        """
        存储key-value数据
        :param key: 存储的key
        :param value: 存储的key对应的值
        :param expire: 存储超时时间，默认是不会过期
        """
        pass

    @abstractmethod
    def get(self, key):
        """
        根据key取值
        :param key: 存储的键
        :return: value: 获取的值
        """
        pass

    @abstractmethod
    def delete(self, key):
        """
        删除存储的键值对
        :param key: 键
        :return: items: 存储的键的值
        """
        pass

    @abstractmethod
    def exists(self, key):
        """
        判断存储的键是否存在
        :param key: 键
        :return: bool
        """
        pass

    @abstractmethod
    def clear(self):
        """
        清空键
        """
        pass

    @abstractmethod
    def nset(self, name, key, value, expire=-1):
        pass

    @abstractmethod
    def nget(self, name, key):
        pass

    @abstractmethod
    def ndelete(self, name, key):
        pass

    @abstractmethod
    def nexists(self, name, key):
        pass


class SimpleCacheAPI(BaseCacheAPI):
    def __init__(self, storage=None, algorithms=None, max_size=1024, memory_limit=True):
        """
        :param storage: 存储类，[storage.BaseStorage]
        :param max_size: 默认存储最大内存为1024字节的数据
        """
        self._storage = storage if storage is not None else SimpleStorage()
        self._alg = algorithms if algorithms is not None else LRU(self._storage)
        self.max_size = max_size
        self.memory_limit = memory_limit

    def exists(self, key):
        return key in self._alg.cache.keys()

    def clear(self):
        self._alg.clear()

    def set(self, key, value, expire=-1):
        if self.memory_limit:
            if sys.getsizeof(value) > self.max_size:
                assert ValueError('超出内存限制')
        return self._alg.set(key, value, expire)

    def get(self, key):
        return self._alg.get(key)

    def delete(self, key):
        return self._alg.delete(key)

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
