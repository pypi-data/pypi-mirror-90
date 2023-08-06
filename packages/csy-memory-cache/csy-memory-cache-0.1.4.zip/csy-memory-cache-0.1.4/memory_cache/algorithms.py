# coding=gbk
import time
from abc import ABCMeta, abstractmethod
from collections import OrderedDict

from memory_cache.timer import Timer

"""
回收算法
"""


class BaseAlgorithms(metaclass=ABCMeta):
    @abstractmethod
    def get(self, key):
        """
        获取存储键的值
        :param key: 存储键
        :return: value
        """
        return None

    @abstractmethod
    def set(self, key, value, expire=-1):
        """
        存储key，并增加超时时间
        :param key: key
        :param value: 值
        :param expire: 超时时间，单位秒（s)
        :return: 是否存储成功
        """
        return True

    @abstractmethod
    def delete(self, key):
        """
        删除key，同时删除存储中的键值对
        :param key: key
        :return: 是否删除成功
        """
        return True

    @abstractmethod
    def clear(self):
        """
        删除所有的键值对
        :return: 存储类
        """
        return True

    @abstractmethod
    def clear_timeout(self):
        """
        清理超时的键
        :return: 是否清除完成
        """
        return True


class LRU(BaseAlgorithms):
    """
    使用LRU算法进行存储
    """
    def __init__(self, storage, timer=Timer):
        self.capacity = 64
        self.cache = None
        self.timer = timer()
        self._storage = storage
        self.cache = OrderedDict()
        self.timer.do(self.clear_timeout)

    def get(self, key):
        if key in self.cache.keys():
            value = self.cache.pop(key)
            cache_value = self._storage.get(key)
            self.cache[key] = value
        else:
            cache_value = None
        return cache_value

    def set(self, key, value, expire=-1):
        if key in self.cache.keys():
            self.cache.pop(key)
        else:
            if len(self.cache) == self.capacity:
                old_key, _ = self.cache.popitem(last=False)
                self._storage.delete(old_key)
        expire_time = 0
        if expire != -1:
            expire_time = int(time.time())
        self.cache[key] = expire_time + expire
        self._storage.set(key, value)
        return True

    def delete(self, key):
        if len(self.cache) == 0:
            return True
        if key not in self.cache.keys():
            return False
        self.cache.pop(key)
        self._storage.delete(key)
        return True

    def clear(self):
        self.cache = OrderedDict()
        self._storage = type(self._storage)()
        return True

    def clear_timeout(self):
        for key in self.cache.keys():
            if self.cache[key] == -1:
                continue
            cur_time = int(time.time())
            if cur_time > self.cache[key]:
                self.delete(key)
