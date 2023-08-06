# coding=gbk
from abc import ABCMeta, abstractmethod

"""
存储类
"""


class BaseStorage(metaclass=ABCMeta):
    @abstractmethod
    def set(self, key, value, **kwargs):
        """
        存储key-value数据
        :param key: 存储的key
        :param value: 存储的key对应的值
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


class SimpleStorage(BaseStorage):
    def __init__(self):
        self._hash_storage = dict()

    def set(self, key, value, **kwargs):
        self._hash_storage[key] = value

    def get(self, key):
        return self._hash_storage.get(key, None)

    def delete(self, key):
        value = self._hash_storage.get(key, None)
        del self._hash_storage[key]
        return value
